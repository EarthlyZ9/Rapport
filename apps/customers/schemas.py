from datetime import date
from typing import List, Optional

from ninja import ModelSchema, Schema

from apps.customers.models import Customer
from apps.products.schemas import ProductSchema
from apps.users.schemas import UserSchema
from config.to_camel_case import to_camel_case


class CustomerSimpleSchema(ModelSchema):
    class Config:
        model = Customer
        model_exclude = ["insurances"]
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class CustomerSchema(ModelSchema):
    fc: UserSchema
    insurances: List[ProductSchema]

    class Config:
        model = Customer
        model_fields = "__all__"
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class CustomerCreateSchema(ModelSchema):
    class Config:
        model = Customer
        model_fields = ["name", "date_of_birth", "calendar"]
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class CustomerUpdateSchema(Schema):
    name: Optional[str]
    date_of_birth: Optional[date]
    calendar: Optional[str]
    enrollment_date: Optional[date]
    enticement_status: Optional[str]
    flag: Optional[str]

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
