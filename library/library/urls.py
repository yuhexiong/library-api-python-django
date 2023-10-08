"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from books import views

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
