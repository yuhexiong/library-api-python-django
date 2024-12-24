import json
from django.http import JsonResponse
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Author, Book, BookType



@method_required(['POST', 'GET'])
def create_and_get_book(request):  # 新增書本
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        book_type_id = body.get('book_type_id')
        publish_at = body.get('publish_at')
        author_id = body.get('author_id')
        location = body.get('location')

        if not all([name, book_type_id, publish_at, author_id, location]):
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'Missing required parameters'}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()

        try:
            book_type = BookType.objects.get(id=book_type_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_type_id {book_type_id} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            author = Author.objects.get(id=author_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"author_id {author_id} not found"}, status=HTTPStatus.NOT_FOUND)

        Author.objects.filter(id=author_id).update(update_at=current_datetime, publish_times=author.publish_times + 1)

        new_book = Book(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            name=name,
            book_type=book_type,
            publish_at=publish_at,
            author=author,
            location=location,
        )
        new_book.save()
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_book.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有書本
        books = list(Book.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'books': books}}, safe=False)


@method_required(['DELETE'])
def delete_book(request, book_id): # 刪除書本
    current_datetime = get_current_datetime()

    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

    Author.objects.filter(id=book.author.id).update(update_at=current_datetime, publish_times=book.author.publish_times-1)
    Book.objects.filter(id=book_id).update(update_at=current_datetime, status=9)

    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'book_id {book_id} deleted'}, safe=False)

