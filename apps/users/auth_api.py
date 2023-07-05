from django.conf import settings
from ninja_extra import api_controller, route, ControllerBase
from ninja_extra.exceptions import AuthenticationFailed
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.schema import TokenRefreshInputSchema

from apps.users.schemas import (
    LoginResponseSchema,
    LoginSchema,
    UserSchema,
    SignupSchema,
)
from apps.users.services import AuthService


class RefreshAuthentication(JWTBaseAuthentication):
    def authenticate(self, request):
        refresh_token = request.COOKIES.get(
            settings.NINJA_JWT.get("REFRESH_TOKEN_NAME"), None
        )

        if refresh_token is None:
            raise AuthenticationFailed("Refresh token is missing")
        return self.jwt_authenticate(request, token=refresh_token)


@api_controller("/auth", tags=["Auth"])
class AuthController(ControllerBase):
    def __init__(self, auth_service: AuthService):
        self.service = auth_service

    @route.post("/login", response=LoginResponseSchema)
    def login(self, request, data: LoginSchema):
        pass

    @route.post("/signup", response=UserSchema)
    def signup(self, request, data: SignupSchema):
        pass

    @route.post(
        "/token/refresh",
        response=TokenRefreshInputSchema.get_response_schema(),
        url_name="token_refresh",
    )
    def refresh_token(self, refresh_token: TokenRefreshInputSchema):
        return refresh_token.to_response_schema()
