from rest_framework import serializers
from .models import User
from .models import Item
from .models import Transaction
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'number', 'email']
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','name','stock','description','user']
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'input','amount','date','description','item']