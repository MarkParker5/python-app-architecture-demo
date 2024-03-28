from models.user import User
from schemes.user_scheme import User as UserScheme


class UserMapper:

    def schemeToModel(self, scheme: UserScheme) -> User:
        return User(scheme.id, scheme.name, scheme.email, scheme.password)

    def modelToScheme(self, model: User) -> UserScheme:
        return UserScheme(model.id, model.name, model.email, model.password)
