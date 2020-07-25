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
              "paramType": "query"
            }
          ]
token = [
        {
              "name": "token",
              "description": "enter token to register",
              "required": True,
              "type": "string",
              "paramType": "path"
            }
]
sort = [
            {
              "name": "sort",
              "description": "enter sort value according to price",
              "required": True,
              "type": "string",
              "paramType": "query"
            }
      ]
jwt = [
        {
          "name": "Authorization",
          "description": "jwt token for the Authorization",
          "required": True,
          "type": "string",
          "paramType": "header"
        }
      ]
product = [
            {
              "name": "Authorization",
              "description": "jwt token for the Authorization",
              "required": True,
              "type": "string",
              "paramType": "header"
            },{
              "name": "productid",
              "description": "product id to add ",
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

order = [
        {
              "name": "name",
              "description": "name of the customer",
              "required": True,
              "type": "sting",
              "paramType": "form"
            },
            {
              "name": "mobilenumber",
              "description": "mobilenumber of the customer",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "address",
              "description": "address for the order",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "pincode",
              "description": "pincode for the order",
              "required": True,
              "type": "string",
              "paramType": "form"
            }
]
order  = jwt + order