from fastapi import status

# Common responses
NOT_ENOUGH_PERMISSIONS = {
    status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
}

# Item responses
ITEM_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Item not found"}}
ITEM_RESPONSES = {**ITEM_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}

# User responses
USER_RESPONSES = {
    status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    status.HTTP_409_CONFLICT: {"description": "Email or phone already exists"},
}

# Google responses
GOOGLE_RESPONSES = {status.HTTP_400_BAD_REQUEST: {"description": "Chat ID is required"}}
