get_login = {200 : "get request called for login"}
failed_login = {401: "post request login failed"}
login = {200: "login sucessfull",401: "user name or email already exists"}
get_register = {200 : "get request called for register"}
validation_msg = {400 : "enter proper details for registration"}
cart = {200:"added to cart",400 : "product id is not available"}
wishlist = { 200 : "added to wishlist",400 : "product id is invalid" }
search = {400:"the book u typed is not available"}
sort = {200 : "get request called for sort",400 : "enter correct values to sort"}
sql = {500 : 'mysql connection or syntax is improper'}
order = {200 : "get order method is called"}
order_post = {200 : "added data into db"}
checkout = {200: "order placed successfully"}