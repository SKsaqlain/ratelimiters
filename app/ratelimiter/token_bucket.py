import logging
import threading

logger = logging.getLogger(__name__)


class TokenBucket:

    def __init__(self, bucket_size, refill_seconds):
        self.bucket_size = bucket_size
        self.tokens = bucket_size
        self.refill_seconds = refill_seconds
        self.lock = threading.Lock()
        threading.Timer(refill_seconds, self.refill).start()

    def rate_limit(self):
        with self.lock:
            if self.tokens == 0:
                logger.warning("No more tokens")
                return False
            else:
                logger.info("Assigning token to api")
                self.tokens -= 1
                return True

    def refill(self):
        logger.debug("Initiating token refill")
        with self.lock:
            if self.tokens == self.bucket_size:
                logger.debug("Bucket is full")
            else:
                logger.info("Adding new token")
                self.tokens += 1
        threading.Timer(self.refill_seconds, self.refill).start()
