import json
from django.http import JsonResponse
from http import HTTPStatus
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import BookType



@method_required(['POST', 'GET'])
def create_and_get_book_type(request):  # 新增書本類型
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')

        if not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()
        new_book_type = BookType(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            name=name,
        )
        new_book_type.save()

        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_book_type.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有書本類型
        book_types = list(BookType.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'book_types': book_types}}, safe=False)


@method_required(['DELETE'])
def delete_book_type(request, book_type_id): # 刪除書本類型
    current_datetime = get_current_datetime()

    BookType.objects.filter(id=book_type_id).update(update_at=current_datetime, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'book_type_id {book_type_id} deleted'}, safe=False)

