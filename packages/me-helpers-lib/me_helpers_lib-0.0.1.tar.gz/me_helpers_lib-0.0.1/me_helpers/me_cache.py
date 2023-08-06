from redis_dec import Cache
from redis import StrictRedis

redis = StrictRedis(decode_responses=True)
cache = Cache(redis)
