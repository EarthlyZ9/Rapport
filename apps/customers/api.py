from ninja_extra import api_controller, route, ControllerBase, paginate
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_extra.searching import searching
from ninja_jwt.authentication import JWTAuth

from apps.customers.models import Customer
from apps.customers.schemas import (
    CustomerSchema,
    CustomerSimpleSchema,
    CustomerCreateSchema,
    CustomerUpdateSchema,
)
from apps.customers.services import CustomerService
from config.exceptions import InstanceNotFoundException, ExceptionSchema
from config.permissions import IsOwnerOrReadOnly


@api_controller(
    "/customers", tags=["Customer"], auth=JWTAuth(), permissions=[IsOwnerOrReadOnly]
)
class CustomerController(ControllerBase):
    def __init__(self, customer_service: CustomerService):
        self.service = customer_service
        self.model = Customer

    @route.get(
        "",
        response={200: NinjaPaginationResponseSchema[CustomerSimpleSchema]},
        by_alias=True,
    )
    @paginate()
    @searching(search_fields=["=name", "=flag", "=enticement_status"])
    def get_all_customers(self):
        user = self.context.request.user
        customers = Customer.objects.filter(fc_id=user.id).all()
        return customers

    @route.get(
        "/{customer_id}",
        response={200: CustomerSchema, 404: ExceptionSchema},
        by_alias=True,
    )
    def get_customer_by_id(self, customer_id: int):
        customer = self.get_object_or_exception(
            Customer.objects.prefetch_related("insurances"),
            id=customer_id,
            exception=InstanceNotFoundException,
            error_message="Customer with the provided id does not exist",
        )
        return customer

    @route.post("", response={201: CustomerSimpleSchema}, by_alias=True)
    def create_new_customer(self, data: CustomerCreateSchema):
        user = self.context.request.user
        user_data = data.dict()
        user_data["fc_id"] = user.id
        new_customer = Customer.objects.create(**user_data)
        return 201, new_customer

    @route.delete("/{customer_id}", response={204: None})
    def delete_customer_by_id(self, customer_id: int):
        customer = self.get_object_or_exception(
            Customer,
            id=customer_id,
            exception=InstanceNotFoundException,
            error_message="Customer with the provided id does not exist",
        )
        customer.delete()

        return 204, None

    @route.patch("/{customer_id}", response={200: CustomerSchema})
    def update_customer_by_id(self, customer_id: int, data: CustomerUpdateSchema):
        customer = self.get_object_or_exception(
            Customer,
            id=customer_id,
            exception=InstanceNotFoundException,
            error_message="Customer with the provided id does not exist",
        )

        customer_data: dict = data.dict(exclude_none=True)
        print(customer_data)

        for k, v in customer_data.items():
            setattr(customer, k, v)

        customer.save(update_fields=customer_data.keys())

        return customer
