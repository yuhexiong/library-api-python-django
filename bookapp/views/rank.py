from django.http import JsonResponse
from bookapp.errors import LibraryCode
from bookapp.utils import method_required
from bookapp.models import Author, Reader


@method_required(['GET'])
def get_rank_of_borrow_times(request): # 取得讀者借書次數排名
    readers = list(Reader.objects.all().order_by('-borrow_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)


@method_required(['GET'])
def get_rank_of_violation_times(request): # 取得讀者違規次數排名
    readers = list(Reader.objects.all().order_by('-violation_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'readers': readers }}, safe=False)


@method_required(['GET'])
def get_rank_of_publish_times(request): # 取得作者出版次數排名
    authors = list(Author.objects.all().order_by('-publish_times').values())
    return JsonResponse({'code': LibraryCode.SUCCESSFUL.value, 'result': {'authors': authors }}, safe=False)

