import json

from django.core.exceptions import ObjectDoesNotExist

from bookapp.models import Book, Reader, Report
from bookapp.responses import LibraryError, LibraryResponse
from bookapp.utils import get_current_datetime, method_required


@method_required(['POST', 'GET'])
def create_and_get_report(request):
    if request.method == 'POST':  # 新增心得
        body = json.loads(request.body)
        book_id = body.get('book_id')
        reader_id = body.get('reader_id')
        content = body.get('content')

        if not book_id:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide book_id."
            )

        if not reader_id:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide reader_id."
            )

        if not content:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide content."
            )

        current_datetime = get_current_datetime()

        try:
            book = Book.objects.get(id=book_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"book_id {book_id} not found"
            )

        try:
            reader = Reader.objects.get(id=reader_id, status=0)
        except ObjectDoesNotExist:
            return LibraryError.to_json_response(
                LibraryError.INVALID_PARAMETER,
                f"reader_id {reader_id} not found"
            )

        new_report = Report(
            create_at=current_datetime,
            update_at=current_datetime,
            status=0,
            book=book,
            reader=reader,
            content=content
        )
        new_report.save()
        return LibraryResponse.to_json_response({'id': new_report.id})

    elif request.method == 'GET':  # 取得所有心得
        reports = list(Report.objects.filter(status=0).values())
        return LibraryResponse.to_json_response({'reports': reports})


@method_required(['PATCH', 'DELETE'])
def update_and_delete_report(request, report_id):
    if request.method == 'PATCH':  # 修改心得
        body = json.loads(request.body)
        content = body.get('content')

        if not content:
            return LibraryError.to_json_response(
                LibraryError.INSUFFICIENT_PARAMETER,
                "Should provide content."
            )

        current_datetime = get_current_datetime()

        Report.objects.filter(id=report_id).update(
            update_at=current_datetime, content=content)
        return LibraryResponse.to_json_response({})

    elif request.method == 'DELETE':  # 刪除心得
        current_datetime = get_current_datetime()

        Report.objects.filter(id=report_id).update(
            update_at=current_datetime, status=9)
        return LibraryResponse.to_json_response({})
