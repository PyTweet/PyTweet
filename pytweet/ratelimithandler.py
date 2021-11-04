import time

class RatelimitHandler:
    def __init__(
        self,
        limit: float,
    ):
        self._limit: float = limit
    

    def is_ratelimited(self):
        return time.time() < self._limit
  