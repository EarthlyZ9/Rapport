from ninja.errors import ValidationError
from ninja_extra import NinjaExtraAPI

from apps.customers.api import CustomerController
from apps.products.api import ProductController
from apps.schedules.api import ScheduleController
from apps.users.auth_api import AuthController
from config.renderer import ResponseRenderer

api = NinjaExtraAPI(
    openapi_extra={
        "info": {
            "termsOfService": "https://example.com/terms/",
            "contact": {"name": "EarthlyZ9", "email": "earthlyz9.dev@gmail.com"},
        },
    },
    title="Rapport API",
    description="Rapport, Managing personal customers",
    servers=[
        {"url": "http://localhost:8000", "description": "Development Local Server"}
    ],
    renderer=ResponseRenderer(),
)

api.register_controllers(AuthController)
api.register_controllers(CustomerController)
api.register_controllers(ScheduleController)
api.register_controllers(ProductController)


@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    return api.create_response(request, {"detail": exc.errors}, status=400)
