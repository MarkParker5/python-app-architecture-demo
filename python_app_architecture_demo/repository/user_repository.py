from entities.user import UserCreate


# No business logic here, only clean CRUD operations
class UserRepository():

    def __init__(self, session: Session):
        # If you use a database, you probably need a session object
        # Then, lifecycle of this Repository is tied to the lifecycle of the session
        self.session = session
        self.users = []

    def add_user(self, user: UserCreate):
        # This is a mock implementation, you should use a database like Postgres via sqalchemy + asyncpg + alembic
        self.users.append(user)
