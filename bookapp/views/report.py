import json
from django.http import JsonResponse
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Book, Reader, Report

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

