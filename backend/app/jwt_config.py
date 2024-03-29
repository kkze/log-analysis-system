# backend/app/jwt_config.py
from .models import TokenBlacklist

def configure_jwt(jwt):
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlacklist.query.filter_by(jti=jti).first() is not None
