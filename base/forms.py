from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room #mesti model
        fields = '__all__'
        exclude =[
            'host','participants'
        ]

