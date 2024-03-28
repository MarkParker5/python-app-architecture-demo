from threading import Thread
import weakref
import uvicorn
from api import get_app as get_fastapi_app
from entities.user import UserCreate
from providers.user_provider import UserProvider
from services.report_service import ReportService


class Coordinator:

    def __init__(self):
        self.users_count = 0 # some state that can be shared between different providers, services, layers, and the entire app

        # self.report_service = ReportService(
        #     get_users_count = lambda: self.users_count # Be aware of circular references
        # )

        # With weakref, you can avoid circular references and memory leaks

        weak_ref = weakref.ref(self)
        def get_users_count_weak_safe() -> int:
            if wself := weak_ref():
                return wself.users_count
            else:
                return 0 # provide default value to handle it safely or raise an exception if it's critical

        # self.report_service = ReportService(
        #     get_users_count = get_users_count_weak_safe
        # )

        # Alternatively, use WeakMethod
        #
        self.report_service = ReportService(
            get_users_count = lambda: (weakref.WeakMethod(self.get_users_count)() or (lambda: 0))() # not very pretty, but works; you can also use a helper function
        )

        # Discussion about weakref:
        # Coordinator holds a strong reference to the ReportService instance.
        # If the ReportService instance holds a reference to the Coordinator instance as well, for example, in a callback,
        # it will create a circular reference, and the garbage collector will not be able to collect these objects.
        # To avoid this, we use weakref to hold a weak reference to the Coordinator instance in the lambda function.
        # This way, the garbage collector will be able to collect the Coordinator instance if it's not referenced anywhere else,
        # so there is no memory leak
        # And then, the garbage collector will be able to collect the ReportService instance and the callback as well.
        # It means the reference graph looks like this: Coordinator -> ReportService -> callback -> Coordinator (weakref)
        # But be aware of cases when callback is called after Coordinator is already collected (weakref will return None).
        # They shouldn't exist, but you may handle it safely anyway. Decide what to do in such cases:
        # raise an exception, provide a default value, log a warning, just ignore it, etc.

    # Coordinator Interface Implementation

    def setup_initial_state(self):
        fastapi_app = get_fastapi_app()

        # You can pass the coordinator instance to the FastAPI app state so you can access it in the endpoints via DI system
        # You can also pass the DIContainer instance in the same way if you have and need it
        fastapi_app.state.coordinator = self

        # Start all services in separate threads
        # Alternatively, you can use an coroutines-based concurrency approach with async-await syntax
        # It's bit more complex, efficient and scalable, but the architecture will be the same
        fastapi_thread = Thread(target=lambda: uvicorn.run(fastapi_app))
        fastapi_thread.start()
        self.report_service.start() # already runs in a separate thread inside the service

    # UserProviderOutput Protocol Implementation

    def user_provider_created_user(self, provider: UserProvider, user: UserCreate):
        self.on_user_created(user)

    # Event handlers

    def on_user_created(self, user):
        print("User created: ", user)
        self.users_count += 1

        # Some cross-service logic here, just for example
        if self.users_count >= 10_000:
            self.report_service.interval_seconds *= 10
        elif self.users_count >= 10_000_000:
            self.report_service.stop() # example of controlling services from the coordinator

    # def on_user_created(self): # just an example of a callback with different signature
    #     print("User created")
    #     self.users_count += 1

    # Private

    def get_users_count(self) -> int:
        return self.users_count