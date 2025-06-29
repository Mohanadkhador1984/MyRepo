import os, json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Dump all users (id, username, location) into quiz/static/quiz/data/users.json'

    def handle(self, *args, **options):
        User = get_user_model()
        output = []

        # اجمع بيانات كل مستخدم
        for u in User.objects.all():
            loc = ''
            if hasattr(u, 'profile') and hasattr(u.profile, 'location'):
                loc = u.profile.location or ''
            output.append({
                'id': u.id,
                'username': u.username,
                'location': loc,
            })

        # حدّد مسار users.json ضمن quiz/static/quiz/data/
        target_dir  = os.path.join(settings.BASE_DIR, 'quiz', 'static', 'quiz', 'data')
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, 'users.json')

        # اكتب الملف
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'✔ Dumped {len(output)} users to {target_file}'
        ))
