from ninja_extra import api_controller, route, ControllerBase
from apps.products.tasks import do_calc_total
from apps.products.services import ProductService


@api_controller("/products", tags=["Product"])
class ProductController(ControllerBase):
    def __init__(self, product_service: ProductService):
        self.service = product_service

    @route.get("")
    def list(self, request):
        return "products"

    @route.get("/test-celery")
    def test_celery(self):
        do_calc_total.delay()
        return "Done"
