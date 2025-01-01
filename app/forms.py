from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'Enter your full name',
        }),
        error_messages={
            'required': 'Please enter your name'
        }
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email address',
        }),
        error_messages={
            'required': 'Please enter a valid email address',
            'invalid': 'Please enter a valid email address'
        }
    )
    
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'subject',
            'class': 'form-control',
            'placeholder': "What's this about?",
        }),
        error_messages={
            'required': 'Please enter a subject'
        }
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-control',
            'placeholder': 'Type your message here...',
            'rows': 5,
        }),
        error_messages={
            'required': 'Please enter your message'
        }
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def clean(self):
        cleaned_data = super().clean()
        print("\nForm Cleaning:")
        print(f"Cleaned data: {cleaned_data}")
        return cleaned_data 