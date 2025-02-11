import json

from django.core.exceptions import ObjectDoesNotExist

from bookapp.models import Reader, User
from bookapp.responses import LibraryError, LibraryResponse
from bookapp.utils import get_current_datetime, method_required
from bookapp.views import user as user_view


@method_required(['POST', 'GET'])
def create_and_get_reader(request):  # 新增讀者
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        user_id = body.get('user_id')

        if not user_id and not name:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide user_id or name."
            )

        if not user_id:
            insert_user_result = user_view.create_and_get_user(request)
            user_id = json.loads(
                insert_user_result.content.decode("utf-8"))["id"]

        try:
            user = User.objects.get(id=user_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"user_id {user_id} not found"
            )

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
        return LibraryResponse.to_json_response({'id': new_reader.id})

    elif request.method == 'GET':  # 取得所有讀者
        readers = list(Reader.objects.filter(status=0).values())

        return LibraryResponse.to_json_response({'readers': readers})


@method_required(['DELETE'])
def delete_reader(request, reader_id):  # 刪除讀者
    current_datetime = get_current_datetime()

    Reader.objects.filter(id=reader_id).update(
        update_at=current_datetime, status=9)

    return LibraryResponse.to_json_response({})
