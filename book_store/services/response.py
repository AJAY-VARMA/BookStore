login_response = {
    401 : {
        "message" : "USER_NAME OR PASSWORD INCORRECT",
        "status" : 401
    },
    400 : {
        "message" : "PLEASE ENTER USERNAME[4-25] AND PASSWORD[8-50] CHARACTERS",
        "status" :400
    },
    411:{
        "message" : "PLEASE VERIFY YOUR EMAIL AND LINK THE LINK FOR REGISTRATION",
        "status" :411
    },
    413:{
        "message" : "PLEASE LOGIN FIRST",
        "status" :413
    }
}

registration_response = {
    200 : {
        "message" : "VERIFICATION LINK SEND TO YOUR MAIL",
        "status" : 200
    },
    400 : {
        "message" : "PLEASE ENTER USERNAME[4-25] AND PASSWORD[8-50] EMAIL[6-50] CHARACTERS",
        "status" :400
    },
    409 : {
        "message" : "USER_NAME OR PASSWORD ALREADY EXISTS",
        "status" : 409
    },
    "success": {
        "message" : "REGISTRATION SUCCESSFUL PLEASE LOGIN",
        "status" : 200
    }
}

response = {
    "added": {
        "message" : "PRODUCT IS ADDED",
        "status" : 200
    },
    "search":{
        "message" : "ENTER PROPER SEARCH VALUE",
        "status" : 400
    },
    "sort" : {
        "message" : "ENTER PROPER SORT VALUE",
        "status" : 400
    },
    400 : {
        "message" : "PRODUCT YOU GIVEN IS NOT AVAILABLE",
        "status" : 400
    },
    200 : {
        "message" : "PRODUCT IS NOT AVAILABLE RIGHT NOW",
        "status" : 200
    },
    "deleted" : {
        "message" :"PRODUCT YOU GIVEN IS DELETED",
        "status" : 200
    },
    "order" :{
        "message" : "ADDED ADDRESS TO DATABASE SUCCESSFULLY ",
        "status" : 200
    },
    "checkout" : {
        "message" : "ORDER PLACED SUCCESSFULLY ",
        "status" : 200
    }
}

sql = {500 : 'MYSQL CONNECTION OR SYNTAX IS IMPROPER'}
redis_error = {500 : 'REDIS CONNECTION OR KEY IS IMPROPER'}
mail_error = {500 : 'ERROR IN MY MAIL SERVICE'}
update_error = {400 : "ENTER PROPER VALUE FOR QUANTITY OR PRODUCTS ID"}
twilio = {500 : "CREDENTIALS ARE IMPROPER"}
