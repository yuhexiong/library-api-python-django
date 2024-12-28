from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from bookapp.responses import LibraryError, LibraryResponse
from bookapp.settings import BORROW_DAYS, MAX_BORROW_TIMES
from bookapp.utils import get_current_datetime, method_required
from bookapp.models import Book, Borrow, Reader


@method_required(['POST'])
def borrow_book(request, book_id, reader_id):  # 借書
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
    return LibraryResponse.to_json_response({'id': new_borrow.id })



@method_required(['POST'])
def renew_book(request, book_id, reader_id):  # 續借
    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return LibraryError.to_json_response(
            LibraryError.INVALID_PARAMETER,
            f"borrow of book_id {book_id}, reader_id {reader_id} not found"
        )

    if borrow.times >= MAX_BORROW_TIMES: 
        return LibraryError.to_json_response(
            LibraryError.OVER_BORROW_TIMES_LIMIT,
            "Can not borrow it any more."
        )

    current_datetime = get_current_datetime()
    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, times=borrow.times+1)
    
    return LibraryResponse.to_json_response({})


@method_required(['POST'])
def return_book(request, book_id, reader_id):  # 還書
    current_datetime = get_current_datetime()

    try:
        borrow = Borrow.objects.get(book_id=book_id, reader_id=reader_id, status=0)
    except ObjectDoesNotExist:
        return LibraryError.to_json_response(
            LibraryError.INVALID_PARAMETER,
            f"borrow of book_id {book_id}, reader_id {reader_id} not found"
        )

    if borrow.borrow_at + timedelta(days=borrow.times * BORROW_DAYS) < timezone.now():  # 逾期還書
        reader = Reader.objects.get(id=reader_id)
        Reader.objects.filter(id=reader_id).update(update_at=current_datetime, violation_times=reader.violation_times + 1)

    Borrow.objects.filter(id=borrow.id).update(update_at=current_datetime, return_at=current_datetime, status=9)
    
    return LibraryResponse.to_json_response({})

