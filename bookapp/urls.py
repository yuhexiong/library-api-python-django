from django.urls import path
from bookapp import views

urlpatterns = [
    # 使用者
    path('user', views.createAndGetUser, name="createAndGetUser"),
    path('user/<str:userId>', views.deleteUser, name="deleteUser"),

    # 作者
    path('author', views.createAndGetAuthor, name="createAndGetAuthor"),
    path('author/<str:authorId>', views.deleteUser, name="deleteUser"),

    # 讀者
    path('reader', views.createAndGetReader, name="createAndGetReader"),
    path('reader/<str:readerId>', views.deleteReader, name="deleteReader"),

    # 書本類型
    path('bookType', views.createAndGetBookType, name="createAndGetBookType"),
    path('bookType/<str:bookTypeId>', views.deleteBookType, name="deleteBookType"),

    # 書本
    path('book', views.createAndGetBook, name="createAndGetBook"),
    path('book/<str:bookId>', views.deleteBook, name="deleteBook"),

    # 借書 續借 還書
    path('borrow/<str:bookId>/<str:readerId>', views.borrowBook, name="borrowBook"),
    path('renew/<str:bookId>/<str:readerId>', views.renewBook, name="renewBook"),
    path('return/<str:bookId>/<str:readerId>', views.returnBook, name="returnBook"),

    # 心得
    path('report', views.createAndGetReport, name="createAndGetReport"),
    path('report/<str:reportId>', views.updateAndDeleteReport, name="updateAndDeleteReport"),

    # 排名
    path('rank/borrowTimes', views.getRankOfBorrowTimes, name="getRankOfBorrowTimes"),
    path('rank/violationTimes', views.getRankOfViolationTimes, name="getRankOfViolationTimes"),
    path('rank/publishTimes', views.getRankOfPublishTimes, name="getRankOfPublishTimes"),
]
