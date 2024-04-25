from mozilla_django_oidc.auth import (
    OIDCAuthenticationBackend as OIDCAuthenticationBackendBase,
)


class OIDCAuthenticationBackend(OIDCAuthenticationBackendBase):
    def filter_users_by_claims(self, claims):
        """Return all users matching the received claims."""
        sub = claims.get("sub")
        if not sub:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(oidc_sub__iexact=sub)

    def verify_claims(self, claims):
        """Verify the provided claims to decide if authentication should be allowed."""
        return "sub" in claims and "email" in claims and "name" in claims

    def get_username(self, claims):
        """Generate username based on claims."""
        if "preferred_username" in claims:
            return claims.get("preferred_username")
        return claims.get("sub")

    def get_name(self, claims):
        """Generate name based on claims."""
        if "name" in claims:
            return claims.get("name")
        return self.get_username(claims)

    def create_user(self, claims):
        """Return object for a newly created user account."""
        sub = claims.get("sub")
        email = claims.get("email")
        username = self.get_username(claims)
        name = self.get_name(claims)

        user = self.UserModel.objects.create_user(
            username, email=email, name=name, oidc_sub=sub
        )

        self.set_permissions(user, claims)

        return user

    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        email = claims.get("email")
        username = self.get_username(claims)
        name = self.get_name(claims)

        _logger.debug("Updating user %s", username)

        user.email = email
        user.username = username
        user.name = name

        self.set_permissions(user, claims, save=False)

        user.save()

        return user

    def set_permissions(self, user, claims, save=True):
        """Set user permissions based of groups provided in claims."""
        groups = claims.get("groups", [])
        user.is_superuser = "superuser" in groups
        user.is_staff = "staff" in groups
        if save:
            user.save()
