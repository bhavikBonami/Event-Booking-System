from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer, UserLoginSerializer
from .models import Customer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from configuration import message, constants, utils
from rest_framework.decorators import authentication_classes, permission_classes

@authentication_classes([])
@permission_classes([])
class Register(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                print("request.data")
                cust_type = request.data.get('cust_type', False)
                serializer.save(cust_type=cust_type)
                # return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
                return utils.success_response(status_code=status.HTTP_201_CREATED, message=message.USER_CREATED)
            
            else:
                return utils.failure_response(message=message.BAD_REQUEST,status_code=status.HTTP_400_BAD_REQUEST)
            
        except Exception as error:
            print(error)
            return utils.failure_response(message=message.INTERNAL_SERVER_ERROR,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserListView(APIView):
    def get(self, request):
        try:
            queryset = Customer.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response({"users": serializer.data})
        except Exception as error:
            print("Error in user list API",error)
            return utils.failure_response(message=message.INTERNAL_SERVER_ERROR,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return utils.failure_response(message=message.INCORRECT_USERNAME_OR_PASSWORD,status_code=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as error:
            return utils.failure_response(message=message.INTERNAL_SERVER_ERROR,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
