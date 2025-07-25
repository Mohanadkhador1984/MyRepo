# quiz/views.py

import os
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Book
from .serializers import QuestionSerializer, BookSerializer

# مسارات ملفات Excel
EXCEL_Q = r'C:\Users\Mohanad\Desktop\1.xlsx'
EXCEL_B = r'C:\Users\Mohanad\Desktop\books.xlsx'

# أعمدة ملف الأسئلة كما في Excel (كلها أحرف صغيرة وبعد إزالة المسافات)
QUESTION_COLS = [
    'id', 'question_en', 'question_ar',
    'answer1_en', 'answer1_ar',
    'answer2_en', 'answer2_ar',
    'answer3_en', 'answer3_ar',
    'answer4_en', 'answer4_ar',
    'correct_answer',
    'attached_text', 'attached_text_ar',
    'year', 'type'
]

# أعمدة ملف الكتب
BOOK_COLS = [
    'id', 'title', 'page_number', 'content', 'type'
]

def _load_and_validate(path, expected_cols):
    """
    1) يقرأ ملف Excel باستخدام openpyxl
    2) يطبع الأعمدة المكتشفة
    3) يتأكد أن كل expected_cols موجودة
    4) يملأ القيم الفارغة بسقيم افتراضية
    """
    if not os.path.exists(path):
        return None, f"File not found: {path}"

    try:
        df = pd.read_excel(path, engine='openpyxl')
    except Exception as e:
        return None, f"Error reading Excel: {e}"

    # تطبيع أسماء الأعمدة
    df.columns = df.columns.str.strip().str.lower()
    found = df.columns.tolist()

    missing = [c for c in expected_cols if c not in found]
    if missing:
        return None, f"Missing columns in Excel: {missing}"

    # ملء NaN في الأعمدة النصية بسلاسل فارغة
    text_cols = [c for c in expected_cols if df[c].dtype == object]
    df[text_cols] = df[text_cols].fillna('')

    # ملء NaN في الأعمدة الرقمية بصفر ثم تحويلها إلى int
    num_cols = [c for c in expected_cols if c not in text_cols and c != 'id']
    for c in num_cols:
        df[c] = df[c].fillna(0).astype(int)

    return df, None

@api_view(['GET'])
def api_root(request):
    base = request.build_absolute_uri().rstrip('/')
    return Response({
        'questions':        f'{base}/questions/',
        'books':            f'{base}/books/',
        'import_questions': f'{base}/import-questions/',
        'import_books':     f'{base}/import-books/',
    })

@api_view(['GET'])
def questions_list(request):
    """GET /api/quiz/questions/"""
    qs = Question.objects.all()
    serializer = QuestionSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def books_list(request):
    """GET /api/quiz/books/"""
    qs = Book.objects.all()
    serializer = BookSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def import_questions(request):
    """
    POST /api/quiz/import-questions/
    يستورد الأسئلة من 1.xlsx ويتجاهل الأسئلة الموجودة مسبقًا.
    """
    df, error = _load_and_validate(EXCEL_Q, QUESTION_COLS)
    if error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    imported = 0
    for record in df.to_dict(orient='records'):
        pk = int(record['id'])
        defaults = {col: record[col] for col in QUESTION_COLS if col != 'id'}
        _, created = Question.objects.update_or_create(id=pk, defaults=defaults)
        if created:
            imported += 1

    return Response(
        {'imported_questions': imported},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def import_books(request):
    """
    POST /api/quiz/import-books/
    يستورد الكتب من books.xlsx ويتجاهل الكتب الموجودة مسبقًا.
    """
    df, error = _load_and_validate(EXCEL_B, BOOK_COLS)
    if error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    imported = 0
    for record in df.to_dict(orient='records'):
        pk = int(record['id'])
        defaults = {col: record[col] for col in BOOK_COLS if col != 'id'}
        _, created = Book.objects.update_or_create(id=pk, defaults=defaults)
        if created:
            imported += 1

    return Response(
        {'imported_books': imported},
        status=status.HTTP_201_CREATED
    )
