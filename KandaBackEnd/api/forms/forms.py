from django import forms
from .models import User

class UserRegistrationForm(forms.Form):
    """
    Formulario para el registro de nuevos usuarios.
    """
    username = forms.CharField(label='Nombre de usuario', max_length=150, required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, required=True)
    
    def clean_username(self):
        """
        Valida que el nombre de usuario no exista ya en la base de datos.
        """
        username = self.cleaned_data.get('username')
        if User.objects(username=username).first():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def clean_email(self):
        """
        Valida que el correo electrónico no exista ya en la base de datos.
        """
        email = self.cleaned_data.get('email')
        if User.objects(email=email).first():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean(self):
        """
        Valida que las dos contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        
        return cleaned_data


class UserLoginForm(forms.Form):
    """
    Formulario para el inicio de sesión de usuarios.
    """
    username = forms.CharField(label='Nombre de usuario o correo electrónico', required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)