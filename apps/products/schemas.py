from ninja import ModelSchema

from apps.products.models import Product


class ProductSchema(ModelSchema):
    class Config:
        model = Product
        model_fields = "__all__"
