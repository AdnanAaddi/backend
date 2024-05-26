from django.views.decorators.csrf import csrf_exempt
from api.serializers import TodoSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from api.models import Todo
from rest_framework.exceptions import ParseError

@csrf_exempt
def Todo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        try:
            todos = Todo.objects.all()
            print("Queryset:", todos)  # Debug: Print the queryset
            serializer = TodoSerializer(todos, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            print("Error retrieving Todo objects:", e)  # Log error for debugging
            return JsonResponse({'error': 'Failed to retrieve Todo objects'}, status=500)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            print("Parsed data:", data)  # Debug: Print parsed data
            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except ParseError as e:
            print("ParseError:", e)  # Debug: Log parse error
            return JsonResponse({'error': 'Invalid or empty JSON payload'}, status=400)
        except Exception as e:
            print("Error:", e)  # Debug: Log any other errors
            return JsonResponse({'error': str(e)}, status=500)