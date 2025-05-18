from fastapi import HTTPException, status


class NotAuthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado"
        )


class NotEnoughPermissionsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes"
        )


class NotFoundException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"No se encontró el {item.lower()}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotUniqueException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} ya existe"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidEmailHttpException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de email inválido.",
        )


class ExternalServiceException(HTTPException):
    def __init__(self, service_name: str, detail: str) -> None:
        detail = f"EXT_SERVICE:{service_name}:{detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class TokenExpiredSignatureException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
        )


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )


class LoginInvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )
