from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Formulário modifcado de registro de usuário
# Adiciona os campos: first_name, last_name e email
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um email válido.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        labels = {
            'username': 'Nome de usuário',
            'email': 'Endereço de email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'password1': 'Senha',
            'password2': 'Confirmação da senha'
        }

        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
            'email': 'Obrigatório. Informe um email válido.',
            'first_name': 'Obrigatório.',
            'last_name': 'Obrigatório.',
            'password1': 'Sua senha não pode ser muito parecida com suas outras informações pessoais.',
            'password2': 'Digite a mesma senha novamente para verificação.'
        }

# Formulário modifcado de login de usuário
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )