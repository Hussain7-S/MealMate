import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from restaurants.models import Restaurant
from .engine import get_reply
from .models import ChatLog


@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    message = data.get('message', '')
    restaurant_id = data.get('restaurant_id')
    restaurant = None
    if restaurant_id:
        restaurant = Restaurant.objects.filter(id=restaurant_id).first()

    reply = get_reply(message, restaurant=restaurant)

    ChatLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key or '',
        message=message,
        reply=reply,
    )

    return JsonResponse({'reply': reply})
