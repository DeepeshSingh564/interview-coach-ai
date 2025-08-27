from django.shortcuts import get_object_or_404, render
import json
import secrets
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Role, Question, Attempt
from .feedback_engine import score_answer
from .serializers import RoleSerializer, QuestionSerializer, AnswerSubmissionSerializer, AttemptSerializer
from .ai_engine import ai_evaluate_answer
from .feedback_engine import score_answer

# Create your views here.

def home(request):
  roles=Role.objects.all()
  return render(request, 'interview/home.html', {'roles': roles})

def interview_page(request):
    roles = Role.objects.order_by("name")
    return render(request, "interview/interview.html", {"roles": roles})

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

@csrf_exempt  # OK for dev; remove later with proper CSRF
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

    # Default: rule-based scoring (free)
    use_ai = payload.get("use_ai", False)

    if use_ai:
        # Try AI evaluation
        try:
            from .ai_engine import ai_evaluate_answer
            result = ai_evaluate_answer(q.text, answer_text)

            score = result.get("score", 0)
            fb = (
                f"Strengths: {', '.join(result.get('strengths', []))}\n"
                f"Weaknesses: {', '.join(result.get('weaknesses', []))}\n"
                f"Improvements: {', '.join(result.get('improvements', []))}"
            )
        except Exception as e:
            # Fall back to rule-based if AI fails
            score, fb = score_answer(answer_text, q.keywords or [])
    else:
        # Use local feedback engine
        score, fb = score_answer(answer_text, q.keywords or [])

    # Save attempt in DB
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


@api_view(['GET', 'POST'])
def api_answer_browsable(request):
    """
    Browsable API endpoint for submitting answers.
    GET: Shows the form interface
    POST: Submits the answer
    """
    if request.method == 'GET':
           # Get some sample questions for easy testing
            sample_questions = list(Question.objects.select_related('role').values(
                'id', 'text', 'role__name', 'difficulty', 'keywords'
            )[:3])

            # Return information about how to use this endpoint with examples
            return Response({
                'message': 'Submit an answer using the form below. Try copying one of the sample question IDs.',
                'instructions': {
                    'step1': 'Choose a question_id from the samples below',
                    'step2': 'Write your answer in the answer_text field',
                    'step3': 'Optionally add a user_session identifier',
                    'step4': 'Click POST to submit'
                },
                'sample_data_to_try': {
                    'question_id': sample_questions[0]['id'] if sample_questions else 1,
                    'answer_text': 'I have experience with Python, Django, and REST APIs. I can work with databases and implement user authentication systems.',
                    'user_session': 'demo-session-123'
                },
                'available_questions': sample_questions
        })
    
    elif request.method == 'POST':
        serializer = AnswerSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        question_id = serializer.validated_data['question_id']
        answer_text = serializer.validated_data['answer_text']
        user_session = serializer.validated_data.get('user_session') or secrets.token_hex(8)
        
        try:
            q = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Invalid question_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        score, fb = score_answer(answer_text, q.keywords or [])
        attempt = Attempt.objects.create(
            question=q,
            user_session=user_session,
            answer_text=answer_text,
            feedback_text=fb,
            score=score,
        )
        
        result_serializer = AttemptSerializer(attempt)
        return Response({
            'attempt_id': attempt.id,
            'score': score,
            'feedback': fb,
            'user_session': user_session,
            'attempt_details': result_serializer.data
        }, status=status.HTTP_201_CREATED)



  