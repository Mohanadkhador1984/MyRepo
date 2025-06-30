from django.core.management.base import BaseCommand
from quiz.models import Question  # غيّر هذا حسب اسم الموديل الحقيقي
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Export questions to static JSON file'

    def handle(self, *args, **kwargs):
        questions = Question.objects.all().values()
        questions_list = list(questions)

        output_dir = os.path.join(settings.BASE_DIR, 'quiz', 'static', 'data')
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'questions.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions_list, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'✅ تم تصدير الأسئلة إلى {output_path}'))
