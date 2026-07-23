"""Create a single administrator account through the configured MongoDB connection."""

from getpass import getpass

from pymongo.errors import DuplicateKeyError

from app.database import get_database
from app.schemas import RegisterRequest
from app.security import hash_password


def main() -> None:
    email = input("Admin email: ")
    password = getpass("Admin password: ")
    payload = RegisterRequest(email=email, password=password)
    users = get_database().users
    users.create_index("email", unique=True)

    try:
        users.insert_one(
            {
                "email": payload.email,
                "password_hash": hash_password(payload.password),
                "role": "admin",
            }
        )
    except DuplicateKeyError:
        print("An account with this email already exists.")
        return

    print(f"Admin account created for {payload.email}.")


if __name__ == "__main__":
    main()
