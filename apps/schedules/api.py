from typing import Optional
import logging

from ninja import FilterSchema, Query
from ninja_extra import api_controller, route, ControllerBase, paginate
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth
from pydantic import Field

from apps.customers.models import Customer
from apps.schedules.models import CustomerSchedule
from apps.schedules.schemas import (
    ScheduleSchema,
    ScheduleUpdateSchema,
    ScheduleCreateSchema,
)
from apps.schedules.services import ScheduleService
from config.exceptions import (
    ExceptionSchema,
    InstanceNotFoundException,
    BadRequestException,
)
from config.permissions import IsOwnerOrReadOnly

logger = logging.getLogger("rapport")


class ScheduleFilterSchema(FilterSchema):
    name: Optional[str] = Field(q="customer__name__icontains")
    title: Optional[str]


@api_controller(
    "/schedules", tags=["Schedule"], auth=JWTAuth(), permissions=[IsOwnerOrReadOnly]
)
class ScheduleController(ControllerBase):
    def __init__(self, schedule_service: ScheduleService):
        self.service = schedule_service
        self.model = CustomerSchedule

    @route.get("", response=NinjaPaginationResponseSchema[ScheduleSchema])
    @paginate()
    def get_all_schedules(self, filters: ScheduleFilterSchema = Query(...)):
        schedules = (
            self.model.objects.select_related("customer")
            .filter(fc_id=self.context.request.user.id)
            .order_by("date")
            .all()
        )
        schedules = filters.filter(schedules)
        return schedules

    @route.get("/{schedule_id}", response={200: ScheduleSchema, 404: ExceptionSchema})
    def get_schedule_by_id(self, schedule_id: int):
        try:
            schedule = self.model.objects.get(id=schedule_id)
            return schedule
        except self.model.DoesNotExist:
            raise InstanceNotFoundException(
                "Customer schedule with the provided id does not exist"
            )

    @route.post("", response={201: ScheduleSchema})
    def create_customer_schedule(self, data: ScheduleCreateSchema):
        schedule_data = data.dict(exclude_none=True)
        if hasattr(schedule_data, "end_time"):
            schedule_data["has_end_time"] = True
        else:
            schedule_data["has_end_time"] = False

        schedule_data["fc_id"] = self.context.request.user.id

        new_schedule = self.model.objects.create(**schedule_data)

        return new_schedule

    @route.patch(
        "/{schedule_id}",
        response={200: ScheduleSchema, 403: ExceptionSchema, 404: ExceptionSchema},
    )
    def update_schedule_by_id(self, schedule_id: int, data: ScheduleUpdateSchema):
        schedule_data = data.dict(exclude_none=True)
        if len(schedule_data) == 0:
            raise BadRequestException("Body cannot be empty")

        # Check if valid customer id
        customer_id = schedule_data.get("customer_id", None)
        if customer_id is not None:
            try:
                Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                raise InstanceNotFoundException(
                    "Customer with the provided id does not exist"
                )

        if "end_time" in schedule_data:
            schedule_data["has_end_time"] = True

        schedule = self.get_object_or_exception(
            self.model,
            id=schedule_id,
            exception=InstanceNotFoundException,
            error_message="Customer schedule with the provided id does not exist",
        )
        # Save
        for k, v in schedule_data.items():
            setattr(schedule, k, v)

        schedule.save(update_fields=schedule_data.keys())

        return schedule

    @route.delete("/{schedule_id}", response={204: None, 404: ExceptionSchema})
    def delete_schedule_by_id(self, schedule_id: int):
        schedule = self.get_object_or_exception(
            self.model,
            id=schedule_id,
            exception=InstanceNotFoundException,
            error_message="Customer schedule with the provided id does not exist",
        )
        schedule.delete()

        return 204, None
