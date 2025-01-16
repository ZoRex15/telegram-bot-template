from dishka import Provider, Scope, provide

from app.application.users.create_user import CreateUser
from app.application.users.get_user_by_id import GetUserById
from app.application.users.get_user_by_tg_id import GetUserByTgId


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)
    get_user_by_id = provide(GetUserById)
    get_user_by_tg_id = provide(GetUserByTgId)