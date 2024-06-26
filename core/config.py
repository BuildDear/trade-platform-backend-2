import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    # private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    # public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    private_key_path: Path = os.getenv("PRIVATE_RSA_KEY")
    public_key_path: Path = os.getenv("PUBLIC_RSA_KEY")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False
    auth_jwt: AuthJWT = AuthJWT()


settings = Setting()
