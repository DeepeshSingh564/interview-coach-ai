from django.db import models

# Create your models here.

class Role(models.Model):
  name=models.CharField(max_length=200,unique=True)
  slug=models.SlugField(max_length=120,unique=True)

  def __str__(self):
    return self.name

class Question(models.Model):
  DIFF_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard')
  ]
  role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name='questions')
  text=models.TextField()
  difficulty=models.CharField(max_length=10, choices=DIFF_CHOICES,default='easy')
  keywords=models.JSONField(default=list,blank=True)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"[{self.role}] {self.text[:50]}"


class Attempt(models.Model):
  question=models.ForeignKey(Question,on_delete=models.CASCADE)
  user_session=models.CharField(max_length=64)
  answer_text=models.TextField()
  feedback_text=models.TextField()
  score=models.IntegerField(default=0)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Attempt {self.id} on Q{self.question_id}"


  