package oauth

// Shipped Entra app registration for official builds (public client, PKCE only
// — client IDs are public identifiers, so no secret and no obfuscation).
// This identifies the upstream Huru Calendar application: distribution packages
// built from this repository may ship it unchanged; forks and rebranded builds
// must register their own app and override via -ldflags -X, or blank this to
// require user-supplied credentials.
// Blanked in the Huru Calendar fork: upstream's app registration is not
// authorized for rebranded builds. Supply your own via
// DANKCAL_MICROSOFT_CLIENT_ID or -ldflags -X.
var builtinMicrosoftClientID = ""

func BuiltinMicrosoftCredentials() (MicrosoftAppCredentials, bool) {
	if builtinMicrosoftClientID == "" {
		return MicrosoftAppCredentials{}, false
	}
	return MicrosoftAppCredentials{ClientID: builtinMicrosoftClientID}, true
}
