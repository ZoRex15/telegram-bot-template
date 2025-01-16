from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    tg_id: int

    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    created_at: datetime = datetime.now()