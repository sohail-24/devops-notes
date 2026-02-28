# =============================================================================
# CACHING (Redis in Production)
# =============================================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 100,
        },
        "KEY_PREFIX": "django_ecommerce_prod",
        "TIMEOUT": 300,
    }
}

# Session cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"











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
