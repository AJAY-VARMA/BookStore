from marshmallow_sqlalchemy import ModelSchema
from model.model import User,ProductData

class ProductSchema(ModelSchema):
    class Meta:
        fields = ("pid","author","title","image","quantity","price","description")

class ProductOrderSchema(ModelSchema):
    class Meta:
        fields = ("author","title","image","quantity","price")