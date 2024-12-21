import json
from django.http import JsonResponse
from http import HTTPStatus
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Reader, User
from bookapp.views import user as userView


@method_required(['POST', 'GET'])
def create_and_get_reader(request):  # 新增讀者
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        user_id = body.get('user_id')


        if not user_id and not name:
            return JsonResponse({'code': LibraryCode.INSUFFICIENT_PARAMETER.value, 'message': 'should provide user_id or name'}, status=HTTPStatus.NOT_FOUND)

        if not user_id:
            insert_user_result = userView.create_and_get_user(request)
            user_id = json.loads(insert_user_result.content.decode("utf-8"))["id"]

        try:
            user = User.objects.get(id=user_id, status=0)
        except ObjectDoesNotExist:
            return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"user_id {user_id} not found"}, status=HTTPStatus.NOT_FOUND)

        current_datetime = get_current_datetime()
        new_reader = Reader(
            create_at=current_datetime,
            update_at=current_datetime,
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
    current_datetime = get_current_datetime()

    Reader.objects.filter(id=reader_id).update(update_at=current_datetime, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': f'reader_id {reader_id} deleted'}, safe=False)
