from ninja_extra import api_controller, route, ControllerBase

from apps.products.services import ProductService


@api_controller("/products", tags=["Product"])
class ProductController(ControllerBase):
    def __init__(self, product_service: ProductService):
        self.service = product_service

    @route.get("")
    def list(self, request):
        return "products"
