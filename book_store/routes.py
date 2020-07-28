from flask import Flask,Blueprint
from views import Login,Register,RegisterEmail,Books,Sort,Cart,Wishlist,Order,CheckOut

def initialize_routes(api):
    api.add_resource(Login,'/login')
    api.add_resource(Register,'/register')
    api.add_resource(RegisterEmail , '/register/<token>')
    api.add_resource(Books,'/books')
    api.add_resource(Sort,'/books/sort')
    api.add_resource(Cart,'/books/cart')
    api.add_resource(Wishlist,'/books/wishlist')
    api.add_resource(Order,'/books/cart/order')
    api.add_resource(CheckOut,'/books/cart/checkout')
