
from django.core.management.base import BaseCommand
from interview.models import Role, Question


class Command(BaseCommand):
    help = "Seed the database with sample interview questions"

    def handle(self, *args, **kwargs):
        # Create roles first
        roles_data = [
            {"name": "Python Developer", "slug": "python-developer", "description": "Python programming questions"},
            {"name": "Django Developer", "slug": "django-developer", "description": "Django framework questions"},
            {"name": "Frontend Developer", "slug": "frontend-developer", "description": "Frontend development questions"},
            {"name": "Full Stack Developer", "slug": "fullstack-developer", "description": "Full stack development questions"},
        ]
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                slug=role_data["slug"],
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"]
                }
            )
            if created:
                self.stdout.write(f"Created role: {role.name}")

        # Get role objects
        python_role = Role.objects.get(slug="python-developer")
        django_role = Role.objects.get(slug="django-developer")
        frontend_role = Role.objects.get(slug="frontend-developer")
        fullstack_role = Role.objects.get(slug="fullstack-developer")

        # Questions data
        questions_data = {
            python_role: [
                ("What are Python's key features?", "easy", "interpreted,dynamic,OOP"),
                ("Explain list comprehension in Python with an example.", "medium", "list comprehension,syntax,example"),
                ("What is the difference between deep copy and shallow copy in Python?", "hard", "copy,memory,mutable"),
                ("What are Python decorators and how are they used?", "medium", "decorator,function,wrapper"),
                ("Explain Python's garbage collection mechanism.", "hard", "garbage collection,memory,reference count"),
                ("What are Python's data types?", "easy", "int,list,dict,tuple"),
                ("What is the difference between Python 2 and Python 3?", "medium", "unicode,print,division"),
                ("Explain the use of *args and **kwargs in Python functions.", "medium", "args,kwargs,parameters"),
                ("What are Python generators and how do they differ from iterators?", "hard", "yield,iterator,generator"),
                ("How does Python handle multithreading and multiprocessing?", "hard", "GIL,thread,process"),
            ],
            django_role: [
                ("What is Django's MTV architecture?", "easy", "model,template,view"),
                ("Explain Django's ORM and how to create models.", "medium", "ORM,models,database"),
                ("What are Django middleware and how do they work?", "medium", "middleware,request,response"),
                ("How do you handle forms in Django?", "medium", "forms,validation,POST"),
                ("Explain Django's authentication system.", "hard", "auth,user,permissions"),
                ("What are Django signals and when would you use them?", "hard", "signals,pre_save,post_save"),
                ("How do you optimize Django queries for better performance?", "hard", "select_related,prefetch_related,queryset"),
                ("What is Django REST framework and how do you create APIs?", "medium", "DRF,serializers,viewsets"),
                ("Explain Django's caching mechanisms.", "medium", "cache,redis,memcached"),
                ("How do you deploy a Django application?", "hard", "deployment,WSGI,production"),
            ],
            frontend_role: [
                ("What is the difference between let, const, and var in JavaScript?", "easy", "let,const,var,scope"),
                ("Explain the concept of closures in JavaScript.", "medium", "closure,scope,function"),
                ("What are React hooks and how do they work?", "medium", "hooks,useState,useEffect"),
                ("How do you optimize React application performance?", "hard", "React.memo,useMemo,useCallback"),
                ("What is the virtual DOM and how does it work?", "medium", "virtual DOM,reconciliation,React"),
                ("Explain CSS flexbox and grid layouts.", "medium", "flexbox,grid,layout"),
                ("What are JavaScript promises and async/await?", "medium", "promises,async,await,asynchronous"),
                ("How do you handle state management in large React applications?", "hard", "Redux,Context,state management"),
                ("What is responsive web design and how do you implement it?", "easy", "responsive,media queries,mobile"),
                ("Explain the concept of RESTful APIs and how to consume them.", "medium", "REST,API,fetch,HTTP"),
            ],
            fullstack_role: [
                ("How do you design a scalable web application architecture?", "hard", "scalability,architecture,microservices"),
                ("Explain the differences between SQL and NoSQL databases.", "medium", "SQL,NoSQL,database,MongoDB"),
                ("How do you implement authentication and authorization in a web app?", "hard", "auth,JWT,sessions,security"),
                ("What are design patterns and which ones do you use most?", "hard", "design patterns,MVC,singleton,factory"),
                ("How do you handle API versioning and backward compatibility?", "hard", "API versioning,backward compatibility,REST"),
                ("Explain containerization and how you would use Docker.", "medium", "Docker,containers,deployment"),
                ("How do you implement real-time features in web applications?", "hard", "WebSockets,real-time,Socket.io"),
                ("What is CI/CD and how do you implement it?", "medium", "CI/CD,deployment,automation"),
                ("How do you optimize database performance?", "hard", "database optimization,indexing,queries"),
                ("Explain caching strategies for web applications.", "medium", "caching,Redis,CDN,performance"),
            ],
        }

        # Create questions
        for role, questions in questions_data.items():
            for question_text, difficulty, keywords in questions:
                question, created = Question.objects.get_or_create(
                    role=role,
                    text=question_text,
                    defaults={
                        "difficulty": difficulty,
                        "keywords": keywords
                    }
                )
                if created:
                    self.stdout.write(f"Created question for {role.name}: {question_text[:50]}...")

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with questions!"))
