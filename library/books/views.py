from datetime import timedelta
import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Author, Book, BookType, Borrow, Reader, Report, User

maxBorrowTimes = 3  # 最多續借2次
BorrowDays = 30  # 一次借書30天


@csrf_exempt
def createAndGetUser(request):
    if request.method == 'POST':  # 新增使用者
        body = json.loads(request.body)
        name = body.get('name')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            return HttpResponseBadRequest('should provide name')

        newUser = User(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            name=name
        )
        newUser.save()

        return JsonResponse(data={'id': newUser.id}, safe=False)
    elif request.method == 'GET':  # 取得所有使用者
        users = list(User.objects.filter(status=0).values())
        return JsonResponse(data={'users': users}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def deleteUser(request, userId):
    if request.method == 'DELETE':  # 刪除使用者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        User.objects.filter(id=userId).update(updateAt=currentDateTime, status=9)
        Author.objects.filter(user_id=userId).update(updateAt=currentDateTime, status=9)
        Reader.objects.filter(user_id=userId).update(updateAt=currentDateTime, status=9)

        return JsonResponse(data={'message': f'userId {userId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def createAndGetAuthor(request):
    if request.method == 'POST':  # 新增作者
        body = json.loads(request.body)
        name = body.get('name')
        userId = body.get('userId')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not userId and not name:
            return HttpResponseBadRequest('should provide userId or name')

        if userId:
            pass
        else:  # no userId then create user by name
            InsertUserResult = createAndGetUser(request)
            userId = json.loads(InsertUserResult.content.decode("utf-8"))["id"]

        user = User.objects.get(id=userId)
        newAuthor = Author(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            user=user,
            publishTimes=0
        )
        newAuthor.save()

        return JsonResponse(data={'id': newAuthor.id}, safe=True)
    elif request.method == 'GET':  # 取得所有作者
        authors = list(Author.objects.filter(status=0).values())
        return JsonResponse(data={'authors': authors}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def deleteAuthor(request, authorId):
    if request.method == 'DELETE':  # 刪除作者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Author.objects.filter(id=authorId).update(updateAt=currentDateTime, status=9)
        return JsonResponse(data={'message': f'authorId {authorId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def createAndGetReader(request):  # 新增讀者
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        userId = body.get('userId')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not userId and not name:
            return HttpResponseBadRequest('should provide userId or name')

        if userId:
            pass
        else:  # no userId then create user by name
            InsertUserResult = createAndGetUser(request)
            userId = json.loads(InsertUserResult.content.decode("utf-8"))["id"]

        user = User.objects.get(id=userId)
        newReader = Reader(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            user=user,
            borrowTimes=0,
            violationTimes=0,
        )
        newReader.save()

        return JsonResponse(data={'id': newReader.id}, safe=True)
    elif request.method == 'GET':  # 取得所有讀者
        readers = list(Reader.objects.filter(status=0).values())
        return JsonResponse(data={'readers': readers}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def deleteReader(request, readerId):
    if request.method == 'DELETE':  # 刪除作者
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Reader.objects.filter(id=readerId).update(updateAt=currentDateTime, status=9)
        return JsonResponse(data={'message': f'readerId {readerId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def createAndGetBookType(request):  # 新增書本類型
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            return HttpResponseBadRequest('should provide name')

        newBookType = BookType(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            name=name,
        )
        newBookType.save()

        return JsonResponse(data={'id': newBookType.id}, safe=True)
    elif request.method == 'GET':  # 取得所有書本類型
        bookTypes = list(BookType.objects.filter(status=0).values())
        return JsonResponse(data={'bookTypes': bookTypes}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def deleteBookType(request, bookTypeId):
    if request.method == 'DELETE':  # 刪除書本類型
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        BookType.objects.filter(id=bookTypeId).update(updateAt=currentDateTime, status=9)
        return JsonResponse(data={'message': f'bookTypeId {bookTypeId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def createAndGetBook(request):  # 新增書本
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        bookTypeId = body.get('bookTypeId')
        publishAt = body.get('publishAt')
        authorId = body.get('authorId')
        location = body.get('location')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not name:
            return HttpResponseBadRequest('should provide name')

        if not bookTypeId:
            return HttpResponseBadRequest('should provide bookTypeId')

        if not publishAt:
            return HttpResponseBadRequest('should provide publishAt')

        if not authorId:
            return HttpResponseBadRequest('should provide authorId')

        if not location:
            return HttpResponseBadRequest('should provide location')

        bookType = BookType.objects.get(id=bookTypeId)
        author = Author.objects.get(id=authorId)

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

        return JsonResponse(data={'id': newBook.id}, safe=True)
    elif request.method == 'GET':  # 取得所有書本
        books = list(Book.objects.filter(status=0).values())
        return JsonResponse(data={'books': books}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def deleteBook(request, bookId):
    if request.method == 'DELETE':  # 刪除書本
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        book = Book.objects.get(id=bookId)

        Author.objects.filter(id=book.author.id).update(updateAt=currentDateTime, publishTimes=book.author.publishTimes-1)
        Book.objects.filter(id=bookId).update(updateAt=currentDateTime, status=9)

        return JsonResponse(data={'message': f'bookId {bookId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def borrowBook(request, bookId, readerId):  # 借書
    if request.method == 'POST':

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        book = Book.objects.get(id=bookId, status=0)
        reader = Reader.objects.get(id=readerId)

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

        return JsonResponse(data={'id': newBorrow.id}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def renewBook(request, bookId, readerId):  # 續借
    if request.method == 'POST':

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        borrow = Borrow.objects.get(book_id=bookId, reader_id=readerId, status=0)
        if borrow.times >= maxBorrowTimes:
            return HttpResponseBadRequest('Can not borrow it any more.')

        Borrow.objects.filter(id=borrow.id).update(updateAt=currentDateTime, times=borrow.times+1)

        return JsonResponse(data={'message': 'book renewal successful'}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def returnBook(request, bookId, readerId):  # 續借
    if request.method == 'POST':

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        borrow = Borrow.objects.get(book_id=bookId, reader_id=readerId, status=0)
        if borrow.borrowAt + timedelta(days=borrow.times*BorrowDays) < now:  # 逾期還書
            reader = Reader.objects.get(id=readerId)
            Reader.objects.filter(id=readerId).update(updateAt=currentDateTime, violationTimes=reader.violationTimes+1)

        Borrow.objects.filter(id=borrow.id).update(updateAt=currentDateTime, returnAt=currentDateTime, status=9)

        return JsonResponse(data={'message': 'book return successful'}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def createAndGetReport(request):
    if request.method == 'POST':  # 新增心得
        body = json.loads(request.body)
        bookId = body.get('bookId')
        readerId = body.get('readerId')
        content = body.get('content')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not bookId:
            return HttpResponseBadRequest('should provide bookId')

        if not readerId:
            return HttpResponseBadRequest('should provide readerId')

        if not content:
            return HttpResponseBadRequest('should provide content')

        book = Book.objects.get(id=bookId)
        reader = Reader.objects.get(id=readerId)

        newReport = Report(
            createAt=currentDateTime,
            updateAt=currentDateTime,
            status=0,
            book=book,
            reader=reader,
            content=content
        )
        newReport.save()

        return JsonResponse(data={'id': newReport.id}, safe=True)
    elif request.method == 'GET':  # 取得所有心得
        reports = list(Report.objects.filter(status=0).values())
        return JsonResponse(data={'reports': reports}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


@csrf_exempt
def updateAndDeleteReport(request, reportId):
    if request.method == 'PATCH':  # 刪除心得
        body = json.loads(request.body)
        content = body.get('content')

        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        if not content:
            return HttpResponseBadRequest('should provide content')

        Report.objects.filter(id=reportId).update(updateAt=currentDateTime, content=content)
        return JsonResponse(data={'message': f'reportId {reportId} updated'}, safe=False)
    elif request.method == 'DELETE':  # 刪除心得
        now = timezone.now()
        currentDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

        Report.objects.filter(id=reportId).update(updateAt=currentDateTime, status=9)
        return JsonResponse(data={'message': f'reportId {reportId} deleted'}, safe=False)
    else:
        return HttpResponseBadRequest('Invalid api')


def getRankOfBorrowTimes(request):
    if request.method == 'GET':  # 取得讀者借書次數排名
        readers = list(Reader.objects.all().order_by('-borrowTimes').values())
        return JsonResponse(data={'readers': readers}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')


def getRankOfViolationTimes(request):
    if request.method == 'GET':  # 取得讀者違規次數排名
        readers = list(Reader.objects.all().order_by('-violationTimes').values())
        return JsonResponse(data={'readers': readers}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')


def getRankOfPublishTimes(request):
    if request.method == 'GET':  # 取得作者出版次數排名
        authors = list(Author.objects.all().order_by('-publishTimes').values())
        return JsonResponse(data={'authors': authors}, safe=True)
    else:
        return HttpResponseBadRequest('Invalid api')