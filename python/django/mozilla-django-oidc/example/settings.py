"""
Django settings for example project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from os import environ
from pathlib import Path

from django.urls import reverse_lazy

from example import utils

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+^)eoj5qe)gq$t5fittf=+tdt7z4#v85&g@@#hkl(7#&$!xgcu"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
]

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "example.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


## Custom settings

# To add the oidc sub field
AUTH_USER_MODEL = "user.User"


# If you need django-rest-framework authentication
OIDC_DRF_AUTH_BACKEND = "example.auth.OIDCAuthenticationBackend"
AUTHENTICATION_BACKENDS = [
    OIDC_DRF_AUTH_BACKEND,
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = reverse_lazy("oidc_authentication_init")
LOGOUT_URL = reverse_lazy("oidc_logout")

# OIDC_URL should contain the provider issuer, for instance https://authentik.company/application/o/app/
OIDC_OP_CONFIG_URL = environ["OIDC_URL"] + "/.well-known/openid-configuration"
OIDC_TIMEOUT = environ.get("OIDC_TIMEOUT", 15)

# Add other scopes you may need here
OIDC_RP_SCOPES = " ".join(["openid", "email", "profile"])
OIDC_OP_CONFIG = utils.get_oidc_config(OIDC_OP_CONFIG_URL, timeout=OIDC_TIMEOUT)
OIDC_OP_AUTHORIZATION_ENDPOINT = OIDC_OP_CONFIG["authorization_endpoint"]
OIDC_OP_TOKEN_ENDPOINT = OIDC_OP_CONFIG["token_endpoint"]
OIDC_OP_USER_ENDPOINT = OIDC_OP_CONFIG["userinfo_endpoint"]
# From the provider configuration
OIDC_RP_CLIENT_ID = environ["OIDC_CLIENT_ID"]
OIDC_RP_CLIENT_SECRET = environ["OIDC_CLIENT_SECRET"]
OIDC_RP_SIGN_ALGO = environ.get("OIDC_RP_SIGN_ALGO", "RS256")

if OIDC_RP_SIGN_ALGO == "RS256":
    OIDC_OP_JWKS_ENDPOINT = OIDC_OP_CONFIG["jwks_uri"]
