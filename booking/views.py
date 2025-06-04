
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer
from zoneinfo import ZoneInfo

IST = ZoneInfo('Asia/Kolkata')

@api_view(['GET'])
def get_classes(request):
    classes = FitnessClass.objects.filter(datetime__gte=datetime.now(tz=IST))
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    data = request.data
    required = ['class_id', 'client_name', 'client_email']
    if not all(field in data for field in required):
        return Response({"error": "Missing required fields"}, status=400)

    try:
        fitness_class = FitnessClass.objects.get(pk=data['class_id'])
    except FitnessClass.DoesNotExist:
        return Response({"error": "Class not found"}, status=404)

    if fitness_class.available_slots <= 0:
        return Response({"error": "No slots available"}, status=400)

    booking = Booking(
        fitness_class=fitness_class,
        client_name=data['client_name'],
        client_email=data['client_email']
    )
    booking.save()
    fitness_class.available_slots -= 1
    fitness_class.save()
    return Response({"message": "Booking successful"}, status=201)

@api_view(['GET'])
def get_bookings(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)

    bookings = Booking.objects.filter(client_email=email)
    result = []
    for b in bookings:
        cls = b.fitness_class
        result.append({
            "class_name": cls.name,
            "datetime": cls.datetime.astimezone(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST'),
            "instructor": cls.instructor
        })
    return Response(result)
