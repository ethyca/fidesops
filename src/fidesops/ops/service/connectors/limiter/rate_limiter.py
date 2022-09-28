import logging
import time

from fidesops.ops.common_exceptions import (
    RedisConnectionError
)

from fidesops.ops.util.cache import (
    FidesopsRedis,
    get_cache,
)

logger = logging.getLogger(__name__)

class RateLimiter():
    """
    """
    def get(
        self, key: str, 
    ) -> None:
        """"""
        second_limit = 100
        timeout_seconds = 30

        try:
            redis: FidesopsRedis = get_cache() 
        except RedisConnectionError as exc:
            print(f"Failed to connect to redis, skipping limiter. {exc}")
            return

        start_time = time.time()
        while(time.time() - start_time < timeout_seconds):
            current_seconds = int(time.time())
            pipe = redis.pipeline()
            pipe.incrby(f"{key}:seconds:{current_seconds}", 1)
            pipe.expire(f"{key}:seconds:{current_seconds}", 30)
            res = pipe.execute()

            if int(res[0]) > second_limit:
                print("Hit tps limit, waiting")
                time.sleep(.1)
            else:
                print(f"Used {res[0]} of tps limit {second_limit}")
                return
        
        print("Timeout waiting for rate limiter")
        raise Exception("Timeout waiting for rate limiter")

