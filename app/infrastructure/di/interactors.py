from dishka import Provider, Scope, provide

from app.application.users.create_user import CreateUser
from app.application.users.get_user_by_id import GetUserById
from app.application.users.get_user_by_tg_id import GetUserByTgId
from app.application.users.get_all_users import GetAllUsers
from app.application.mailing.create import CreateMailing
from app.application.mailing.update import UpdateMailing
from app.application.mailing.get_by_id import GetMailingById
from app.application.mailing.save_metadata import SaveMailingMetadata
from app.application.mailing.get_metadata_by_id import GetMailingMetadataById
from app.application.mailing.delete_metadata import MailingDeleteMetadata


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)
    get_user_by_id = provide(GetUserById)
    get_user_by_tg_id = provide(GetUserByTgId)
    get_all_users = provide(GetAllUsers)
    
    create_mailing = provide(CreateMailing)
    update_mailing = provide(UpdateMailing)
    get_mailing_by_id = provide(GetMailingById)
    get_mailing_metadata = provide(GetMailingMetadataById)
    save_mailing_metadata = provide(SaveMailingMetadata)
    delete_mailing_metadata = provide(MailingDeleteMetadata)