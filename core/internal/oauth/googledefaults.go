package oauth

import "encoding/base64"

// Shipped OAuth client for official builds (Google "Desktop app" client type,
// public per the installed-app model). Encoded — not encrypted — only so the
// values are not searchable plaintext in the repository; installed-app
// credentials cannot be kept confidential.
//
// Blanked in the Huru Calendar fork: the shipped client identifies the upstream
// Dux Calendar application, and its terms do not authorize rebranded builds
// (see "OAuth client credentials" in the upstream README). Blank means
// BuiltinGoogleCredentials reports "none", so a caller must supply its own via
// -ldflags "-X .../internal/oauth.builtinGoogleClientID=...", the
// DANKCAL_GOOGLE_CLIENT_ID / DANKCAL_GOOGLE_CLIENT_SECRET environment
// variables, or the in-app custom-client option. iCloud/CalDAV needs no OAuth
// client at all.
var (
	builtinGoogleClientID     = ""
	builtinGoogleClientSecret = ""
	encodedGoogleClientID     = ""
	encodedGoogleClientSecret = ""
)

func BuiltinGoogleCredentials() (GoogleAppCredentials, bool) {
	switch {
	case builtinGoogleClientID != "" && builtinGoogleClientSecret != "":
		return GoogleAppCredentials{ClientID: builtinGoogleClientID, ClientSecret: builtinGoogleClientSecret}, true
	case builtinGoogleClientID != "" || builtinGoogleClientSecret != "":
		return GoogleAppCredentials{}, false
	}

	id := deobfuscate(encodedGoogleClientID)
	secret := deobfuscate(encodedGoogleClientSecret)
	if id == "" || secret == "" {
		return GoogleAppCredentials{}, false
	}
	return GoogleAppCredentials{ClientID: id, ClientSecret: secret}, true
}

func deobfuscate(encoded string) string {
	raw, err := base64.StdEncoding.DecodeString(encoded)
	if err != nil {
		return ""
	}
	key := "com.danklinux.dankcalendar"
	for i := range raw {
		raw[i] ^= key[i%len(key)]
	}
	return string(raw)
}
