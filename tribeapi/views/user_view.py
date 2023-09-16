# """View module for handling requests about game types"""
# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers, status
# from django.contrib.auth.models import User
# from tribeapi.models import TribeUser

# class TribeUserView(ViewSet):
#     # "VibeTribe django user view.

#     def retrieve(self, request, pk):
#         """Handle GET requests for a single user
#         Returns:
#             Response -- JSON serialized user
#         """
#         try:
#             user = User.objects.get(pk=pk)
#             tribe_user = TribeUser.objects.get(user=user)
#             serializer = UserSerializer(user)
#             tribe_user_serializer = TribeUserSerializer(tribe_user)
#             return Response({
#                 "user": serializer.data,
#                 "tribe_user": tribe_user_serializer.data
#             })
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         except TribeUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def list(self, request):
#         """Handle GET requests to get all users

#         Returns:
#             Response -- JSON serialized list of users
#         """
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)




# class TribeUserSerializer(serializers.ModelSerializer):
#     """JSON serializer for customers"""

#     class Meta:
#         model = TribeUser
#         fields = ('id', 'user', 'bio','img_url')


# class UserSerializer(serializers.ModelSerializer):
#     """JSON serializer for customers"""

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'last_name', 'first_name', 'password'
#                 'email', 'date_joined', 'is_staff')