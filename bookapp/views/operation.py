from datetime import timedelta
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from bookapp.errors import LibraryCode
from bookapp.settings import BORROW_DAYS, MAX_BORROW_TIMES
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Book, Borrow, Reader


@method_required(['POST'])
def borrow_book(request, book_id, reader_id):  # 借書
    try:
        book = Book.objects.get(id=book_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"book_id {book_id} not found"}, status=HTTPStatus.NOT_FOUND)

    try:
        reader = Reader.objects.get(id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    current_datetime = get_current_datetime()
    Book.objects.filter(id=book_id).update(update_at=current_datetime, status=1)
    Reader.objects.filter(id=reader_id).update(update_at=current_datetime, borrow_times=reader.borrow_times+1)

    new_borrow = Borrow(
        create_at=current_datetime,
        update_at=current_datetime,
        status=0,
        book=book,
        reader=reader,
        borrow_at=current_datetime,
        times=1,
    )
    new_borrow.save()
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'id': new_borrow.id }}, safe=False)



@method_required(['POST'])
def renew_book(request, book_id, reader_id):  # 續借
    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    if borrow.times >= MAX_BORROW_TIMES: 
        return JsonResponse({'code': LibraryCode.OVER_BORROW_TIMES_LIMIT.value, 'message': 'Can not borrow it any more'}, status=HTTPStatus.NOT_FOUND)

    current_datetime = get_current_datetime()
    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, times=borrow.times+1)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': 'book renewal successful'}, safe=False)


@method_required(['POST'])
def return_book(request, book_id, reader_id):  # 還書
    current_datetime = get_current_datetime()

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return JsonResponse({'code': LibraryCode.INVALID_PARAMETER.value, 'error': f"borrow of book_id {book_id}, reader_id {reader_id} not found"}, status=HTTPStatus.NOT_FOUND)

    if borrow.borrow_at + timedelta(days=borrow.times * BORROW_DAYS) < timezone.now():  # 逾期還書
        reader = Reader.objects.get(id=reader_id)
        Reader.objects.filter(id=reader_id).update(update_at=current_datetime, violation_times=reader.violation_times + 1)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, return_at=current_datetime, status=9)
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'message': 'book return successful'}, safe=False)

