from ninja import ModelSchema, Schema

from apps.users.models import User
from config.to_camel_case import to_camel_case


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
        alias_generator = to_camel_case
        allow_population_by_field_name = True


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
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class RefreshTokenSchema(Schema):
    refresh: str


class TokenSchema(Schema):
    access: str
    refresh: str


class EmailSchema(Schema):
    email: str
