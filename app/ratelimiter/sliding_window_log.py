import logging
import time
import threading

logger = logging.getLogger(__name__)


class SlidingWindowLog:

    def __init__(self, window_size, request_limit):
        self.window_size = window_size
        self.request_limit = request_limit
        self.timestamps = []
        self.lock = threading.Lock()

    def rate_limit(self):
        with self.lock:
            current_time = time.time()
            window_start = current_time - self.window_size

            # Remove timestamps outside the current window
            old_count = len(self.timestamps)
            self.timestamps = [ts for ts in self.timestamps if ts > window_start]
            removed = old_count - len(self.timestamps)
            if removed > 0:
                logger.debug(f"Removed {removed} expired timestamps, {len(self.timestamps)} remaining")
            

            if len(self.timestamps) < self.request_limit:
                logger.info(f"Request within limit, adding to log | timestamp {current_time}")
                self.timestamps.append(current_time)
                return True
            
            logger.warning(f"Rate limit applied, too many requests in window, last timestapm {self.timestamps[-1]}")
            return False
