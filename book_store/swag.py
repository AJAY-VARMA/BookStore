login = [
            {
              "name": "username",
              "description": "enter username for the login",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "password",
              "description": "enter password for the login",
              "required": True,
              "type": "string",
              "paramType": "form"
            }
 ]

register = [
            {
              "name": "username",
              "description": "enter username to register",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "email",
              "description": "enter email to register",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "password",
              "description": "enter password to register",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "confirm",
              "description": "re-enter  password to register",
              "required": True,
              "type": "string",
              "paramType": "form"
            }
 ]
search = [
            {
              "name": "search",
              "description": "enter author or book name to search",
              "required": True,
              "type": "string",
              "paramType": "param"
            }
          ]
sort = [
            {
              "name": "sort",
              "description": "enter sort value according to price",
              "required": True,
              "type": "string",
              "paramType": "param"
            }
      ]
jwt = [
        {
          "name": "Authorization",
          "description": "jwt token for the wishlist",
          "required": True,
          "type": "string",
          "paramType": "header"
        }
      ]
product = [
            {
              "name": "Authorization",
              "description": "jwt token for the wishlist",
              "required": True,
              "type": "string",
              "paramType": "header"
            },{
              "name": "productid",
              "description": "product id to add to wishlist",
              "required": True,
              "type": "string",
              "paramType": "form"
            }
          ]
quantity = [
            {
              "name": "quantity",
              "description": "quantity to add cart",
              "required": True,
              "type": "sting",
              "paramType": "form"
            }
]
quantity = product + quantity