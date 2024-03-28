from typing import Annotated
from fastapi import Request, Depends
from repository import UserRepository
from providers.user_provider import UserProvider, UserProviderImpl
from providers.mail_provider import MailProvider
from coordinator import Coordinator
from .database import get_session, Session
import config


def _get_coordinator(request: Request) -> Coordinator: # NOTE: You can pass the DIContainer is the same way
    return request.app.state.coordinator # if hasattr(request.app.state, 'coordinator') else Coordinator()

def user_provider(
    session: Annotated[Session, Depends(get_session)], # managed by FastAPI Dependency Injection system
    coordinator: Annotated[Coordinator, Depends(_get_coordinator)]
) -> UserProvider:
    # UserProvider's lifecycle is bound to short endpoint's lifecycle, so it's safe to use strong references here
    return UserProviderImpl(
        repository=UserRepository(session),
        mail_provider=MailProvider(config.mail_token),
        output=coordinator, # make sure Coordinator implements UserProviderOutput Protocol,
        on_user_created=coordinator.on_user_created # or pass a callback function
        # on_user_created: lambda: coordinator.on_user_created() # add a lambda if the method's signature is not compatible
    )
