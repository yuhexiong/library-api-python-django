import json
from django.http import JsonResponse
from http import HTTPStatus
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Author, Reader, User


@method_required(['POST', 'GET'])
def create_and_get_user(request):
    if request.method == 'POST':  # 新增使用者
        body = json.loads(request.body)
        name = body.get('name')

        if not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide name'}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()
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
    current_datetime = get_current_datetime()
    
    User.objects.filter(id=user_id).update(update_at=current_datetime, status=9)
    Author.objects.filter(user_id=user_id).update(update_at=current_datetime, status=9)
    Reader.objects.filter(user_id=user_id).update(update_at=current_datetime, status=9)

    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'user_id {user_id} deleted'}, safe=False)
