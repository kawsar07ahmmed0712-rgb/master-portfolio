"""
Create the database if it does not exist.

- Reads DB credentials from backend/.env
- Connects to MySQL server (not a specific database)
- Runs: CREATE DATABASE IF NOT EXISTS ...
"""

from pathlib import Path

import pymysql
from dotenv import load_dotenv
import os


def load_env_from_backend() -> None:
    # We intentionally load env from backend/.env to keep secrets in one place.
    env_path = Path(__file__).resolve().parents[1] / "backend" / ".env"
    if not env_path.exists():
        raise FileNotFoundError(
            f"backend/.env not found at: {env_path}. Create it first."
        )
    load_dotenv(env_path)


def create_database_if_missing() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not all([user, password, db_name]):
        raise ValueError("DB_USER, DB_PASSWORD, DB_NAME must be set in backend/.env")

    # Connect to the MySQL server (no database selected yet).
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        autocommit=True,
        charset="utf8mb4",
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
    finally:
        connection.close()

    return db_name


def main() -> None:
    load_env_from_backend()
    db_name = create_database_if_missing()
    print(f"✅ Database ensured: {db_name}")


if __name__ == "__main__":
    main()
