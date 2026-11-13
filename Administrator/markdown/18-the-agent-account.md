Title: Giving an AI Agent an Account
Subtitle: A recipe with no code: a Windows user and an SD account of the agent's own, so that the operating system is the wall.

An AI agent that works on an SD project needs a place to work and a limit on what it can reach. Prompts, tool scopes and promises inside the agent's own software protect against mistakes and against instructions hidden in the data it reads. **They do not stop an agent that holds a person's sign-in**: with it the agent can open an interactive `sd` as that person and do whatever the person can. The wall that holds is the operating system's, and this recipe is how to build it from what SD already has.

> **The agent is never you.** Do not give it your password, a shared password or a window that is already signed in.

The full recipe is `agent-pack/recipe/agent-account.md` in the SD Core for Windows source repository, with a template for the project's `CLAUDE.md` and a Claude Code skill that carries the SD knowledge (the User set describes them in *SD and AI Agents*). The installer puts the guide and the knowledge pack of the installed version under `C:\ProgramData\SD\sdsys\agent-pack\` (text, writable by the administrators only). The agent's own account cannot read that path, since a path outside an account needs `os-on` and this recipe does not give it, so copy the folder to the machine where the agent runs instead of opening a gate for it. In outline, signed in to Windows as SDSYS, in SD:

1. **Make the account**, with the fewest gates that let it do its job: `create.account user proj-agent ssh bp-on`. `ssh` gives the remote route, and `bp-on` lets the account compile and catalog (without it even `basic` is refused). The verb asks for a password for the new Windows user and `no.query` does not suppress that, so it cannot be scripted. Leave `sh-on`, `os-on`, `sd-on`, `voc-on`, `dict-on`, `net-on`, `files-on` and `shared-write-on` off. Every word you add widens what an instruction hidden in a record could make the agent do.
2. **Keep its password where only the agent's software reads it.** SD Core for Windows signs every ssh session in with the account's name and password, never a key. Every ssh session of an SD account is forced into `sd` for that account, so the sign-in gives a session in SD and no command prompt.
3. **Give it a workspace of its own**, populated with copies. Keep the production data in accounts the agent is not a member of. If it must see real data, put that data in a group account of its own and add the agent to it with `modify.account`.
4. **Prove the wall** before you trust it. As the agent, try the things the guide says are refused: the `sh` verb, `os.execute`, a path outside the account, a write to the VOC, a restricted statement. Each must be refused in the words the guide quotes. If one succeeds, a gate is open that you did not mean to open.
5. **Keep the hand-over human.** The agent proposes; a person reads the program and copies it into the production account.
6. **Take it back** with `modify.account proj-agent none` (the ssh route), `modify.account proj-agent suspended`, or by changing the Windows user's password.

## What this does not give you

There are no scopes inside the account: the agent can read, change and delete everything in its own account and in any group account it belongs to, which is why the production data is elsewhere. The audit trail names what the agent did, not what it saw. There is no MCP door yet, and a project-scope `.mcp.json` for it is a shape in the source repository, not something to use. And no setting protects you from a prompt that persuades the agent to ask *you* for more: the answer to a request to switch a gate on is yours, and the safe default is no.

None of this recipe has been run end to end on SD Core for Windows for this release.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Remote access and the machine](05-remote-access-and-the-machine.html).
