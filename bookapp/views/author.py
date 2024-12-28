import json
from django.core.exceptions import ObjectDoesNotExist
from bookapp.responses import LibraryError, LibraryResponse
from bookapp.views import user as userView
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Author, User


@method_required(['POST', 'GET'])
def create_and_get_author(request):
    if request.method == 'POST':  # 新增作者
        body = json.loads(request.body)
        name = body.get('name')
        user_id = body.get('user_id')


        if not user_id and not name:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "should provide user_id or name."
            )

        if user_id:
            pass
        else:  # no user_id then create user by name
            insert_user_result = userView.create_and_get_user(request)
            user_id = json.loads(insert_user_result.content.decode("utf-8"))['result']['id']

        try:
            user = User.objects.get(id=user_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"user_id {user_id} not found."
            )
        
        current_datetime = get_current_datetime()
        new_author = Author(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            user=user,
            publish_times=0
        )
        new_author.save()
        return LibraryResponse.to_json_response({'id': new_author.id})

    elif request.method == 'GET':  # 取得所有作者
        authors = list(Author.objects.filter(status=0).values())
        return LibraryResponse.to_json_response({'authors': authors})


@method_required(['DELETE'])
def delete_author(request, author_id): # 刪除作者
    current_datetime = get_current_datetime()

    Author.objects.filter(id=author_id).update(update_at=current_datetime, status=9)
    return LibraryResponse.to_json_response({})
