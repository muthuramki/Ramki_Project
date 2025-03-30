from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, TravelRequest
from .serializers import RegisterSerializer, UserSerializer, TravelRequestSerializer

# User Registration
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "User registered successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

# User Login (JWT)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    print(f"Login Attempt:")
    print(f"  Username: {username}")


    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=400)
    

    print("User Logged In:")
    print(f"  Username: {user.username}")
    print(f"  ID: {user.id}")
    print(f"  Is Admin: {user.is_admin}")

    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
        "is_admin": user.is_admin 
    })

# Get User Info
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request):
    serializer = UserSerializer(request.user)
    data = serializer.data
    data["is_admin"] = request.user.is_admin  # Ensure frontend gets admin status
    return JsonResponse(data, safe=False)

# List & Create Travel Requests
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def travel_request_list(request):
    if request.method == "GET":
        if request.user.is_admin:
            travel_requests = TravelRequest.objects.all()
        else:
            travel_requests = TravelRequest.objects.filter(user=request.user)
        serializer = TravelRequestSerializer(travel_requests, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = request.data.copy()
        data["user"] = request.user.id  # Assign user ID directly
        serializer = TravelRequestSerializer(data=data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)

# Retrieve, Update, Approve, Reject Travel Requests
@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def travel_request_detail(request, pk):
    try:
        travel_request = TravelRequest.objects.get(pk=pk)
        if not request.user.is_admin and travel_request.user != request.user:
            return JsonResponse({"error": "You do not have permission to view this request"}, status=403)
    except TravelRequest.DoesNotExist:
        return JsonResponse({"error": "Travel request not found"}, status=404)

    if request.method == "GET":
        serializer = TravelRequestSerializer(travel_request)
        return JsonResponse(serializer.data, safe=False)

    if request.method in ["PUT", "PATCH"]:
        if request.user.is_admin:
            status = request.data.get("status")
            if status in ["approved", "rejected"]:
                travel_request.status = status
                travel_request.save()
                return JsonResponse({"message": f"Travel request {status}"})
        serializer = TravelRequestSerializer(travel_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

# Get All Travel Requests (Admin Only)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_travel_requests(request):
    if not request.user.is_admin:
        return JsonResponse({"error": "Permission denied"}, status=403)
    travel_requests = TravelRequest.objects.all()
    serializer = TravelRequestSerializer(travel_requests, many=True)
    return JsonResponse(serializer.data, safe=False)
