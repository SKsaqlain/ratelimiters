import logging
import threading

logger = logging.getLogger(__name__)


class FixedWindowCounter:

    def __init__(self, window_size, max_requests):
        self.window_size = window_size
        self.max_requests = max_requests
        self.counter = max_requests
        self.lock = threading.Lock()
        threading.Timer(self.window_size, self.refresh_counter).start()

    def rate_limit(self):
        with self.lock:
            if self.counter == 0:
                logger.warning(
                    f"Rate limit applied, counter will reset after {self.window_size} seconds"
                )
                return False
            else:
                logger.info("Allowing request, decrementing counter")
                self.counter -= 1
                return True

    def refresh_counter(self):
        logger.debug(f"Refreshing counter after {self.window_size} second interval")
        with self.lock:
            self.counter = self.max_requests
            logger.info("Counter reset to maximum")
        threading.Timer(self.window_size, self.refresh_counter).start()
