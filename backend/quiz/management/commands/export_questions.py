from django.core.management.base import BaseCommand
from quiz.models import Question
import json, os
from django.conf import settings

class Command(BaseCommand):
    help = 'Export questions to static JSON file'

    def handle(self, *args, **kwargs):
        # جلب جميع الأسئلة كنصوص
        qs = Question.objects.all().values()
        questions_list = list(qs)

        # مسار الإخراج داخل quiz/static/data
        output_dir = os.path.join(settings.BASE_DIR, 'quiz', 'static', 'data')
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'questions.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions_list, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'✅ Exported questions to {output_path}'
        ))
