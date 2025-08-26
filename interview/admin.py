from django.contrib import admin
from .models import Role, Question, Attempt
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "slug")
  search_fields=("name", "slug")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ("id", "role", "text", "difficulty", "short_text", "created_at")
  list_filter = ("role", "difficulty")
  search_fields = ("text", "keywords")

  def short_text(self, obj):
    return (obj.text[:50] + "...") if len(obj.text) > 60 else obj.text


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
  list_display=("id", "question","user_session", "score", "created_at")
  list_filter=("score","created_at")
  search_fields=("user_session", "answer_text", "feedback_text")
  
