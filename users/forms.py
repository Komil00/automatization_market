from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
class DirectorForm(UserCreationForm):
    class Meta:
        model = Director
        fields = "__all__"
class ManagerForm(UserCreationForm):
    class Meta:
        model = Manager
        fields = "__all__"
