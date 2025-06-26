from django.urls import path
from .views import import_data_from_excel, import_books_from_excel, load_questions, index, offline, service_worker

app_name = 'quiz'

urlpatterns = [
    path('offline/', offline, name='offline'),
    path('index/', index, name='index'),
    path('import-questions/', import_data_from_excel, name='import_questions'),
    path('import-books/', import_books_from_excel, name='import_books'),
    path('load-questions/', load_questions, name='load_questions'),
    path('serviceworker.js', service_worker, name='serviceworker'),
]