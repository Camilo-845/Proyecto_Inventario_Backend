from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

#Users
class UserManager(BaseUserManager):
    def create_user(self, username, password=None): 
        """
        Creates and saves a user with the given username and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Username', max_length=15, unique=True)
    password = models.CharField('Password', max_length=256)
    number = models.IntegerField('Number')
    email = models.EmailField('Email', max_length=100, unique=True)
    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)
    objects = UserManager()
    USERNAME_FIELD = 'username'


#Items

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name',max_length=20, unique=True)
    stock = models.IntegerField('Stock')
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='item', on_delete=models.CASCADE,)
 #   user = models.OneToOneField(User, verbose_name='related user', on_delete=models.CASCADE)

#Transaction

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    input =models.BooleanField(default=True)#Si es verdadero hay entrada de productos
                                            #si es falsa hay salida de productos
    amount = models.IntegerField()
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    item = models.ForeignKey(Item,related_name='transaction', on_delete=models.CASCADE)
