package aerospace

import (
	"context"
	"net/http"

	"github.com/coreos/go-oidc/v3/oidc"
)

const (
	cloudflareTeamURL = "https://vongogetem.cloudflareaccess.com"
	audienceTag       = "32eafc7626e974616deaf0dc3ce63d7bcbed58a2731e84d06bc3cdf1b53c4228"
)

func CloudflareAccessMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		tokenString := r.Header.Get("Cf-Access-Jwt-Assertion")
		if tokenString == "" {
			http.Error(w, "Missing Cloudflare Access token", http.StatusUnauthorized)
			return
		}

		ctx := context.Background()
		provider, err := oidc.NewProvider(ctx, cloudflareTeamURL)
		if err != nil {
			http.Error(w, "Failed to verify identity provider", http.StatusInternalServerError)
			return
		}

		verifier := provider.Verifier(&oidc.Config{
			ClientID: audienceTag,
		})

		idToken, err := verifier.Verify(ctx, tokenString)
		if err != nil {
			http.Error(w, "Invalid token signature or expired token", http.StatusUnauthorized)
			return
		}

		next.ServeHTTP(w, r)
	})
}
