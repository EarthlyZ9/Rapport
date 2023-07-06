from django.conf import settings
from django.http import HttpResponse, HttpRequest
from ninja_extra import api_controller, route, ControllerBase
from ninja_extra.exceptions import AuthenticationFailed
from ninja_jwt.schema import TokenRefreshInputSchema, TokenRefreshOutputSchema
from django.contrib.auth.hashers import check_password

from apps.users.models import User
from apps.users.schemas import (
    LoginResponseSchema,
    LoginSchema,
    UserSchema,
    SignupSchema,
    EmailSchema,
)
from apps.users.services import AuthService
from config.exceptions import (
    BadRequestException,
    ExceptionSchema,
    DuplicateInstanceException,
    UnprocessableEntityException,
)


@api_controller("/auth", tags=["Auth"])
class AuthController(ControllerBase):
    def __init__(self, auth_service: AuthService):
        self.service = auth_service

    @route.post("/login", response=LoginResponseSchema)
    def login(self, data: LoginSchema):
        d = data.dict()
        email, password = d.get("email"), d.get("password")
        try:
            user: User = User.objects.get(email=email)
            if not check_password(password, user.password):
                raise AuthenticationFailed("Authentication failed. Incorrect password.")
        except User.DoesNotExist:
            raise AuthenticationFailed("Authentication failed. No user by this email.")

        tokens = self.service.generate_tokens_for_user(user)
        res = user.__dict__
        res.update(tokens)

        return res

    @route.post(
        "/signup",
        response={201: UserSchema, 400: ExceptionSchema, 422: ExceptionSchema},
    )
    def signup(self, request: HttpRequest, data: SignupSchema):
        # Check if duplicate email has been checked
        checked_duplicate = request.COOKIES.get("check-duplicate", None)
        if checked_duplicate is None:
            raise UnprocessableEntityException(
                "Email duplication check should be preceded"
            )

        # Check confirmation password
        data = data.dict()
        if data["password"] != data["confirm_password"]:
            raise BadRequestException("Password mismatch")

        # Create new user
        new_user: User = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            affiliation=data["affiliation"],
            name=data["name"],
        )

        return 201, new_user

    @route.post("/check-email", response={200: EmailSchema, 409: ExceptionSchema})
    def check_duplicate_email(self, response: HttpResponse, data: EmailSchema):
        email = data.dict()["email"]
        try:
            existing_user = User.objects.get(email=email)
            raise DuplicateInstanceException("Provided email already exists")
        except User.DoesNotExist:
            # set cookie
            response.set_cookie("check-duplicate", "complete")
            return {"email": email}

    @route.post(
        "/token/refresh",
        response=TokenRefreshOutputSchema,
    )
    def refresh_token(self, refresh_token: TokenRefreshInputSchema):
        return refresh_token.to_response_schema()

    @route.post("/logout", response={204: None})
    def logout(self, request: HttpRequest):
        request.COOKIES.clear()
        return 204, None
