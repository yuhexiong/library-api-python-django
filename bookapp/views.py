from datetime import timedelta
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from .models import Author, Book, BookType, Borrow, Reader, Report, User

max_borrow_times = 3  # 最多續借2次
borrow_days = 30  # 一次借書30天



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



@method_required(['POST'])
def borrow_book(request, book_id, reader_id):  # 借書
    current_datetime = get_current_datetime()

    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

    try:
        reader = Reader.objects.get(id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    Book.objects.filter(id=book_id).update(update_at=current_datetime, status=1)
    Reader.objects.filter(id=reader_id).update(update_at=current_datetime, borrow_times=reader.borrow_times+1)

    new_borrow = Borrow(
        create_at=current_datetime,
        update_at=current_datetime,
        status=0,
        book=book,
        reader=reader,
        borrow_at=current_datetime,
        times=1,
    )
    new_borrow.save()
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_borrow.id }}, safe=False)



@method_required(['POST'])
def renew_book(request, book_id, reader_id):  # 續借
    current_datetime = get_current_datetime()

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    if borrow.times >= max_borrow_times: 
        return JsonResponse({'code': LibraryCode.OVER_BORROW_TIMES_LIMIT.value, 'message': 'Can not borrow it any more'}, status=HTTPStatus.NOT_FOUND)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, times=borrow.times+1)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': 'book renewal successful'}, safe=False)


@method_required(['POST'])
def return_book(request, book_id, reader_id):  # 還書
    current_datetime = get_current_datetime()

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    now = timezone.now()
    if borrow.borrow_at + timedelta(days=borrow.times * borrow_days) < now:  # 逾期還書
        reader = Reader.objects.get(id=reader_id)
        Reader.objects.filter(id=reader_id).update(update_at=current_datetime, violation_times=reader.violation_times + 1)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, return_at=current_datetime, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': 'book return successful'}, safe=False)



@method_required(['POST', 'GET'])
def create_and_get_report(request):
    if request.method == 'POST':  # 新增心得
        body = json.loads(request.body)
        book_id = body.get('book_id')
        reader_id = body.get('reader_id')
        content = body.get('content')

        if not book_id:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide book_id'}, status=HTTPStatus.NOT_FOUND)

        if not reader_id:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide reader_id'}, status=HTTPStatus.NOT_FOUND)

        if not content:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide content'}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()

        try:
            book = Book.objects.get(id=book_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            reader = Reader.objects.get(id=reader_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

        new_report = Report(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            book=book,
            reader=reader,
            content=content
        )
        new_report.save()
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_report.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有心得
        reports = list(Report.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'reports': reports }}, safe=False)


@method_required(['PATCH', 'DELETE'])
def update_and_delete_report(request, report_id):
    if request.method == 'PATCH':  # 修改心得
        body = json.loads(request.body)
        content = body.get('content')

        if not content:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide content'}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()

        Report.objects.filter(id=report_id).update(update_at=current_datetime, content=content)
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'report_id {report_id} updated'}, safe=False)

    elif request.method == 'DELETE':  # 刪除心得
        current_datetime = get_current_datetime()

        Report.objects.filter(id=report_id).update(update_at=current_datetime, status=9)
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'report_id {report_id} deleted'}, safe=False)


@method_required(['GET'])
def get_rank_of_borrow_times(request): # 取得讀者借書次數排名
    readers = list(Reader.objects.all().order_by('-borrow_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)


@method_required(['GET'])
def get_rank_of_violation_times(request): # 取得讀者違規次數排名
    readers = list(Reader.objects.all().order_by('-violation_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)


@method_required(['GET'])
def get_rank_of_publish_times(request): # 取得作者出版次數排名
    authors = list(Author.objects.all().order_by('-publish_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'authors': authors }}, safe=False)

