# huru-calendar.spec — Huru Calendar, the iCloud (CalDAV) sync daemon for the
# Hurunagus desktop.
#
# A fork of Dux Calendar (github.com/duxlabs-dev/dux-calendar, MIT) scoped to
# iCloud only and built HEADLESS: the daemon is pure Go, so there is no Qt, no
# dux-qt-base and no shell runtime to package. The upstream QML UI stays in the
# source tree but is not built here (that needs -tags withshell plus the
# dux-qml-common submodule), and upstream's OAuth client credentials are
# deliberately absent — iCloud needs none.
#
# COPR-safe: the only source is the tag archive. `go build` fetches modules, so
# the COPR project must have network access enabled.

# Pure Go, built with -s -w: there is no debug info to extract, and an empty
# debuginfo subpackage fails the build.
%global debug_package %{nil}

Name:           huru-calendar
Version:        2.1.2
Release:        1%{?dist}
Summary:        iCloud (CalDAV) calendar sync daemon for the Hurunagus desktop

License:        MIT
URL:            https://github.com/wegweg7979/huru-calendar
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

# Compiled for x86_64 — the only arch the hurunagus images target.
ExclusiveArch:  x86_64

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

# The daemon keeps the iCloud app-specific password in the Secret Service
# (gnome-keyring, D-Bus activated; a local file fallback exists for credentials
# written before the service appeared).
Requires:       gnome-keyring
# CalDAV is HTTPS.
Requires:       ca-certificates

%description
Huru Calendar syncs iCloud (CalDAV) calendars and serves them to a Quickshell
bar widget over a unix socket. It is a headless Go daemon — accounts, reminders,
recurring events and iCloud reminder lists (VTODO) included — with no Qt, no
shell process and no tray of its own.

Create an account with an Apple app-specific password (a regular Apple ID
password will not work):

    hcal account add icloud
    hcal sync

Then read the data over IPC, which is what the bar widget does:

    hcal ipc events.list from=2026-11-01 to=2026-11-30

%prep
%autosetup -n %{name}-%{version} -p1

%build
# Fedora 45 ships golang 1.27.3, exactly what core/go.mod asks for. Keep the
# toolchain local so the build cannot try to fetch a different one.
export GOTOOLCHAIN=local
export CGO_ENABLED=0
export BUILD_TIME="$(date -u '+%%Y-%%m-%%d_%%H:%%M:%%S')"
cd core
go build -trimpath \
    -ldflags "-s -w -X main.Version=%{version} -X main.BuildTime=${BUILD_TIME}" \
    -o ../hcal ./cmd/hcal
cd ..

%check
./hcal version

%install
install -Dm755 hcal %{buildroot}%{_bindir}/hcal
install -Dm644 assets/huru-calendar.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/huru-calendar.svg
install -Dm644 assets/systemd/hcal.service %{buildroot}%{_userunitdir}/hcal.service

mkdir -p completions
./hcal completion bash > completions/hcal
./hcal completion zsh  > completions/_hcal
./hcal completion fish > completions/hcal.fish
install -Dm644 completions/hcal      %{buildroot}%{_datadir}/bash-completion/completions/hcal
install -Dm644 completions/_hcal     %{buildroot}%{_datadir}/zsh/site-functions/_hcal
install -Dm644 completions/hcal.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/hcal.fish

%files
%license LICENSE
%{_bindir}/hcal
%{_userunitdir}/hcal.service
%{_datadir}/icons/hicolor/scalable/apps/huru-calendar.svg
%{_datadir}/bash-completion/completions/hcal
%{_datadir}/zsh/site-functions/_hcal
%{_datadir}/fish/vendor_completions.d/hcal.fish

%changelog
* Fri Nov 13 2026 wegweg7979 <wegweg7979@users.noreply.github.com> - 2.1.2-1
- Huru Calendar: rebrand of Dux Calendar 2.1.2, iCloud-only, headless daemon
