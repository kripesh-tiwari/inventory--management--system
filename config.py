import os

class Config:
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

```
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://inventory_user:change_me@localhost:3306/inventory_db"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
```
