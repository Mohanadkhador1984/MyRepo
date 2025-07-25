from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('questions/',       views.questions_list, name='questions'),
    path('books/',           views.books_list,     name='books'),
    path('import-questions/',views.import_questions, name='import-questions'),
    path('import-books/',    views.import_books,     name='import-books'),
]
