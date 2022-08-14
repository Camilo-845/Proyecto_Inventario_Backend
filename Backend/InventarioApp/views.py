from ast import Break
import re
from rest_framework import status, views, generics
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User
from .models import Item
from .models import Transaction
from .serializers import UserSerializer
from .serializers import ItemSerializer
from .serializers import TransactionSerializer

# UserCRUD

#Crear Usuario
class UserCreateView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        tokenData = {"username":request.data["username"],
                     "password":request.data["password"]}
        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)
        return Response(tokenSerializer.validated_data, status=status.HTTP_201_CREATED)

#Detalles del Usuario
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

#Actualizar informacion del Usuario        
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    def put (self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)


#ItemCRUD

#Crear Item
class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)
    def post (self, request, *args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != int(request.data["user"]):
            stringResponse = {'detail':'Unauthorized Request, Incorrect User'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Item creado", status=status.HTTP_201_CREATED)
    
#Borrar Item
class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)
    def delete (self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

#Actualizar Item
class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)
    def put (self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

#Detalles del item por id
class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class= ItemSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

#Lista de Items filtradas por usuario
class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class= ItemSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != self.kwargs['user']:
            return 
        queryset = Item.objects.filter(user_id=self.kwargs['user'])
        return queryset
    #Error AL poner algun contenido en el return si 
    # el id del token es diferente al id del kwargs
    """
    AttributeError at /itemListView/2/
    Got AttributeError when attempting to get a value for field `name` on serializer `ItemSerializer`.
    The serializer field might be named incorrectly and not match any attribute or key on the `str` instance.
    Original exception text was: 'str' object has no attribute 'name'.
    """

#TransactionCRUD

#Crear Transaccion
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    def post (self, request, *args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        item=Item.objects.get(id=request.data['item'])
        if valid_data['user_id'] != kwargs["user"]:
            stringResponse = {'detail':'Unauthorized Request, Incorrect User'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        if request.data['input']==True:
            item.stock += int(request.data['amount'])
            item.save()
        else:
            if item.stock < int(request.data['amount']):
                stringResponse = {'detail':'Cantidad insuficiente'}
                return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            item.stock -= int(request.data['amount'])
            item.save()
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Transaccion exitosa", status=status.HTTP_201_CREATED)

#Detalles de transaccion
class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class= TransactionSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

#Transacciones por Item
class TransactionByItemListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class= TransactionSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != self.kwargs['user']:
            return 
        queryset = Transaction.objects.filter(item_id=self.kwargs['item'])
        return queryset

    #Tiene el mismo error que la otra lista

#Transacciones por usuario