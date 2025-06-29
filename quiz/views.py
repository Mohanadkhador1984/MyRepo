# quiz/views.py

import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # تأكد من استيراد JsonResponse
from .models import Question, Book
from django.conf import settings




# مسارات ملفات Excel
excel_file_path = r'C:\Users\Mohanad\Desktop\1.xlsx'
books_excel_file_path = r'C:\Users\Mohanad\Desktop\books.xlsx'


def index(request):
    return render(request, "quiz/index.html")


def offline(request):
    return render(request, "quiz/offline.html")


def import_data_from_excel(request):
    """استيراد البيانات الجديدة فقط من ملفات Excel إلى قاعدة البيانات."""
    try:
        if not os.path.exists(excel_file_path):
            return HttpResponse("Excel file not found.")

        # قراءة ملف Excel
        df1 = pd.read_excel(excel_file_path)

        if df1.empty:
            return HttpResponse("The Excel file is empty.")

        # إدخال البيانات الجديدة فقط في `questions`
        for _, row in df1.iterrows():
            question, created = Question.objects.get_or_create(
                id=row['id'],
                defaults={
                    'question_en': row['question_en'],
                    'question_ar': row['question_ar'],
                    'answer1_en': row['answer1_en'],
                    'answer1_ar': row['answer1_ar'],
                    'answer2_en': row['answer2_en'],
                    'answer2_ar': row['answer2_ar'],
                    'answer3_en': row['answer3_en'],
                    'answer3_ar': row['answer3_ar'],
                    'answer4_en': row['answer4_en'],
                    'answer4_ar': row['answer4_ar'],
                    'correct_answer': row['correct_answer'],
                    'attached_text': row['attached_text'],
                    'attached_text_ar': row['attached_text_ar'],
                    'year': row['year'],
                    'type': row['type']
                }
            )
            if created:
                print(f"Question {question.id} created.")
            else:
                print(f"Question {question.id} already exists.")

        return HttpResponse("New questions data imported successfully.")
    except Exception as e:
        return HttpResponse(f"Error importing data from Excel: {e}")

def import_books_from_excel(request):
    """استيراد البيانات الجديدة فقط من ملف الكتب إلى قاعدة البيانات."""
    try:
        if not os.path.exists(books_excel_file_path):
            return HttpResponse(f"File not found: {books_excel_file_path}")

        df = pd.read_excel(books_excel_file_path)

        if df.empty:
            return HttpResponse("The books Excel file is empty.")

        for _, row in df.iterrows():
            book, created = Book.objects.get_or_create(
                id=row['id'],
                defaults={
                    'title': row['title'],
                    'page_number': row['page_number'],
                    'content': row['content'],
                    'type': row['type']
                }
            )
            if created:
                print(f"Book {book.id} created.")
            else:
                print(f"Book {book.id} already exists.")

        return HttpResponse("New books data imported successfully.")
    except Exception as e:
        return HttpResponse(f"Error importing books data from Excel: {e}")

def load_questions(request):
    """تحميل الأسئلة من قاعدة البيانات وإرجاعها كـ JSON."""
    questions = Question.objects.all().values(
        'id', 
        'question_en',  # إضافة السؤال باللغة الإنجليزية
        'question_ar',  # السؤال باللغة العربية
        'answer1_en',   # الإجابة الأولى باللغة الإنجليزية
        'answer1_ar',   # الإجابة الأولى باللغة العربية
        'answer2_en',   # الإجابة الثانية باللغة الإنجليزية
        'answer2_ar',   # الإجابة الثانية باللغة العربية
        'answer3_en',   # الإجابة الثالثة باللغة الإنجليزية
        'answer3_ar',   # الإجابة الثالثة باللغة العربية
        'answer4_en',   # الإجابة الرابعة باللغة الإنجليزية
        'answer4_ar',   # الإجابة الرابعة باللغة العربية
        'correct_answer',  # الإجابة الصحيحة
        'attached_text',  # نص مرفق (إن وجد)
        'attached_text_ar',  # نص مرفق باللغة العربية (إن وجد)
        'year',  # رقم الاختبار من 1-9
        'type'   # A or B
    )
    return JsonResponse(list(questions), safe=False)
