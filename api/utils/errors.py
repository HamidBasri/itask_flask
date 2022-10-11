SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
ALREADY_EXIST = ({"message": "Already exists."}, 409)
UNAUTHORIZED = ({"message": "Wrong credentials."}, 401)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
HEADER_NOT_FOUND = ({"message": "Header does not exists."}, 999)
PERMISSION_DENIED_403 = ({"message": "Forbidden."}, 403)

INVALID_TOKEN = (
    {"message": "Invalid token."},
    401,
)
EXPIRED_TOKEN = (
    {"message": "Expired token."},
    401,
)


HTTP_UNPROCESSABLE_ENTITY_422 = 422
HTTP_SUCCESS_200 = 200
HTTP_NOT_FOUND_404 = 404
