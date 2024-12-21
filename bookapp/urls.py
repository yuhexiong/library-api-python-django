from django.urls import path
from bookapp.views import user as userView
from bookapp.views import author as authorView
from bookapp.views import reader as readerView
from bookapp.views import book_type as bookTypeView

urlpatterns = [
    # 使用者
    path('user', userView.create_and_get_user, name="create_and_get_user"),
    path('user/<str:user_id>', userView.delete_user, name="delete_user"),

    # 作者
    path('author', authorView.create_and_get_author, name="create_and_get_author"),
    path('author/<str:author_id>', authorView.delete_author, name="delete_author"),

    # 讀者
    path('reader', readerView.create_and_get_reader, name="create_and_get_reader"),
    path('reader/<str:reader_id>', readerView.delete_reader, name="delete_reader"),

    # 書本類型
    path('book_type', bookTypeView.create_and_get_book_type, name="create_and_get_book_type"),
    path('book_type/<str:book_type_id>', bookTypeView.delete_book_type, name="delete_book_type"),

    # 書本
    path('book', views.create_and_get_book, name="create_and_get_book"),
    path('book/<str:book_id>', views.delete_book, name="delete_book"),

    # 借書 續借 還書
    path('borrow/<str:book_id>/<str:reader_id>', views.borrow_book, name="borrow_book"),
    path('renew/<str:book_id>/<str:reader_id>', views.renew_book, name="renew_book"),
    path('return/<str:book_id>/<str:reader_id>', views.return_book, name="return_book"),

    # 心得
    path('report', views.create_and_get_report, name="create_and_get_report"),
    path('report/<str:report_id>', views.update_and_delete_report, name="update_and_delete_report"),

    # 排名
    path('rank/borrow_times', views.get_rank_of_borrow_times, name="get_rank_of_borrow_times"),
    path('rank/violation_times', views.get_rank_of_violation_times, name="get_rank_of_violation_times"),
    path('rank/publish_times', views.get_rank_of_publish_times, name="get_rank_of_publish_times"),
]
