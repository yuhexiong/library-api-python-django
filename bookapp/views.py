from datetime import timedelta
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from enum import Enum
from .models import Author, Book, BookType, Borrow, Reader, Report, User

maxBorrowTimes = 3  # 最多續借2次
BorrowDays = 30  # 一次借書30天

# error code
class LibraryError(Enum):
    SUCCESSFUL = 0
    INVALID_API = 117
    INVALID_PARAMETER = 118
    INSUFFICIENT_PARAMETER = 119
    OVER_BORROW_TIMES_LIMIT = 120



def createAndGetUser(request):
    if request.method == 'POST':  # 新增使用者
        body = json.loads(request.body)
        name = body.get('name')

        if not name:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        newUser = User(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            name=name
        )
        newUser.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newUser.id}}, safe=False)

    elif request.method == 'GET':  # 取得所有使用者
        users = list(User.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'users': users}}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def deleteUser(request, userId):
    if request.method == 'DELETE':  # 刪除使用者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        User.objects.filter(id=userId).update(updateAt=currentDateTime, status=9)
        Author.objects.filter(user_id=userId).update(updateAt=currentDateTime, status=9)
        Reader.objects.filter(user_id=userId).update(updateAt=currentDateTime, status=9)

        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'userId {userId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def createAndGetAuthor(request):
    if request.method == 'POST':  # 新增作者
        body = json.loads(request.body)
        name = body.get('name')
        userId = body.get('userId')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not userId and not name:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide userId or name'}, status=HTTPStatus.NOT_FOUND)

        if userId:
            pass
        else:  # no userId then create user by name
            InsertUserResult = createAndGetUser(request)
            userId = json.loads(InsertUserResult.content.decode("utf-8"))["id"]

        try:
            user = User.objects.get(id=userId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"userId {userId} not found"}, status=HTTPStatus.NOT_FOUND)
        
        newAuthor = Author(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            user=user,
            publishTimes=0
        )
        newAuthor.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newAuthor.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有作者
        authors = list(Author.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'authors': authors }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def deleteAuthor(request, authorId):
    if request.method == 'DELETE':  # 刪除作者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Author.objects.filter(id=authorId).update(updateAt=currentDateTime, status=9)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'authorId {authorId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def createAndGetReader(request):  # 新增讀者
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        userId = body.get('userId')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not userId and not name:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide userId or name'}, status=HTTPStatus.NOT_FOUND)

        if userId:
            pass
        else:  # no userId then create user by name
            InsertUserResult = createAndGetUser(request)
            userId = json.loads(InsertUserResult.content.decode("utf-8"))["id"]

        try:
            user = User.objects.get(id=userId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"userId {userId} not found"}, status=HTTPStatus.NOT_FOUND)

        newReader = Reader(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            user=user,
            borrowTimes=0,
            violationTimes=0,
        )
        newReader.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newReader.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有讀者
        readers = list(Reader.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def deleteReader(request, readerId):
    if request.method == 'DELETE':  # 刪除作者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Reader.objects.filter(id=readerId).update(updateAt=currentDateTime, status=9)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'readerId {readerId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def createAndGetBookType(request):  # 新增書本類型
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        newBookType = BookType(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            name=name,
        )
        newBookType.save()

        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newBookType.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有書本類型
        bookTypes = list(BookType.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'bookTypes': bookTypes }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def deleteBookType(request, bookTypeId):
    if request.method == 'DELETE':  # 刪除書本類型
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        BookType.objects.filter(id=bookTypeId).update(updateAt=currentDateTime, status=9)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'bookTypeId {bookTypeId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def createAndGetBook(request):  # 新增書本
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        bookTypeId = body.get('bookTypeId')
        publishAt = body.get('publishAt')
        authorId = body.get('authorId')
        location = body.get('location')

        if not name:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        if not bookTypeId:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide bookTypeId'}, status=HTTPStatus.NOT_FOUND)

        if not publishAt:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide publishAt'}, status=HTTPStatus.NOT_FOUND)

        if not authorId:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide authorId'}, status=HTTPStatus.NOT_FOUND)

        if not location:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide location'}, status=HTTPStatus.NOT_FOUND)

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            bookType = BookType.objects.get(id=bookTypeId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"bookTypeId {bookTypeId} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            author = Author.objects.get(id=authorId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"authorId {authorId} not found"}, status=HTTPStatus.NOT_FOUND)

        Author.objects.filter(id=authorId).update(updateAt=currentDateTime, publishTimes=author.publishTimes+1)

        newBook = Book(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            name=name,
            bookType=bookType,
            publishAt=publishAt,
            author=author,
            location=location,
        )
        newBook.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newBook.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有書本
        books = list(Book.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'books': books }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def deleteBook(request, bookId):
    if request.method == 'DELETE':  # 刪除書本
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            book = Book.objects.get(id=bookId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"bookId {bookId} not found"}, status=HTTPStatus.NOT_FOUND)

        Author.objects.filter(id=book.author.id).update(updateAt=currentDateTime, publishTimes=book.author.publishTimes-1)
        Book.objects.filter(id=bookId).update(updateAt=currentDateTime, status=9)

        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'bookId {bookId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def borrowBook(request, bookId, readerId):  # 借書
    if request.method == 'POST':
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            book = Book.objects.get(id=bookId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"bookId {bookId} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            reader = Reader.objects.get(id=readerId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"readerId {readerId} not found"}, status=HTTPStatus.NOT_FOUND)

        Book.objects.filter(id=readerId).update(updateAt=currentDateTime, status=1)
        Reader.objects.filter(id=readerId).update(updateAt=currentDateTime, borrowTimes=reader.borrowTimes+1)

        newBorrow = Borrow(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            book=book,
            reader=reader,
            borrowAt=currentDateTime,
            times=1,
        )
        newBorrow.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newBorrow.id }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def renewBook(request, bookId, readerId):  # 續借
    if request.method == 'POST':
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            borrow = Borrow.objects.get(book_id=bookId, reader_id=readerId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"borrow of bookId {bookId}, readerId {readerId} not found"}, status=HTTPStatus.NOT_FOUND)

        if borrow.times >= maxBorrowTimes: 
            return JsonResponse({'code': LibraryError.OVER_BORROW_TIMES_LIMIT.value, 'message': 'Can not borrow it any more'}, status=HTTPStatus.NOT_FOUND)

        Borrow.objects.filter(id=borrow.id).update(updateAt=currentDateTime, times=borrow.times+1)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': 'book renewal successful'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def returnBook(request, bookId, readerId):  # 續借
    if request.method == 'POST':
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            borrow = Borrow.objects.get(book_id=bookId, reader_id=readerId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"borrow of bookId {bookId}, readerId {readerId} not found"}, status=HTTPStatus.NOT_FOUND)

        if borrow.borrowAt + timedelta(days=borrow.times*BorrowDays) < now:  # 逾期還書
            reader = Reader.objects.get(id=readerId)
            Reader.objects.filter(id=readerId).update(updateAt=currentDateTime, violationTimes=reader.violationTimes+1)

        Borrow.objects.filter(id=borrow.id).update(updateAt=currentDateTime, returnAt=currentDateTime, status=9)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': 'book return successful'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def createAndGetReport(request):
    if request.method == 'POST':  # 新增心得
        body = json.loads(request.body)
        bookId = body.get('bookId')
        readerId = body.get('readerId')
        content = body.get('content')

        if not bookId:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide bookId'}, status=HTTPStatus.NOT_FOUND)

        if not readerId:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide readerId'}, status=HTTPStatus.NOT_FOUND)

        if not content:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide content'}, status=HTTPStatus.NOT_FOUND)

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            book = Book.objects.get(id=bookId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"bookId {bookId} not found"}, status=HTTPStatus.NOT_FOUND)

        try:
            reader = Reader.objects.get(id=readerId, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryError.INVALID_PARAMETER.value, 'error': f"readerId {readerId} not found"}, status=HTTPStatus.NOT_FOUND)

        newReport = Report(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            book=book,
            reader=reader,
            content=content
        )
        newReport.save()
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'id': newReport.id }}, safe=False)

    elif request.method == 'GET':  # 取得所有心得
        reports = list(Report.objects.filter(status=0).values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'reports': reports }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def updateAndDeleteReport(request, reportId):
    if request.method == 'PATCH':  # 刪除心得
        body = json.loads(request.body)
        content = body.get('content')

        if not content:
            return JsonResponse({'code': LibraryError.INSUFFICIENT_PARAMETER.value, 'message': 'should provide content'}, status=HTTPStatus.NOT_FOUND)

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Report.objects.filter(id=reportId).update(updateAt=currentDateTime, content=content)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'reportId {reportId} updated'}, safe=False)

    elif request.method == 'DELETE':  # 刪除心得
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Report.objects.filter(id=reportId).update(updateAt=currentDateTime, status=9)
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'message': f'reportId {reportId} deleted'}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def getRankOfBorrowTimes(request):
    if request.method == 'GET':  # 取得讀者借書次數排名
        readers = list(Reader.objects.all().order_by('-borrowTimes').values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)


def getRankOfViolationTimes(request):
    if request.method == 'GET':  # 取得讀者違規次數排名
        readers = list(Reader.objects.all().order_by('-violationTimes').values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)



def getRankOfPublishTimes(request):
    if request.method == 'GET':  # 取得作者出版次數排名
        authors = list(Author.objects.all().order_by('-publishTimes').values())
        return JsonResponse({'code': LibraryError.SUCCESSFUL.value, 'result': {'authors': authors }}, safe=False)

    else:
        return JsonResponse({'code': LibraryError.INVALID_API.value, 'message': 'Invalid api'}, status=HTTPStatus.BAD_REQUEST)