#
# tclmap.py <sdb_ai/sd64/sdsys/newvoc>
#
# Assign every SD TCL verb to exactly one document, and CHECK THAT THE DOCUMENT
# ACTUALLY DOCUMENTS IT.  docmap.py does the first half for the SD BASIC roster;
# this does both halves for the verbs.
#
# ***WHY THE SECOND HALF EXISTS.***  On 27 Aug 2026 the TCL coverage was
# recorded as "127 of 144, 17 left".  It was 118, and ten verbs had no page.
# Seven of the ten were counted as covered because their NAME appeared
# somewhere - `listu` inside a warning on another page, `lock` inside the word
# "unlock", `create.account` inside a keyword table on the editor page.  The
# count had been answering "does this string occur" and the question is "is this
# verb explained here".  A map alone cannot tell the difference, so this script
# does not trust its own map: for every verb it also requires evidence on the
# page.
#
# EVIDENCE IS DELIBERATELY NARROW.  A verb counts as documented on a page only
# if the page mentions it backticked - `verb` - or begins a line with it inside
# a fenced code block, which is what the syntax blocks look like.  Prose alone
# is not evidence.  If that is too strict for a real page, widen the page, not
# this test.
#
# THE ROSTER IS COMPUTED, NEVER TYPED.  RELEASE_1.1 64 (18 Sep 2026) removed
# the three account tiers and newvoc/TIER.ADD.ADMINISTRATOR with them - this
# script crashed outright against a tree past that model, the same way
# mktclsyntax.py did.  The roster is now every verb record in `newvoc`, plus
# whatever `voc_template` (SDSYS's own, a sibling of `newvoc`) has that
# `newvoc` does not - computed by reading both directories directly, not by
# a list.  A VOC record is a verb if the first character of field 1 is V, or
# - for the four records that are a keyword AND a verb - the first character
# of field 3.
#
# EXITS NON-ZERO on: a verb assigned nowhere, a verb assigned twice, a verb
# assigned to a page that does not evidence it, an assignment naming a verb
# that is not on the roster, or a roster that came out empty.
#
import io
import os
import re
import sys

if len(sys.argv) < 2:
    sys.exit('usage: tclmap.py <path to sdsys/newvoc>')

NEWVOC = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- the roster

def field(rec, n):
    return rec[n - 1] if len(rec) >= n else ''

def verbs_in(directory):
    found = set()
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        with io.open(path, encoding='latin-1', newline='') as f:
            rec = [l.rstrip('\r\n') for l in f.read().split('\n')]
        t1 = field(rec, 1)[:1].upper()
        t3 = field(rec, 3)[:1].upper()
        if t1 == 'V' or (t1 == 'K' and t3 == 'V'):
            found.add(name.lower())
    return found

roster = verbs_in(NEWVOC)
VOCT = os.path.join(os.path.dirname(NEWVOC), 'voc_template')
roster |= verbs_in(VOCT)

if len(roster) < 100:
    sys.exit('REFUSED: roster came out as %d verbs - that is not a roster'
             % len(roster))

# ------------------------------------------------------------ the assignment
#
# Each entry is (set, markdown filename, verbs).  Keep it in page order.

DOCS = [
 ('User', '19-sd-tcl-command-processor.md', """
   abort clear.data clear.input clr
   display go if message off pause quit redo report.src stop break
 """),
 # The command stack, the @-variables and the session verbs left 19 for 19a
 # when the page was cut in two.  The twelve below were named by tclmap itself,
 # one NO EVIDENCE row each, which is the map working as designed.
 ('User', '19a-sd-tcl-the-command-stack.md', """
   alias clear.abort clear.stack get.stack list.vars logto option save.stack
   set set.exit.status who who.am.i
 """),
 ('User', '20-sd-tcl-files-and-records.md', """
   analyze.file clear.file cname compare.files configure.file
   convert.data copy create.file ct delete delete.file dump file.stat find.file fixdir fstat
   fstat.user hsm import.csv import.json import.xml list.files list.triggers profiler
   set.file set.trigger oscopy
 """),
 ('User', '21-sd-tcl-query-processor.md', """
   count list list.item list.label reformat scan search show sort sort.item
   sort.label sreformat sum
 """),
 ('User', '22-sd-tcl-select-lists.md', """
   clear.select copy.list delete.list form.list get.list
   execute.list merge.list move.list nselect
   qselect save.list select select.dir show.list sort.list sselect
 """),
 ('User', '23-sd-tcl-alternate-key-indexes.md', """
   analyse.index build.index create.index delete.index disable.index list.index
   rebuild.all.indices selectindex
 """),
 ('User', '24-sd-tcl-programs-and-the-catalogue.md', """
   basic catalog decatalog delete.catalog map run
 """),
 # 13 Nov 26 (RELEASE_1.1 269): 24 was cut in two; the program-development verbs and the IDE are explained on 24a.
 # 17 Nov 26 (coordinator, D8): Linux's own page 24 is over the 14,000-character limit, so the split stays.
 ('User', '24a-sd-tcl-find-program-dictionaries-and-the-ide.md', """
   compile.dict debug delete.common find.program format generate ide list.common
 """),
 ('User', '25-sd-tcl-ed.md', """
   ed
 """),
 ('User', '26-sd-tcl-edit.md', """
   edit
 """),
 ('User', '27-sd-tcl-micro.md', """
   micro
 """),
 # 13 Nov 26 (RELEASE_1.1 269): the pages carried with the TUI (RELEASE_1.1 197) had no entry here.
 ('User', '27a-sd-tcl-sed.md', """
   sed
 """),
 ('User', '27b-sd-tcl-ced.md', """
   ced
 """),
 ('User', '28-sd-tcl-printing-and-spooling.md', """
   block.print block.term printer setptr
   sp.view spool como report.style
 """),
 ('User', '29-sd-tcl-the-terminal-and-the-session.md', """
   autologout bell clear.prompts command.logging date
   date.format echo hush list.term.types logmsg nls pterm sleep term time
 """),
 # 26 Oct 26 the home screen page (Linux 4a50799 docs; RELEASE_1.1 172)
 ('User', '29a-sd-tcl-the-home-screen.md', """
   exit home menu my.menu set.start.default set.tile tool.keys
 """),
 # 13 Nov 26 (RELEASE_1.1 246): the AI, carried from Linux S.69 (Linux's map has the same two entries).
 ('User', '29b-sd-tcl-asking-the-ai.md', """
   ai
 """),
 ('User', '29c-sd-tcl-the-development-tools.md', """
   tool.files tool.voc tool.dict tool.query tool.bulk tool.catalog tool.test
 """),
 # 15 Nov 26 (RELEASE_1.1 299): file transfer, carried from Linux S.242 (Linux's map has the same entry).
 ('User', '29e-sd-tcl-moving-files-in-and-out.md', """
   receive send
 """),
 ('User', '30-sd-tcl-processes-and-phantoms.md', """
   list.phantoms pdebug pdump phantom pstat status
 """),
 ('User', '31-sd-tcl-locks.md', """
   release
 """),
 ('Administrator', '01-accounts-and-security.md', """
   create.account load.help modify.account modify.password
   tool.gates tool.menus tool.accounts
 """),
 # THE MAINTENANCE VERBS MOVED TO 01a AND ONLY ONE OF THEM SAID SO.  tclmap
 # reported set.date and passed the other four, because 01 still MENTIONS
 # clean.account, config, delete.account and update.accounts - in the "two
 # gates" paragraph and in a refusal example - and a backtick is evidence.
 # That is the incidental-mention false positive this script exists for,
 # arriving from the other direction: the name is on the page and the
 # explanation is not.  Each verb is assigned where it is actually explained.
 ('Administrator', '01a-account-maintenance.md', """
   clean.account config delete.account list.voc.removed load.examples remove.examples
   restore.voc set.date update.accounts
 """),
 # 9 Nov 26 (RELEASE_1.1 197): set.batch is explained on the scheduled jobs page of Getting Started; Core's Administrator guide has no such page.
 ('GettingStarted', '04-scheduled-jobs.md', """
   set.batch
 """),
 ('Administrator', '01b-backup-and-restore.md', """
   backup.account restore.account set.backup.directory settings.report tool.backups
 """),
 ('Administrator', '02-sessions-and-locks.md', """
   clear.locks inhibit.login list.locks list.readu listu lock lock.tracer logout tool.sessions unlock
 """),
 ('Administrator', '03-operating-system-access.md', """
   sh docs.install
 """),
 ('Administrator', '05-remote-access-and-the-machine.md', """
   append.sd.path remote.api remote.ssh ssh.server tool.remote
 """),
 # 13 Nov 26 (RELEASE_1.1 269): the configuration verbs (RELEASE_1.1 218), scheduled jobs (222), the master files and run.in (201).
 ('Administrator', '07-sd-admin-configuration.md', """
   set.config tool.config
 """),
 ('Administrator', '17-scheduled-jobs.md', """
   set.job tool.jobs
 """),
 ('Administrator', '19-the-master-files.md', """
   run.in tool.entries
 """),
 # 14 Nov 26 (RELEASE_1.1 247): the audit trail page, carried from Linux; in voc_template (SDSYS's set), not in newvoc.
 ('Administrator', '20-the-audit-trail.md', """
   tool.audit
 """),
 # 13 Nov 26 (RELEASE_1.1 246): Linux's page is Administrator 20; here 20 is the audit trail, so the AI is 21 (the help records name it).
 ('Administrator', '21-the-ai-helper.md', """
   set.ai tool.ai
 """),
 # 13 Nov 26 (RELEASE_1.1 202): remote administration over ssh (Linux's remote.sdsys, the SDRADMIN account here).
 ('Administrator', '22-remote-administration.md', """
   remote.sdsys
 """),
 # 25 Oct 26 SDNet carry (RELEASE_1.1 171): the SDNet client's five verbs are explained on the Administrator page for SDNet.
 ('Administrator', '12a-sdnet.md', """
   set.server delete.server list.servers set.netlogin delete.netlogin
 """),
 # 26 Oct 26: both pages already explain these; the map had no entry for them.
 ('Administrator', '13-the-shared-account.md', """
   list.shared
 """),
 ('Administrator', '04-sd-encryption.md', """
   encrypt.key
 """),
]

# Verbs deliberately not given a page of their own, with the reason.  These
# still have to be justified out loud rather than silently dropped.
# Nothing is exempt today, and that is the intended state.  An entry here has to
# carry the reason it is not on a page, so that "we skipped it" cannot look the
# same as "it is covered".  set.date lived here for one revision on a reason
# that turned out to be false - it was named on a USER page, not an
# administrator one - which is exactly the failure this dictionary invites.
EXEMPT = {}

# ------------------------------------------------------------------ evidence

# A long page is kept to about 14,000 characters by splitting it into parts
# (Nov 2026, page-length rule in README.md).  The map names the page that kept
# the number; a verb is documented on it when ANY part of it is evidence, so
# the map need not change each time a section moves from one part to the next.
SPLITS = {
    ('Administrator', '01-accounts-and-security.md'): [
        '01-accounts-and-security-2-making-an-account.md',
        '01-accounts-and-security-3-edit-switches.md',
        '01-accounts-and-security-4-modify-account.md',
        '01-accounts-and-security-5-gates-recovery-transfer-and-start.md',
        '01-accounts-and-security-6-home-screen-shared-account-and-net.md',
        '01-accounts-and-security-7-files-only-ai-and-passwords.md'],
    ('Administrator', '02-sessions-and-locks.md'): ['02a-locks-and-the-sessions-screen.md'],
    ('Administrator', '07-sd-admin-configuration.md'): [
        '07a-sd-admin-configuration-changing-from-sd.md',
        '07b-sd-admin-configuration-api-printing-and-netfiles.md'],
    ('Administrator', '12a-sdnet.md'): [
        '12a-sdnet-servers.md', '12b-sdnet-logins.md', '12c-sdnet-files-only-route.md',
        '12d-sdnet-administration-group-and-read-only-files.md',
        '12e-sdnet-writing-and-locking.md', '12f-sdnet-waits-and-audit.md'],
    ('Administrator', '19-the-master-files.md'): [
        '19a-the-master-files-global-change.md', '19b-run-in.md'],
    ('Administrator', '21-the-ai-helper.md'): ['21a-the-ai-helper-set-ai-and-the-key.md'],
    ('User', '07-sd-basic-file-handling.md'): ['07a-sd-basic-locking-and-asking-about-a-file.md'],
    ('User', '12a-sd-basic-the-screen-statement.md'): [
        '12b-sd-basic-the-screen-statement-forms.md',
        '12c-sd-basic-the-screen-statement-widgets.md',
        '12d-sd-basic-the-screen-statement-events-and-styles.md'],
    ('User', '17-sd-basic-debugging.md'): ['17a-sd-basic-debugging-full-screen-and-ai.md'],
    ('User', '20-sd-tcl-files-and-records.md'): [
        '20-sd-tcl-files-and-records-2-comparing-triggers-and-import.md'],
    ('User', '21-sd-tcl-query-processor.md'): ['21a-sd-tcl-query-processor-headings-and-output.md'],
    ('User', '24a-sd-tcl-find-program-dictionaries-and-the-ide.md'): [
        '24b-sd-tcl-the-ide-keys.md', '24c-sd-tcl-the-ide-other-files-and-options.md',
        '24d-sd-tcl-the-ide-zoom-fields-and-dictionary-items.md',
        '24e-sd-tcl-the-ide-ai-and-the-window.md'],
    ('User', '29-sd-tcl-the-terminal-and-the-session.md'): [
        '29-sd-tcl-the-terminal-and-the-session-2-timers-dates-and-logging.md'],
    ('User', '29c-sd-tcl-the-development-tools.md'): [
        '29c1-sd-tcl-tool-dict.md', '29c2-sd-tcl-tool-query.md', '29c3-sd-tcl-tool-bulk.md',
        '29c4-sd-tcl-tool-catalog-and-tool-test.md'],
    ('User', '37-sd-client-api.md'): ['37-sd-client-api-2-select-lists-and-the-rest.md'],
}


def evidence(setname, filename):
    """Names backticked on the page (and its split parts), plus names starting a line in a fence."""
    parts = [filename] + SPLITS.get((setname, filename), [])
    union = None
    for part in parts:
        one = evidence_one(setname, part)
        if one is None:
            return None
        union = one if union is None else (union | one)
    return union


def evidence_one(setname, filename):
    """Names backticked on the page, plus names starting a line in a fence."""
    path = os.path.join(HERE, setname, 'markdown', filename)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding='utf-8', newline='') as f:
        text = f.read()
    found = set(m.lower() for m in re.findall(r'`([a-z!][a-z0-9._!]*)`', text))
    in_fence = False
    for line in text.split('\n'):
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            m = re.match(r'^:?([a-z!][a-z0-9._!]*)', line.strip())
            if m:
                found.add(m.group(1).lower())
    return found

# ------------------------------------------------------------------- checking

assigned = {}
problems = []

for setname, filename, block in DOCS:
    verbs = block.split()
    ev = evidence(setname, filename)
    if ev is None:
        problems.append('MISSING PAGE   %s/%s' % (setname, filename))
        continue
    if not ev:
        problems.append('NO EVIDENCE AT ALL on %s/%s - refusing to score it'
                        % (setname, filename))
        continue
    for v in verbs:
        if v not in roster:
            problems.append('NOT A VERB     %-18s claimed by %s/%s'
                            % (v, setname, filename))
            continue
        if v in assigned:
            problems.append('ASSIGNED TWICE %-18s %s and %s'
                            % (v, assigned[v], filename))
            continue
        assigned[v] = '%s/%s' % (setname, filename)
        if v not in ev:
            problems.append('NO EVIDENCE    %-18s assigned to %s/%s but the '
                            'page neither backticks it nor opens a syntax line '
                            'with it' % (v, setname, filename))

for v in EXEMPT:
    if v in roster:
        assigned[v] = 'exempt'

missing = sorted(roster - set(assigned))
for v in missing:
    problems.append('NO PAGE        %-18s is a verb and is on no page' % v)

print('roster        : %d verbs' % len(roster))
print('assigned      : %d' % len([v for v in assigned if assigned[v] != 'exempt']))
print('exempt        : %d  %s' % (len(EXEMPT), ', '.join(sorted(EXEMPT))))
print('documents     : %d across %d set(s)'
      % (len(DOCS), len(set(d[0] for d in DOCS))))
print()

if problems:
    print('=== %d PROBLEM(S) ===' % len(problems))
    for p in problems:
        print('  ' + p)
    sys.exit(1)

print('every verb is on exactly one page, and every page evidences the verbs '
      'assigned to it.')
