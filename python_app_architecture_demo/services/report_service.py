from typing import Callable
import time
from .abstract_service import AbstractService


class ReportService(AbstractService):

    # Initialization

    def __init__(self, get_users_count: Callable[[], int | None]):
        super().__init__()
        self.get_users_count = get_users_count
        self.last_message_timestamp = 0
        self.interval_seconds = 3600 # 1 hour

    # AbstractService Implementation (private)

    def _loop_iteration(self):
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
