from ninja_extra import api_controller, route, ControllerBase

from apps.customers.services import CustomerService


@api_controller("/customers", tags=["Customer"])
class CustomerController(ControllerBase):
    def __init__(self, customer_service: CustomerService):
        self.service = customer_service

    @route.get("")
    def list(self, request):
        return "customers"
