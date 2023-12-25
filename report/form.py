from django import forms
from account.models import CustomUser

class MessageForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        max_length=100,
        help_text='Enter your full name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='Email',
        help_text='Enter a valid email address',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        labels = {
            'username': 'Enter user name',
            'password': 'Enter Password',
        }
       
