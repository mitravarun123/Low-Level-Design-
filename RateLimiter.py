import time
from abc import ABC, abstractmethod
from enum import Enum


# -------------------- STRATEGY --------------------
class RateLimiterStrategy(ABC):
    @abstractmethod
    def allow_request(self, key: str) -> bool:
        pass


# -------------------- TOKEN BUCKET --------------------
class TokenBucketRateLimiter(RateLimiterStrategy):
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate   # tokens per second
        self.buckets = {}  # key -> [tokens, last_refill_time]

    def allow_request(self, key: str) -> bool:
        now = time.time()

        if key not in self.buckets:
            self.buckets[key] = [self.capacity, now]

        tokens, last_refill = self.buckets[key]

        # Refill tokens
        tokens += (now - last_refill) * self.refill_rate
        tokens = min(tokens, self.capacity)

        if tokens >= 1:
            tokens -= 1
            self.buckets[key] = [tokens, now]
            return True

        self.buckets[key] = [tokens, now]
        return False


# -------------------- FIXED WINDOW --------------------
class FixedWindowRateLimiter(RateLimiterStrategy):
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.requests = {}  # key -> [count, window_start]

    def allow_request(self, key: str) -> bool:
        now = int(time.time())

        if key not in self.requests:
            self.requests[key] = [0, now]

        count, window_start = self.requests[key]

        if now - window_start >= self.window_size:
            count = 0
            window_start = now

        if count < self.limit:
            self.requests[key] = [count + 1, window_start]
            return True

        return False


# -------------------- FACTORY --------------------
class RateLimiterType(Enum):
    TOKEN_BUCKET = "TOKEN_BUCKET"
    FIXED_WINDOW = "FIXED_WINDOW"


class RateLimiterFactory:
    @staticmethod
    def get_rate_limiter(limiter_type: RateLimiterType) -> RateLimiterStrategy:
        if limiter_type == RateLimiterType.TOKEN_BUCKET:
            return TokenBucketRateLimiter(capacity=5, refill_rate=1)
        elif limiter_type == RateLimiterType.FIXED_WINDOW:
            return FixedWindowRateLimiter(limit=5, window_size=10)
        else:
            raise ValueError("Invalid Rate Limiter Type")


# -------------------- SERVICE --------------------
class RateLimiterService:
    def __init__(self, strategy: RateLimiterStrategy):
        self.strategy = strategy

    def allow(self, key: str) -> bool:
        return self.strategy.allow_request(key)


# -------------------- CLIENT --------------------
if __name__ == "__main__":

    limiter = RateLimiterFactory.get_rate_limiter(
        RateLimiterType.TOKEN_BUCKET
    )

    service = RateLimiterService(limiter)

    user = "user_123"

    for i in range(10):
        allowed = service.allow(user)
        print(f"Request {i+1}: {'ALLOWED' if allowed else 'BLOCKED'}")
        time.sleep(0.5)
