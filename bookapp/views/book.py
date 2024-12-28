import json
from django.core.exceptions import ObjectDoesNotExist
from bookapp.responses import LibraryError, LibraryResponse
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
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Missing required parameters."
            )

        current_datetime = get_current_datetime()

        try:
            book_type = BookType.objects.get(id=book_type_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"book_type_id {book_type_id} not found"
            )

        try:
            author = Author.objects.get(id=author_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"author_id {author_id} not found"
            )

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
        return LibraryResponse.to_json_response({'id': new_book.id})

    elif request.method == 'GET':  # 取得所有書本
        books = list(Book.objects.filter(status=0).values())
        return LibraryResponse.to_json_response({'books': books})


@method_required(['DELETE'])
def delete_book(request, book_id): # 刪除書本
    current_datetime = get_current_datetime()

    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return LibraryError.to_json_response(
            LibraryError.INVALID_PARAMETER,
            f"book_id {book_id} not found"
        )

    Author.objects.filter(id=book.author.id).update(update_at=current_datetime, publish_times=book.author.publish_times-1)
    Book.objects.filter(id=book_id).update(update_at=current_datetime, status=9)

    return LibraryResponse.to_json_response({})

