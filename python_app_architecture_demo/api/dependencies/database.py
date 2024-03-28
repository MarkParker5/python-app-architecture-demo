from typing import ContextManager, Generator
from contextlib import contextmanager


class Session: # dummy
    def close(self): ...

@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.close()
