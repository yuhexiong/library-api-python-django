from django.urls import path

from bookapp.views import author as author_view
from bookapp.views import book as book_view
from bookapp.views import book_type as bookType_view
from bookapp.views import operation as operation_view
from bookapp.views import rank as rank_view
from bookapp.views import reader as reader_view
from bookapp.views import report as report_view
from bookapp.views import user as user_view

urlpatterns = [
    # 使用者
    path('user', user_view.create_and_get_user, name="create_and_get_user"),
    path('user/<str:user_id>', user_view.delete_user, name="delete_user"),

    # 作者
    path('author', author_view.create_and_get_author,
         name="create_and_get_author"),
    path('author/<str:author_id>', author_view.delete_author, name="delete_author"),

    # 讀者
    path('reader', reader_view.create_and_get_reader,
         name="create_and_get_reader"),
    path('reader/<str:reader_id>', reader_view.delete_reader, name="delete_reader"),

    # 書本類型
    path('book_type', bookType_view.create_and_get_book_type,
         name="create_and_get_book_type"),
    path('book_type/<str:book_type_id>',
         bookType_view.delete_book_type, name="delete_book_type"),

    # 書本
    path('book', book_view.create_and_get_book, name="create_and_get_book"),
    path('book/<str:book_id>', book_view.delete_book, name="delete_book"),

    # 操作
    path('borrow/<str:book_id>/<str:reader_id>',
         operation_view.borrow_book, name="borrow_book"),
    path('renew/<str:book_id>/<str:reader_id>',
         operation_view.renew_book, name="renew_book"),
    path('return/<str:book_id>/<str:reader_id>',
         operation_view.return_book, name="return_book"),

    # 心得
    path('report', report_view.create_and_get_report,
         name="create_and_get_report"),
    path('report/<str:report_id>', report_view.update_and_delete_report,
         name="update_and_delete_report"),

    # 排名
    path('rank/borrow_times', rank_view.get_rank_of_borrow_times,
         name="get_rank_of_borrow_times"),
    path('rank/violation_times', rank_view.get_rank_of_violation_times,
         name="get_rank_of_violation_times"),
    path('rank/publish_times', rank_view.get_rank_of_publish_times,
         name="get_rank_of_publish_times"),
]
