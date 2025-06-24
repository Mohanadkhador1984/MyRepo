from django.urls import path
from .views import import_data_from_excel, import_books_from_excel, load_questions, home,offline  # استيراد دالة العرض للصفحة الرئيسية
from .views import service_worker
urlpatterns = [
    path('offline/', offline, name='offline'),
    path('home/', home, name='home'),
    path('', home, name='home'),  # إضافة مسار للصفحة الرئيسية
    path('import-questions/', import_data_from_excel, name='import_questions'),  # مسار لاستيراد الأسئلة
    path('import-books/', import_books_from_excel, name='import_books'),        # مسار لاستيراد الكتب
    path('load-questions/', load_questions, name='load_questions'),  
     path('serviceworker.js', service_worker, name='serviceworker'),
           # مسار لتحميل الأسئلة
]


