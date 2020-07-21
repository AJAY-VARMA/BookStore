from flask import Flask,Blueprint
from views import Login,Register,RegisterEmail,GetBooks,Sort,Cart,Wishlist,Order,CheckOut

def initialize_routes(api):
    api.add_resource(Login,'/login')
    api.add_resource(Register,'/register')
    api.add_resource(RegisterEmail , '/register-email/<token>')
    api.add_resource(GetBooks,'/getbooks')
    api.add_resource(Sort,'/getbooks/sort-by-price')
    api.add_resource(Cart,'/getbooks/add-to-cart')
    api.add_resource(Wishlist,'/getbooks/add-to-wishlist')
    api.add_resource(Order,'/getbooks/add-to-cart/order')
    api.add_resource(CheckOut,'/getbooks/add-to-cart/checkout')
