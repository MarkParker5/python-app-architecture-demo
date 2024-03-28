from typing import Callable
import time
from threading import Thread


class ReportService:

    # Initialization

    def __init__(self, get_users_count: Callable[[], int | None]):
        self.get_users_count = get_users_count
        self.last_message_timestamp = 0
        self.interval_seconds = 3600 # 1 hour
        self._is_running = False

    # Service Interface Implementation

    def start(self):
        report_service_thread = Thread(target=self.run)
        report_service_thread.start()

    def run(self):
        # Main service loop, may be a coroutine in async-await syntax
        # can be private or public, depends if you want to allow to run the service manually
        is_running = True
        self.last_message_timestamp = 0
        while self._is_running:
            self._report_if_needed()
            time.sleep(1)

    def stop(self):
        self._is_running = False

    # Private

    def _report_if_needed(self):
        now = time.monotonic()
        if now - self.last_message_timestamp > self.interval_seconds:
            last_message_timestamp = now
            if users_count := self.get_users_count():
                print(f"The current number of registered users is: {users_count}")
            else:
                # Probably, the coordinator is already collected, so we can't get the users count.
                # Decide what to do in this case, for example,
                # stop the app, raise an exception, provide a default value, log the state, or just ignore it
                pass
