import jwt

from configs import CONFIG


async def decode_token(access_token: str) -> str:
    access_token = jwt.decode(access_token, CONFIG.JWT_SECRET, algorithms=["HS256"])
    return access_token