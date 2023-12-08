from rest_framework.views import APIView
from Account.serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        ser = UserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)



class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')

        if not mobile or not password:
            error_message = "Mobile number and password are required."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(mobile=mobile).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        resp = Response()
        resp.set_cookie(key='jwt', value=token, httponly=True)
        resp.data = {
            "token": token
        }
        return resp


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticate User!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticate User!")
        user = User.objects.filter(id=payload['id']).first()
        ser = UserSerializer(user)
        return Response(ser.data)

class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"You have logged out"
        }
        return response