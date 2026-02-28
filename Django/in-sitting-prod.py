Replace

# =============================================================================
# CACHING (TEMPORARY – no Redis)
# =============================================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Use DB sessions instead of Redis
SESSION_ENGINE = "django.contrib.sessions.backends.db"
