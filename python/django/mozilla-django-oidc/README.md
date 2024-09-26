# authentik, Django and mozilla-django-oidc

This project is an example of how to integration [authentik](https://goauthentik.io) with [mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc/).

You can follow the documentation about how to create an OAuth2/OpenID provider in authentik [here](https://docs.goauthentik.io/docs/providers/oauth2/).

The main files where things have been modified are:

### `example/settings.py`

mozilla-django-oidc has been added to the `INSTALLED_APPS` and `MIDDLEWARE` lists. Some settings have been added after the `## Custom settings` comment. Read about them in mozilla-django-oidc documentation.

### `example/auth.py`

Custom implementation of an authentication backend for mozilla-django-oidc. Allows for user uniqueness based on the `sub` claim instead of their email.

### `example/utils.py`

Utility functions to retrieve the OIDC configuration automatically from authentik.

### `example/urls.py`

Added the mozilla-django-oidc URLs. The redirect URL to configure in authentik would be `https://example.company/auth/oidc/callback/`

### `user/models.py`

Custom user model to add an `oidc_sub` field to uniquely identify a user. Also makes the username field non-unique and adds a `name` field instead of `first_name` and `last_name` to match the representation in authentik.
