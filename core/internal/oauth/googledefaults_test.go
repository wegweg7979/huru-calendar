package oauth

import "testing"

// The Huru Calendar fork ships no OAuth client. Upstream's shipped credentials
// identify the Dux Calendar application and are not authorized for rebranded
// builds (see "OAuth client credentials" in the upstream README), so the
// default build must report "none" and callers must supply their own client via
// DANKCAL_GOOGLE_CLIENT_ID / DANKCAL_GOOGLE_CLIENT_SECRET, -ldflags -X, or the
// in-app custom-client option. iCloud/CalDAV needs no OAuth client at all.
func TestBuiltinCredentialsAbsent(t *testing.T) {
	if creds, ok := BuiltinGoogleCredentials(); ok {
		t.Fatalf("default build must ship no builtin Google client, got %q", creds.ClientID)
	}
	if creds, ok := BuiltinMicrosoftCredentials(); ok {
		t.Fatalf("default build must ship no builtin Microsoft client, got %q", creds.ClientID)
	}
}
