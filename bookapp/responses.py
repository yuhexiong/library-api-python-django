from http import HTTPStatus

from django.http import JsonResponse


class LibraryResponse:
    @staticmethod
    def to_json_response(result: dict = {}, status: int = 200):
        response_data = {
            "code": 0,
            "result": result
        }
        return JsonResponse(response_data, status=status)


class LibraryError:
    INVALID_API = {"code": 1001, "message": "Invalid API"}
    INVALID_PARAMETER = {"code": 1002, "message": "Invalid Parameter"}
    INSUFFICIENT_PARAMETER = {"code": 1003,
                              "message": "Insufficient Parameter"}
    OVER_BORROW_TIMES_LIMIT = {"code": 1004,
                               "message": "Over Borrow Times Limit"}

    @staticmethod
    def to_json_response(error: dict, message: str = "", status: int = HTTPStatus.BAD_REQUEST):
        response_data = {
            "code": error["code"],
            "message": f"[{error['message']}] {message}"
        }
        return JsonResponse(response_data, status=status)
