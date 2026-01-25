import logging
import threading

logger = logging.getLogger(__name__)


class LeakyBucket:

    def __init__(self, queue_size, process_rate):
        self.queue_size = queue_size
        self.process_rate = process_rate
        self.waiting_queue = list()
        self.size = 0
        self.lock = threading.Lock()
        threading.Timer(self.process_rate, self.release).start()

    def rate_limit(self, callback, args):
        with self.lock:
            if self.size == self.queue_size:
                logger.warning("Queue is full")
                return False
            else:
                logger.info(f"Adding request to the queue {callback.__name__} {args}")
                self.waiting_queue.append([callback, args])
                self.size += 1
                return True

    def release(self):
        with self.lock:
            if self.size == 0:
                logger.debug("No more request to process")
            else:
                callback_method, args = self.waiting_queue.pop(0)
                logger.info(f"Processing request {args}")
                self.size -= 1
                threading.Thread(target=callback_method, args=(args,), daemon=False).start()
        threading.Timer(self.process_rate, self.release).start()
