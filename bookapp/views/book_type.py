import json

from bookapp.models import BookType
from bookapp.responses import LibraryError, LibraryResponse
from bookapp.utils import get_current_datetime, method_required


@method_required(['POST', 'GET'])
def create_and_get_book_type(request):  # 新增書本類型
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')

        if not name:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide name."
            )

        current_datetime = get_current_datetime()
        new_book_type = BookType(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            name=name,
        )
        new_book_type.save()

        return LibraryResponse.to_json_response({'id': new_book_type.id})

    elif request.method == 'GET':  # 取得所有書本類型
        book_types = list(BookType.objects.filter(status=0).values())
        return LibraryResponse.to_json_response({'book_types': book_types})


@method_required(['DELETE'])
def delete_book_type(request, book_type_id):  # 刪除書本類型
    current_datetime = get_current_datetime()

    BookType.objects.filter(id=book_type_id).update(
        update_at=current_datetime, status=9)
    return LibraryResponse.to_json_response({})
