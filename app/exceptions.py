from fastapi import HTTPException, status


class UserException(HTTPException):
    def __init__(self, status_code: int, detail: str, code: str = "USER_ERROR"):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)


class BookingException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, code: str = "BOOKING_ERROR"
    ):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)


class HotelException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, code: str = "HOTEL_ERROR"
    ):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist",
            code="USER_ALREADY_EXISTS",
        )


class IncorrectEmailorPasswordException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            code="INVALID_CREDENTIALS",
        )


class TokenExpiredException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            code="TOKEN_EXPIRED",
        )


class TokenAbsentException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token absent",
            code="TOKEN_ABSENT",
        )


class IncorrectTokenFormatException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token format",
            code="TOKEN_INCORRECT_FORMAT",
        )


class UserIsNotPresentException(UserException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error",
        )


class RoomCannotBeBookedException(BookingException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="No rooms left",
        )


class HotelNotAvailableException(BookingException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hotel is not available",
        )
