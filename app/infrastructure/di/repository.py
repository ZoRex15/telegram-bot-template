from dishka import Provider, Scope, provide

from app.infrastructure.db.repository import UsersRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    users_repository = provide(UsersRepository)

    