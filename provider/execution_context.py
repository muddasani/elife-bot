import redis
from pydoc import locate


def Session(settings):
    settings_session_class = "RedisSession"  # Default
    if hasattr(settings, 'session_class'):
        settings_session_class = settings.session_class

    session_class = locate('provider.execution_context.' + settings_session_class)
    return session_class(settings)

# class Session(object):
#     def __new__(self, settings):
#         settings_session_class = "RedisSession"  # Default
#         if hasattr(settings, 'session_class'):
#             settings_session_class = settings.session_class
#
#         session_class = locate('provider.execution_context.' + settings_session_class)
#         return session_class(settings)


class FileSession(object):

    # TODO : replace with better implementation - e.g. use Redis/Elasticache

    def __init__(self, settings):
        self.settings = settings

    def store_value(self, execution_id, key, value):
        f = open(self.settings.workflow_context_path + self.get_full_key(execution_id, key), 'w')
        f.write(value)

    def get_value(self, execution_id, key):
        try:
            f = open(self.settings.workflow_context_path + self.get_full_key(execution_id, key), 'r')
            return f.readline()
        except:
            return None

    @staticmethod
    def get_full_key(execution_id, key):
        return execution_id + '__' + key


class RedisSession(object):
    def __init__(self, settings):
        self.expire_key = settings.redis_expire_key
        self.r = redis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

    def store_value(self, execution_id, key, value):
        self.r.hset(execution_id, key, value)
        self.r.expire(execution_id, self.expire_key)

    def get_value(self, execution_id, key):
        return self.r.hget(execution_id,key)
