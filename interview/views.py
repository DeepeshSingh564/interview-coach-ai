from django.shortcuts import render
import json
import secrets
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Role, Question, Attempt
from .feedback_engine import score_answer


# Create your views here.

def home(request):
  return render(request, 'interview/home.html')

@require_GET
def api_roles(request):
  roles = list(Role.objects.order_by('name').values('id', 'name', 'slug'))
  return JsonResponse({'roles': roles})

@require_GET
def api_question(request):
  role_id = request.GET.get('role_id')
  if not role_id:
    return HttpResponseBadRequest("role_id is required")
  q=Question.objects.filter(role_id=role_id).order_by('?').first()
  if not q:
    return JsonResponse({'question' : None})
  return JsonResponse({
    'question':{
      'id': q.id,
      'text': q.text,
      'difficulty': q.difficulty,
      'keywords': q.keywords,
    }
  })  

@csrf_exempt # OK for dev; remove when you add proper forms/CSRF on frontend
@require_POST
def api_answer(request):
  try:
    payload = json.loads(request.body.decode('utf-8'))
    question_id = payload['question_id']
    answer_text = payload['answer_text']
    user_session = payload.get('user_session') or secrets.token_hex(8)

  except Exception:
    return HttpResponseBadRequest("Invalid JSON")

  try:
    q = Question.objects.get(id=question_id)
  except Question.DoesNotExist:
    return HttpResponseBadRequest("Invalid question_id")

  score, fb = score_answer(answer_text, q.keywords or [])
  attempt = Attempt.objects.create(
    question=q,
    user_session=user_session,
    answer_text=answer_text,
    feedback_text=fb,
    score=score,
  )
  return JsonResponse({
    'attempt_id': attempt.id,
    'score': score,
    'feedback': fb,
    'user_session': user_session
  })



  