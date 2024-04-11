from typing import Annotated
from fastapi import Depends
from api.users.auth import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
