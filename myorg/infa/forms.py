from django import forms
from django.contrib.auth.hashers import make_password

from .models import InfaModelProfile, InfaUser


class InfaUserForm(forms.ModelForm):
    class Meta:
        model = InfaUser
        fields = ['name', 'email', 'location', 'bio']


class InfaModelProfileForm(forms.ModelForm):
    class Meta:
        model = InfaModelProfile
        fields = [
            'age',
            'gender',
            'category',
            'experience',
            'height_cm',
            'instagram_handle',
            'portfolio_image_url',
            'gallery_image_1_url',
            'gallery_image_2_url',
            'gallery_image_3_url',
            'featured',
        ]


class SignupForm(forms.Form):
    ROLE_CHOICES = [
        ('model', 'Model'),
        ('organizer', 'Organizer'),
    ]

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    location = forms.CharField(max_length=120, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    age = forms.IntegerField(required=False, min_value=1)
    gender = forms.CharField(max_length=20, required=False)
    category = forms.CharField(max_length=50, required=False)
    experience = forms.CharField(widget=forms.Textarea, required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if InfaUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        if role == 'model':
            required_fields = ['age', 'gender', 'category', 'experience']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for model accounts.')

        return cleaned_data

    def save(self):
        user = InfaUser.objects.create(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password']),
            role=self.cleaned_data['role'],
            location=self.cleaned_data.get('location', ''),
            bio=self.cleaned_data.get('bio', ''),
        )

        if user.role == 'model':
            InfaModelProfile.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                category=self.cleaned_data['category'],
                experience=self.cleaned_data['experience'],
            )

        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
