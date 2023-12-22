from typing import Final

import requests
import requests_cache
from yarl import URL

from retirement_calculator.models import User

# cache API requests as user data is static
requests_cache.install_cache(
    "retirement_calculator", backend="filesystem", use_temp=True
)


USER_API_ROOT: Final[URL] = URL(
    "https://pgf7hywzb5.execute-api.us-east-1.amazonaws.com/users"
)


def get_user_data(user_id: int) -> User:
    # edge case: limit user_id max value to some sane upper bound?
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, not {type(user_id)}")

    url = USER_API_ROOT / str(user_id)
    data = requests.get(url).json()
    return User(id=user_id, **data["user_info"], **data["assumptions"])
