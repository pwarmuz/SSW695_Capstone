class BaseConfig(object):

    # Flask
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 megabytes

    # MongoDB
    MONGO_HOST = 'enptfb55.com'
    MONGO_PORT = 27017

    # Configuration for analytics
    TRACK_USAGE_USE_FREEGEOIP = False
    TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS = 'include'
