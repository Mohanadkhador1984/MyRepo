# quiz/management/commands/import_data.py

import os
import pandas as pd
from django.db import models
from django.core.management.base import BaseCommand
from quiz.models import Question, Book

class Command(BaseCommand):
    help = 'Import all columns from Excel files for Questions and Books.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--questions-file',
            type=str,
            default=r'C:\Users\Mohanad\Desktop\1.xlsx',
            help='مسار ملف الأسئلة (Excel)'
        )
        parser.add_argument(
            '--books-file',
            type=str,
            default=r'C:\Users\Mohanad\Desktop\books.xlsx',
            help='مسار ملف الكتب (Excel)'
        )

    def handle(self, *args, **options):
        q_file = options['questions_file']
        b_file = options['books_file']

        q_count = self._import_file(Question, q_file, 'Questions')
        b_count = self._import_file(Book,     b_file, 'Books')

        self.stdout.write(f"✅ Imported {q_count} new questions and {b_count} new books.")

    def _import_file(self, model, filepath, label):
        """
        Generic importer:
        1) Reads the Excel
        2) Normalizes column names
        3) Fills NaN appropriately
        4) Uses update_or_create on 'id' to insert new records
        """
        if not os.path.exists(filepath):
            self.stderr.write(f"❌ {label} file not found: {filepath}")
            return 0

        try:
            df = pd.read_excel(filepath, engine='openpyxl')
        except Exception as e:
            self.stderr.write(f"❌ Error reading {label} Excel: {e}")
            return 0

        # normalize column names
        df.columns = df.columns.str.strip().str.lower()
        self.stdout.write(f"{label} columns → {df.columns.tolist()}")

        if 'id' not in df.columns:
            self.stderr.write(f"❌ Missing 'id' column in {label} file.")
            return 0

        # fill numeric columns with 0 and cast to int
        for num_col in ('correct_answer', 'year', 'page_number'):
            if num_col in df.columns:
                df[num_col] = df[num_col].fillna(0).astype(int)

        # fill all other NaNs with empty string
        df = df.fillna('')

        # get concrete, non-relational field names
        concrete_fields = {
            f.name: f for f in model._meta.get_fields()
            if getattr(f, 'concrete', False) and not f.is_relation
        }

        imported = 0
        for record in df.to_dict(orient='records'):
            raw_id = record.get('id')
            try:
                pk = int(raw_id)
            except (TypeError, ValueError):
                self.stderr.write(f"⚠️ Skipping row with invalid id: {raw_id}")
                continue

            defaults = {}
            for col, val in record.items():
                if col == 'id' or col not in concrete_fields:
                    continue

                field = concrete_fields[col]
                # if the model field is IntegerField but value is string, cast
                if isinstance(field, models.IntegerField):
                    try:
                        val = int(val)
                    except (TypeError, ValueError):
                        val = 0
                defaults[col] = val

            obj, created = model.objects.update_or_create(id=pk, defaults=defaults)
            if created:
                imported += 1

        return imported
