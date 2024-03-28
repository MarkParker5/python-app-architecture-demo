from abc import ABC, abstractmethod
from threading import Thread
import time


class AbstractService(ABC):

    # Init

    def __init__(self):
        self._is_running = False

    # Interface

    def start(self):
        self._is_running = True
        self._thread = Thread(target=self.main_loop)
        self._thread.start()

    def main_loop(self):
        # Main service loop, may be a coroutine in async-await syntax
        # can be private or public, depends if you want to allow to run the service manually
        while self._is_running:
            self._loop_iteration()
            time.sleep(1)

    def stop(self):
        self._is_running = False

    # Abstract

    @abstractmethod
    def _loop_iteration(self):
        pass
