# Huru Calendar

iCloud calendars on the Hurunagus desktop: a small headless Go daemon that syncs
your iCloud (CalDAV) calendars, and a Quickshell widget that shows them in the
bar. A deliberately narrow rebrand of
[Dux Calendar](https://github.com/duxlabs-dev/dux-calendar) (MIT).

## What this fork is (and isn't)

- **iCloud only.** No Google or Microsoft OAuth client is shipped or used —
  upstream's credentials are blanked, because their terms don't authorize
  rebranded builds. Local ICS directories, plain CalDAV, iCal feeds and
  Evolution still work; the Google/Microsoft providers stay compiled but inert
  until you supply your own client.
- **Daemon, not a desktop app.** `hcal daemon` is pure Go (`CGO_ENABLED=0`) with
  no Qt and no `dux-qt-base` runtime. The bar widget is the frontend, so there is
  no window, tray icon or shell process to start.
- **The upstream QML UI is still in the tree** (`quickshell/`, with its
  submodules) but is not built, installed or required.

## Install

In the hurunagus-hyprland image `huru-calendar` comes from the
`wegweg7979/huru-calendar` COPR — the image installs it, you don't. Elsewhere:

```bash
sudo dnf copr enable wegweg7979/huru-calendar
sudo dnf install huru-calendar
systemctl --user enable --now hcal     # sync + reminders at login
```

## iCloud setup

iCloud refuses your Apple ID password. Create an **app-specific password** at
<https://account.apple.com/account/manage> (Sign-In and Security → App-Specific
Passwords), then:

```bash
hcal account add icloud            # asks for Apple ID + the app-specific password
hcal account list                  # confirm the account and its calendars
hcal sync                          # first sync
```

`icloud` targets `caldav.icloud.com` with Apple's CalDAV discovery (calendar
colours, VTODO reminder lists and iCloud's placeholder-reminder quirk handled).
The password and any OAuth tokens live in the file-backed keyring under
`~/.local/share/dankcal/keyring`, never in plaintext.

## Command line

```bash
hcal daemon                        # run the sync daemon (IPC + HTTP, no UI)
hcal account list                  # connected accounts
hcal account add local ~/cal       # a directory of .ics files
hcal account add caldav            # any other CalDAV server
hcal account remove <account-id>
hcal sync [account-id]             # force a sync
hcal reminders                     # upcoming reminders
hcal events import invite.ics --calendar <id>
hcal events rsvp <event-id> accept
hcal kill                          # stop the running daemon
```

## IPC (what the widget talks to)

The daemon serves a unix socket at `$XDG_RUNTIME_DIR/dankcal-<pid>.sock`
(`DANKCAL_SOCKET` overrides it). Every call prints JSON:

```bash
hcal ipc list                                            # every method + params
hcal ipc events.list from=2026-11-01 to=2026-11-30       # agenda
hcal ipc reminders.upcoming
hcal ipc calendars.list
hcal ipc subscribe topics=events,calendars               # push updates instead of polling
```

`tasks.*` covers iCloud Reminders (VTODO) with the same account.

## Compatibility

The config, data, state and socket namespace stays `dankcal`, and the
`DANKCAL_*` environment variables are unchanged — an existing install keeps its
accounts, settings and database. Only the binary (`dcal` → `hcal`), the product
name, the icon and the shipped unit are renamed.

## Development

```bash
# headless build: no submodules, no build tags, no Qt
cd core && CGO_ENABLED=0 go build -trimpath -o hcal ./cmd/hcal

make test        # Go test suite
make fmt         # gofmt
```

`DANKCAL_SHELL_DIR` / `hcal -c <dir>` only matter for the unbuilt QML UI.

## Credits and licence

Based on [Dux Calendar](https://github.com/duxlabs-dev/dux-calendar) by Dux Labs
(Avenge Media LLC), MIT — the sync engine, providers, schema and CLI are theirs;
their copyright notice is retained in [LICENSE](LICENSE). Upstream's OAuth
client credentials are *not* included: `hcal account add google|microsoft` needs
your own registration, supplied via `DANKCAL_GOOGLE_CLIENT_ID` /
`DANKCAL_GOOGLE_CLIENT_SECRET` / `DANKCAL_MICROSOFT_CLIENT_ID`.

Also built on [Quickshell](https://quickshell.org/) (for the UI),
[Ent](https://entgo.io/) and [HUMA](https://huma.rocks/).
