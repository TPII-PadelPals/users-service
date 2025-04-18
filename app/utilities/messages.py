from fastapi import status

# Common responses
NOT_ENOUGH_PERMISSIONS = {
    status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
}

# Item responses
ITEM_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Item not found"}}
ITEM_RESPONSES = {**ITEM_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}

# User responses
POST_USERS_RESPONSES = {
    status.HTTP_201_CREATED: {"description": "User created"},
    status.HTTP_409_CONFLICT: {"description": "Email or phone already exists"},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid email format."},
}

GET_USERS_RESPONSES = {status.HTTP_200_OK: {"description": "Users recovered"}}
GET_USER_RESPONSES = {
    status.HTTP_200_OK: {"description": "User recovered"},
    status.HTTP_404_NOT_FOUND: {"description": "User not found"},
}

POST_PUBLIC_KEY_RESPONSES = {
    status.HTTP_201_CREATED: {"description": "User Public key saved"}
}

POST_TOKEN_RESPONSES = {status.HTTP_201_CREATED: {"description": "Token created"}}

GET_VALIDATE_TOKEN_RESPONSES = {
    status.HTTP_200_OK: {"description": "Valid token"},
    status.HTTP_409_CONFLICT: {"description": "Invalid token"},
    status.HTTP_404_NOT_FOUND: {"description": "User not found"},
}
