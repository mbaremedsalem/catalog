from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.views import TokenObtainPairView

#------ api login --------
import logging
logger = logging.getLogger(__name__)

class MyLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.debug(f"Attempting login with username: {username}")

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        logger.debug("Invalid credentials")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
#------ api Register --------
class MyRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)  # Debugging statement
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer valid")  # Debugging statement
            user = serializer.save()
            username = serializer.validated_data['username']
            message = f"Hey {username}, your account was created successfully"

            # Authenticate the new user with their email and password
            new_user = authenticate(username=user.username, password=request.data['password1'])
            if new_user is not None:
                login(request, new_user)

            return Response({'message': message}, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response({'status': status.HTTP_200_OK, 'Message':"Vous avez été déconnecté avec succès"})
        except Exception as e:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Requête incorrecte'})
       
#---- view django -----
def RegisterView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            new_user = form.save() #new user.email
            username = form.cleaned_data.get("username")
            # username = request.POST.get("username")
            messages.success(request,f"Hey {username}, your account was created successfully")
            # new_user = authenticate(username=form.cleaned_data.get('email'))
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("userauths:index")
        
    # elif request.user.is_authenticated:
    #     messages.success(request,f"your are already logged in")

    #     return redirect("core:index")        

    else:
        form = UserRegisterForm()       
    context = {
        "form":form
    } 
    return render(request,"userauths/sign-up.html",context)


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)

            if user is not None: # if there is a user
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect("userauths:account")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("userauths/account.html")
        
    return render(request, "userauths/sign-in.html")


def logoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("userauths:sign-in")


#---- account -------
def account(request):
    if request.user.is_authenticated:
        try:
            # kyc = KYC.objects.get(user=request.user)
            pass
        except:
            # messages.warning(request, "You need to submit your kyc")
            return redirect("userauths:account.html")
        
        # account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

    # context = {
    #     "kyc":kyc,
    #     "account":account,
    # }
    return render(request, "userauths/account.html")

