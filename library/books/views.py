import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Author, BookType, Reader, User


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

        User.objects.filter(id=userId).update(
            updateAt=currentDateTime, status=9)
        Author.objects.filter(user_id=userId).update(
            updateAt=currentDateTime, status=9)
        Reader.objects.filter(user_id=userId).update(
            updateAt=currentDateTime, status=9)

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

        Author.objects.filter(id=authorId).update(
            updateAt=currentDateTime, status=9)

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

        Reader.objects.filter(id=readerId).update(
            updateAt=currentDateTime, status=9)

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

        BookType.objects.filter(id=bookTypeId).update(
            updateAt=currentDateTime, status=9)

        return JsonResponse(data={'message': f'bookTypeId {bookTypeId} deleted'}, safe=False)

    else:
        return HttpResponseBadRequest('Invalid api')
