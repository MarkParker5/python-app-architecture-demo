from typing import Protocol, runtime_checkable, Callable
from typing_extensions import runtime_checkable
from repository import UserRepository
from providers.mail_provider import MailProvider
from entities.user import UserCreate


@runtime_checkable
class UserProvider(Protocol):
    def create_user(self, user: UserCreate): ...

@runtime_checkable
class UserProviderOutput(Protocol):  # also called "Delegate", "Observer", "Listener", "Subscriber", "Callback"
    def user_provider_created_user(self, provider: UserProvider, user: UserCreate): ...

# class UserProviderImpl(UserProvider): # some languages require to implement the interface explicitly, but in Python it's a question of style
class UserProviderImpl:

    def __init__(self,
        repository: UserRepository,
        mail_provider: MailProvider,
        output: UserProviderOutput | None,
        # alternative way to implement the output interface:
        # pass a callback function instead of an object that implements the protocol with the method
        on_user_created: Callable[[UserCreate], None] | None
    ):
        self.repository = repository
        self.mail_provider = mail_provider
        self.output = output
        self.on_user_created = on_user_created

    # UserProvider interface (protocol, input) implementation

    def create_user(self, user: UserCreate):
        # Main high-level business logic is here
        self.repository.add_user(user) # Use repository wrapper instead of direct DB access
        self.mail_provider.send_mail(user.email, f"Welcome, {user.name}!") # Some another logic besides simple CRUD. Also, it can be CRUD of another entity

        if output := self.output: # unwrap the optional
            output.user_provider_created_user(self, user) # Notify the delegate about the event

        # Alternative way to implement the output interface
        if on_user_created := self.on_user_created:
            on_user_created(user)
