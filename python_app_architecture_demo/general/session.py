from typing import ContextManager, Generator
from contextlib import contextmanager
from general import Session


class Session: # dummy
    def close(self): ...

@contextmanager
def create_session() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.close()
