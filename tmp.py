import jwt
import time

SECRET_KEY = "1234567890"

token = jwt.encode(
    {
        "user": "Kirill",
        "exp": int(time.time()) + 3600
    },
    SECRET_KEY,
    algorithm="HS256"
)

print(token)
