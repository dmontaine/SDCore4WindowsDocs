#!/usr/bin/env python3
"""
mkfooterpdf.py - print one mkdoc.py page to a PDF whose footer reads, left to
right, the NAME OF THE SECTION the page is in, the PAGE NUMBER and the DATE.

    python tools/mkfooterpdf.py <page.html> <out.pdf> [--date "9 November 2026"]

WINDOWS PORT, 9 Nov 2026 (RELEASE_1.1 177), of SD Core for Linux's
tools/mkfooterpdf.py (its owner's request of 24 Oct 2026 for the changes
document).  What differs, and why:
  * It is ONE FILE.  Linux imports its mkbookpdf.py for the browser finder and the
    DevTools client; this repository's book PDF is mkbookpdf.ps1, so the small
    stdlib WebSocket client (class CDP) and wait_for_debug_port are copied here
    from Linux's mkbookpdf.py, unchanged.
  * No poppler.  Linux calls pdfinfo, pdftotext and pdfunite; this machine has no
    pdfinfo or pdfunite, so the page count, the text of each page and the join are
    done with pypdf (a pure-Python package, already installed here).
  * The browser is Chrome or Edge from their Windows install folders.
  * Two checks Linux's script does not make: it says how many of the page's
    headings it actually FOUND in the printed text (a run that found none would
    have labelled every page with the document title and passed), and it reads
    the footer of the first and last page of the result back and refuses the PDF
    if the date is not there.

How it works (as Linux's):
  1. one full print, only to learn which page each heading falls on (the text of
     each page is read and the headings are looked for in the order they appear in
     the HTML, so a word that is also a table cell cannot match out of turn);
  2. one print of each run of pages that share a section, with pageRanges, whose
     footer template carries that section's name and Chrome's own page number
     (which stays the page number of the whole document when pageRanges is used -
     the script refuses the result if the page count differs from the full print);
  3. pypdf joins the pieces.

WHAT IS LOST.  The join does not carry the bookmark tree, so this PDF has no
outline.

The section is the page's last <h2>; under the h2 "New Features Unique to SD
Core" it is that h2 and the last <h3>.
"""

import argparse
import base64
import datetime
import html
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import uuid

UNIQUE = 'New Features Unique to SD Core'


def find_browser():
    for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'):
        if os.path.isfile(p):
            return p
    for name in ('chrome', 'msedge'):
        found = shutil.which(name)
        if found:
            return found
    return None


class CDP:
    """A minimal, blocking WebSocket client speaking just enough of RFC 6455 to drive Chrome DevTools Protocol - stdlib
    only.  Copied unchanged from SD Core for Linux's tools/mkbookpdf.py."""

    def __init__(self, ws_url, timeout=30):
        assert ws_url.startswith('ws://'), ws_url
        host_port, _, path = ws_url[len('ws://'):].partition('/')
        path = '/' + path
        host, _, port = host_port.partition(':')
        port = int(port or 80)
        self.sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(uuid.uuid4().bytes).decode()
        req = ('GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\n'
               'Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n'
               'Sec-WebSocket-Version: 13\r\n\r\n') % (path, host, port, key)
        self.sock.sendall(req.encode())
        status = self._recv_http_headers().split(b'\r\n', 1)[0]
        if b'101' not in status:
            raise RuntimeError('WebSocket handshake failed: %r' % status)
        self._next_id = 1

    def _recv_http_headers(self):
        data = b''
        while b'\r\n\r\n' not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            data += chunk
        return data

    def _recvn(self, n):
        out = bytearray()
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise RuntimeError('connection closed mid-frame')
            out += chunk
        return bytes(out)

    def _send_frame(self, opcode, payload):
        header = bytearray([0x80 | opcode])
        mask_bit = 0x80
        length = len(payload)
        if length <= 125:
            header.append(mask_bit | length)
        elif length <= 0xFFFF:
            header.append(mask_bit | 126)
            header += struct.pack('>H', length)
        else:
            header.append(mask_bit | 127)
            header += struct.pack('>Q', length)
        mask = os.urandom(4)
        header += mask
        masked = bytearray(payload)
        for i in range(len(masked)):
            masked[i] ^= mask[i % 4]
        self.sock.sendall(bytes(header) + bytes(masked))

    def _recv_frame(self):
        first2 = self._recvn(2)
        fin = first2[0] & 0x80
        opcode = first2[0] & 0x0F
        masked = first2[1] & 0x80
        length = first2[1] & 0x7F
        if length == 126:
            length = struct.unpack('>H', self._recvn(2))[0]
        elif length == 127:
            length = struct.unpack('>Q', self._recvn(8))[0]
        payload = self._recvn(length)
        if masked:
            mask = payload[:4]
            payload = payload[4:]
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        return fin, opcode, payload

    def _recv_message(self, timeout=None):
        if timeout is not None:
            self.sock.settimeout(timeout)
        parts = []
        while True:
            fin, opcode, payload = self._recv_frame()
            if opcode == 0x8:
                raise RuntimeError('server closed the connection')
            if opcode == 0x9:
                self._send_frame(0xA, payload)  # pong
                continue
            if opcode in (0x1, 0x0):
                parts.append(payload)
            if fin:
                break
        return b''.join(parts).decode('utf-8')

    def call(self, method, params=None, timeout=90):
        """Send a CDP command and wait for ITS response, discarding any event notifications that arrive first."""
        my_id = self._next_id
        self._next_id += 1
        self._send_frame(0x1, json.dumps({'id': my_id, 'method': method, 'params': params or {}}).encode())
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self._recv_message(timeout=max(1, deadline - time.time())))
            if msg.get('id') == my_id:
                if 'error' in msg:
                    raise RuntimeError('%s: %s' % (method, msg['error']))
                return msg.get('result', {})
        raise RuntimeError('%s: no response within %ds' % (method, timeout))

    def wait_for_event(self, method_name, timeout=90):
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self._recv_message(timeout=max(1, deadline - time.time())))
            if msg.get('method') == method_name:
                return msg
        raise RuntimeError('%s never arrived within %ds' % (method_name, timeout))

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


def wait_for_debug_port(port, timeout=15):
    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen('http://127.0.0.1:%d/json/version' % port, timeout=1):
                return
        except OSError as e:
            last_err = e
            time.sleep(0.2)
    raise RuntimeError('the browser never opened its debugging port: %s' % last_err)


def headings(page_html):
    """[(level, text)] of every h2 and h3 of the page, in order."""
    out = []
    for m in re.finditer(r'<h([23])[^>]*>(.*?)</h\1>', page_html, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        t = re.sub(r'\s*[#\u00b6]$', '', t).strip()
        out.append((int(m.group(1)), t))
    return out


def page_texts(pdf):
    """The text of each page, as a list of stripped lines (pypdf in place of pdftotext)."""
    from pypdf import PdfReader
    return [[ln.strip() for ln in (p.extract_text() or '').split('\n')] for p in PdfReader(pdf).pages]


def page_count(pdf):
    from pypdf import PdfReader
    return len(PdfReader(pdf).pages)


def labels_for(pages, heads, title):
    """One label for each page: the last section heading on the page, or the one in force when the page began if it has
    none.  Taking the LAST heading means every section is named on at least the page it starts on.  Returns the labels
    and how many headings were found."""
    labels = []
    h2 = title
    h3 = ''
    nxt = 0
    for lines in pages:
        up = [ln.upper() for ln in lines]   # the stylesheet prints an h3 in capitals, so compare in capitals
        while nxt < len(heads) and heads[nxt][1].upper() in up:
            lvl, text = heads[nxt]
            if lvl == 2:
                h2, h3 = text, ''
            else:
                h3 = text
            nxt += 1
        labels.append(h2 + (' \u00b7 ' + h3 if h2 == UNIQUE and h3 else ''))
    return labels, nxt


def footer_template(label, date):
    e = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    cell = 'flex:1;'
    return ('<div style="width:100%;font-size:9px;color:#555;padding:0 8mm;'
            'display:flex;font-family:Arial,sans-serif;">'
            '<span style="' + cell + 'text-align:left;">' + e(label) + '</span>'
            '<span style="' + cell + 'text-align:center;"><span class="pageNumber"></span></span>'
            '<span style="' + cell + 'text-align:right;">' + e(date) + '</span>'
            '</div>')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('html')
    ap.add_argument('pdf')
    today = datetime.date.today()
    ap.add_argument('--date', default='%d %s' % (today.day, today.strftime('%B %Y')))
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()

    html_path = os.path.abspath(args.html)
    pdf_path = os.path.abspath(args.pdf)
    page_html = open(html_path, encoding='utf-8').read()
    heads = headings(page_html)
    m = re.search(r'<title>(.*?)</title>', page_html, re.S)
    title = html.unescape(m.group(1)).split(' - ')[0].strip() if m else 'Changes'
    sys.stdout.write('mkfooterpdf: page %s\nmkfooterpdf: out  %s\nmkfooterpdf: date %s\n' % (html_path, pdf_path, args.date))
    if not heads:
        sys.stderr.write('mkfooterpdf: no h2 or h3 in %s\n' % html_path)
        return 1
    browser = find_browser()
    if not browser:
        sys.stderr.write('mkfooterpdf: no Chrome or Edge found\n')
        return 1
    try:
        import pypdf  # noqa: F401
    except ImportError:
        sys.stderr.write('mkfooterpdf: pypdf is not installed (pip install pypdf)\n')
        return 1
    sys.stdout.write('mkfooterpdf: browser %s\n' % browser)

    work = tempfile.mkdtemp(prefix='mkfooterpdf-')
    profile = os.path.join(work, 'profile')
    port = 9500 + (os.getpid() % 300)
    proc = subprocess.Popen(
        [browser, '--headless=new', '--disable-gpu', '--no-first-run',
         '--no-default-browser-check', '--user-data-dir=' + profile,
         '--remote-debugging-port=%d' % port, 'about:blank'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cdp = None
    tab_id = None
    pages = []
    try:
        wait_for_debug_port(port)
        file_url = 'file:///' + urllib.parse.quote(html_path.replace('\\', '/'), safe=':/')
        # A BLANK tab first, then Page.enable, THEN the page: opening the page directly with /json/new lets it finish loading
        # before Page.enable, and the load event is never seen (measured here, 9 Nov 2026: a 180 s timeout on a local file).
        req = urllib.request.Request('http://127.0.0.1:%d/json/new?about:blank' % port, method='PUT')
        with urllib.request.urlopen(req, timeout=10) as r:
            tab = json.loads(r.read().decode())
        tab_id = tab['id']
        cdp = CDP(tab['webSocketDebuggerUrl'])
        cdp.call('Page.enable')
        cdp.call('Page.navigate', {'url': file_url})
        cdp.wait_for_event('Page.loadEventFired', timeout=args.timeout)

        base = {'printBackground': True, 'marginTop': 0.4, 'marginBottom': 0.5,
                'marginLeft': 0.4, 'marginRight': 0.4, 'preferCSSPageSize': False}

        def printed(path, **extra):
            opts = dict(base)
            opts.update(extra)
            res = cdp.call('Page.printToPDF', opts, timeout=args.timeout)
            with open(path, 'wb') as f:
                f.write(base64.b64decode(res['data']))

        full = os.path.join(work, 'full.pdf')
        printed(full, displayHeaderFooter=False)
        pages = page_texts(full)
        labels, found = labels_for(pages, heads, title)
        sys.stdout.write('mkfooterpdf: %d pages; %d of the page\'s %d headings found in the printed text, in order\n'
                         % (len(pages), found, len(heads)))
        if found == 0:
            sys.stderr.write('mkfooterpdf: no heading was found in the printed text, so every footer would name the title only\n')
            return 1

        runs = []
        for i, lab in enumerate(labels, 1):
            if runs and runs[-1][2] == lab:
                runs[-1][1] = i
            else:
                runs.append([i, i, lab])
        pieces = []
        for k, (a, b, lab) in enumerate(runs):
            piece = os.path.join(work, 'p%03d.pdf' % k)
            printed(piece, displayHeaderFooter=True, headerTemplate='<span></span>',
                    footerTemplate=footer_template(lab, args.date), pageRanges='%d-%d' % (a, b))
            pieces.append(piece)
            sys.stdout.write('  pages %3d-%-3d  %s\n' % (a, b, lab))
        from pypdf import PdfWriter
        writer = PdfWriter()
        for piece in pieces:
            writer.append(piece)
        with open(pdf_path, 'wb') as f:
            writer.write(f)
    finally:
        if cdp:
            cdp.close()
        if tab_id:
            try:
                urllib.request.urlopen('http://127.0.0.1:%d/json/close/%s' % (port, tab_id), timeout=5)
            except OSError:
                pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        if not os.environ.get('MKFOOTERPDF_KEEP'):
            shutil.rmtree(work, ignore_errors=True)

    n_out = page_count(pdf_path)
    if n_out != len(pages):
        sys.stderr.write('mkfooterpdf: %d pages out, %d in the full print\n' % (n_out, len(pages)))
        return 1
    out_pages = page_texts(pdf_path)
    for idx in (0, n_out - 1):
        if not any(args.date in ln for ln in out_pages[idx]):
            sys.stderr.write('mkfooterpdf: page %d of the result has no footer with the date %r\n' % (idx + 1, args.date))
            return 1
    sys.stdout.write('mkfooterpdf: wrote %s (%d pages; the footer with the date read back on the first and last page)\n'
                     % (pdf_path, n_out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
