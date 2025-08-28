from django.core.management.base import BaseCommand
from interview.models import Role, Question

class Command(BaseCommand):
    help = "Seed the database with sample interview questions"

    def handle(self, *args, **kwargs):
        questions = {
            1: [  # Python Developer
                ("What are Python’s key features?", "easy", ["interpreted", "dynamic", "OOP"]),
                ("Explain list comprehension in Python with an example.", "medium", ["list comprehension", "syntax", "example"]),
                ("What is the difference between deep copy and shallow copy in Python?", "hard", ["copy", "memory", "mutable"]),
                ("What are Python decorators and how are they used?", "medium", ["decorator", "function", "wrapper"]),
                ("Explain Python’s garbage collection mechanism.", "hard", ["garbage collection", "memory", "reference count"]),
                ("What are Python’s data types?", "easy", ["int", "list", "dict", "tuple"]),
                ("What is the difference between Python 2 and Python 3?", "medium", ["unicode", "print", "division"]),
                ("Explain the use of *args and **kwargs in Python functions.", "medium", ["args", "kwargs", "parameters"]),
                ("What are Python generators and how do they differ from iterators?", "hard", ["yield", "iterator", "generator"]),
                ("How does Python handle multithreading and multiprocessing?", "hard", ["GIL", "thread", "process"]),
            ],
            2: [  # Django Developer
                ("What is Django’s MTV architecture?", "easy", ["model", "template", "view"]),
                ("How does Django handle migrations?", "medium", ["migrations", "database", "schema"]),
                ("Explain middleware in Django with an example.", "hard", ["middleware", "request", "response"]),
                ("What are Django signals and when would you use them?", "medium", ["signal", "decouple", "event"]),
                ("Explain how Django ORM works.", "medium", ["ORM", "queryset", "SQL"]),
                ("What are Django class-based views (CBVs) and how are they different from function-based views (FBVs)?", "hard", ["CBV", "FBV", "views"]),
                ("How does Django handle user authentication?", "easy", ["auth", "login", "logout", "session"]),
                ("Explain Django’s caching framework.", "hard", ["cache", "performance", "redis", "memcached"]),
                ("How can you optimize database queries in Django?", "hard", ["select_related", "prefetch_related", "queryset"]),
                ("What is the difference between ForeignKey, OneToOneField, and ManyToManyField in Django?", "medium", ["relationship", "foreign key", "many-to-many"]),
            ],
        }

        for role_id, q_list in questions.items():
            role = Role.objects.get(id=role_id)
            for text, difficulty, keywords in q_list:
                obj, created = Question.objects.get_or_create(
                    role=role,
                    text=text,
                    defaults={
                        "difficulty": difficulty,
                        "keywords": keywords,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {text}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {text}"))
