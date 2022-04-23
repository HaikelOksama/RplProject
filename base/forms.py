from dataclasses import field
from django.forms import ModelForm
from .models import Organisasi, Event, Feed, UserProfile, Topic
from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'interest' : forms.CheckboxSelectMultiple(),
        }
 


class OrganisasiForm(ModelForm):
    class Meta:
        model = Organisasi
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Masukkan nama Organisasi anda'}),
            'description' : forms.Textarea(attrs={'placeholder' : 'Jelaskan Organisasi anda'})
            
        }
        exclude = ['host',]

class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(ModelForm):
    class Meta:
        model = Event
        field = '__all__'
        widgets = {
            'jadwal' : forms.DateTimeInput(attrs={'type':'datetime-local'}),
            
        }
        exclude = ['organisasi',]

class FeedForm(ModelForm):
    class Meta:
        model = Feed
        field = '__all__'
        exclude = ['organisasi',]


