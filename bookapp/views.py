from datetime import timedelta
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.utils import method_required
from .models import Author, Book, BookType, Borrow, Reader, Report, User

max_borrow_times = 3  # 最多續借2次
borrow_days = 30  # 一次借書30天

@method_required(['POST', 'GET'])
def create_and_get_user(request):
    if request.method == 'POST':  # 新增使用者
        body = json.loads(request.body)
        name = body.get('name')

        if not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        now = timezone.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        new_user = User(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            name=name
        )
        new_user.save()
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_user.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有使用者
        users = list(User.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'users': users}}, safe=False)

@method_required(['DELETE'])
def delete_user(request, user_id): # 刪除使用者
    now = timezone.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    User.objects.filter(id=user_id).update(update_at=current_datetime, status=9)
    Author.objects.filter(user_id=user_id).update(update_at=current_datetime, status=9)
    Reader.objects.filter(user_id=user_id).update(update_at=current_datetime, status=9)

    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'user_id {user_id} deleted'}, safe=False)


@method_required(['POST', 'GET'])
def create_and_get_author(request):
    if request.method == 'POST':  # 新增作者
        body = json.loads(request.body)
        name = body.get('name')
        user_id = body.get('user_id')

        now = timezone.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not user_id and not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide user_id or name'}, status=HTTPStatus.NOT_FOUND)

        if user_id:
            pass
        else:  # no user_id then create user by name
            insert_user_result = create_and_get_user(request)
            user_id = json.loads(insert_user_result.content.decode("utf-8"))['result']['id']

        try:
            user = User.objects.get(id=user_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f'user_id {user_id} not found'}, status=HTTPStatus.NOT_FOUND)
        
        new_author = Author(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            user=user,
            publish_times=0
        )
        new_author.save()
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_author.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有作者
        authors = list(Author.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'authors': authors}}, safe=False)


@method_required(['DELETE'])
def delete_author(request, author_id): # 刪除作者
    now = timezone.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    Author.objects.filter(id=author_id).update(update_at=current_datetime, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'author_id {author_id} deleted'}, safe=False)


@method_required(['POST', 'GET'])
def create_and_get_reader(request):  # 新增讀者
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        user_id = body.get('user_id')

        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        if not user_id and not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide user_id or name'}, status=HTTPStatus.NOT_FOUND)

        if not user_id:
            insert_user_result = create_and_get_user(request)
            user_id = json.loads(insert_user_result.content.decode("utf-8"))["id"]

        try:
            user = User.objects.get(id=user_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"user_id {user_id} not found"}, status=HTTPStatus.NOT_FOUND)

        new_reader = Reader(
            create_at=current_date_time,
            update_at=current_date_time,
            status=0,
            user=user,
            borrow_times=0,
            violation_times=0,
        )
        new_reader.save()
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_reader.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有讀者
        readers = list(Reader.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'readers': readers}}, safe=False)


@method_required(['DELETE'])
def delete_reader(request, reader_id): # 刪除讀者
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    Reader.objects.filter(id=reader_id).update(update_at=current_date_time, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'reader_id {reader_id} deleted'}, safe=False)



@method_required(['POST', 'GET'])
def create_and_get_book_type(request):  # 新增書本類型
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')

        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        new_book_type = BookType(
            create_at=current_date_time,
            update_at=current_date_time,
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
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    BookType.objects.filter(id=book_type_id).update(update_at=current_date_time, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'book_type_id {book_type_id} deleted'}, safe=False)



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

        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            book_type = BookType.objects.get(id=book_type_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_type_id {book_type_id} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            author = Author.objects.get(id=author_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"author_id {author_id} not found"}, status=HTTPStatus.NOT_FOUND)

        Author.objects.filter(id=author_id).update(update_at=current_date_time, publish_times=author.publish_times + 1)

        new_book = Book(
            create_at=current_date_time,
            update_at=current_date_time,
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
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

    Author.objects.filter(id=book.author.id).update(update_at=current_date_time, publish_times=book.author.publish_times-1)
    Book.objects.filter(id=book_id).update(update_at=current_date_time, status=9)

    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'book_id {book_id} deleted'}, safe=False)



@method_required(['POST'])
def borrow_book(request, book_id, reader_id):  # 借書
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

    try:
        reader = Reader.objects.get(id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    Book.objects.filter(id=book_id).update(update_at=current_date_time, status=1)
    Reader.objects.filter(id=reader_id).update(update_at=current_date_time, borrow_times=reader.borrow_times+1)

    new_borrow = Borrow(
        create_at=current_date_time,
        update_at=current_date_time,
        status=0,
        book=book,
        reader=reader,
        borrow_at=current_date_time,
        times=1,
    )
    new_borrow.save()
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_borrow.id }}, safe=False)



@method_required(['POST'])
def renew_book(request, book_id, reader_id):  # 續借
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    if borrow.times >= max_borrow_times: 
        return JsonResponse({'code': LibraryCode.OVER_BORROW_TIMES_LIMIT.value, 'message': 'Can not borrow it any more'}, status=HTTPStatus.NOT_FOUND)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_date_time, times=borrow.times+1)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': 'book renewal successful'}, safe=False)


@method_required(['POST'])
def return_book(request, book_id, reader_id):  # 還書
    now = timezone.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    if borrow.borrow_at + timedelta(days=borrow.times * borrow_days) < now:  # 逾期還書
        reader = Reader.objects.get(id=reader_id)
        Reader.objects.filter(id=reader_id).update(update_at=current_date_time, violation_times=reader.violation_times + 1)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_date_time, return_at=current_date_time, status=9)
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

        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            book = Book.objects.get(id=book_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            reader = Reader.objects.get(id=reader_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

        new_report = Report(
            create_at=current_date_time,
            update_at=current_date_time,
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

        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        Report.objects.filter(id=report_id).update(update_at=current_date_time, content=content)
        return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'report_id {report_id} updated'}, safe=False)

    elif request.method == 'DELETE':  # 刪除心得
        now = timezone.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        Report.objects.filter(id=report_id).update(update_at=current_date_time, status=9)
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

