import datetime
from typing import Optional

import pydantic
from django.core.exceptions import ValidationError
from ninja import ModelSchema
from pydantic import root_validator

from apps.customers.schemas import CustomerSchema
from apps.schedules.models import CustomerSchedule
from apps.schedules.services import ScheduleService
from config.exceptions import BadRequestException
from config.to_camel_case import to_camel_case


class ScheduleSchema(ModelSchema):
    customer: CustomerSchema

    class Config:
        model = CustomerSchedule
        model_fields = "__all__"
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class ScheduleCreateSchema(ModelSchema):
    customer_id: int

    class Config:
        model = CustomerSchedule
        model_fields = ["title", "date", "start_time", "end_time"]
        model_fields_optional = ["start_time", "end_time"]
        alias_generator = to_camel_case
        allow_population_by_field_name = True

    @root_validator(pre=False)
    def validate_time_and_date(cls, values):
        if not ScheduleService.date_format_validator(values.get("date")):
            raise BadRequestException("Invalid date format, should be %Y-%m-%d")

        if hasattr(values, "end_time") and not hasattr(values, "start_time"):
            raise BadRequestException("start_time should be specified with end_time")

        if (
            hasattr(values, "end_time")
            and not ScheduleService.time_format_validator(values.get("end_time"))
        ) or (
            hasattr(values, "start_time")
            and not ScheduleService.time_format_validator(values.get("start_time"))
        ):
            raise BadRequestException("Invalid time format, should be %H:%M")

        if (
            hasattr(values, "end_time") and hasattr(values, "start_time")
        ) and values.get("start_time") > values.get("end_time"):
            raise BadRequestException("start_time should be ahead of end_time")

        return values


class ScheduleUpdateSchema(ModelSchema):
    customer_id: Optional[int]

    class Config:
        model = CustomerSchedule
        model_fields = ["title", "date", "start_time", "end_time"]
        model_fields_optional = "__all__"
        alias_generator = to_camel_case
        allow_population_by_field_name = True

    @root_validator(pre=False)
    def validate_time_and_date(cls, values):
        date = values.get("date")
        if date and not ScheduleService.date_format_validator(values.get("date")):
            raise BadRequestException("Invalid date format, should be %Y-%m-%d")

        if hasattr(values, "end_time") and not hasattr(values, "start_time"):
            raise BadRequestException("start_time should be specified with end_time")

        if (
            hasattr(values, "end_time")
            and not ScheduleService.time_format_validator(values.get("end_time"))
        ) or (
            hasattr(values, "start_time")
            and not ScheduleService.time_format_validator(values.get("start_time"))
        ):
            raise BadRequestException("Invalid time format, should be %H:%M")

        if (
            hasattr(values, "end_time") and hasattr(values, "start_time")
        ) and values.get("start_time") > values.get("end_time"):
            raise BadRequestException("start_time should be ahead of end_time")

        return values
