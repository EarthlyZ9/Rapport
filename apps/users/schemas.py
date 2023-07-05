from ninja import ModelSchema, Schema

from apps.users.models import User


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = [
            "id",
            "email",
            "name",
            "affiliation",
            "created_at",
            "updated_at",
        ]


class LoginSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["email", "password"]


class LoginResponseSchema(UserSchema):
    access: str
    refresh: str


class SignupSchema(ModelSchema):
    confirm_password: str

    class Config:
        model = User
        model_fields = ["email", "password", "name", "affiliation"]


class RefreshTokenSchema(Schema):
    refresh: str


class TokenSchema(Schema):
    access: str
    refresh: str
