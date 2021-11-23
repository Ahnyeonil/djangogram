from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )
    
    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleand_date["username"]
        
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        raise ValidationError(self.error_message["duplicate_username"])
    
class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password']
        
        labels = {
            'email' : '이메일 주소',
            'name' : '성명',
            'username' : '사용자 이름',
            'password' : '비밀번호'
        }
        
        widgets = {
            'password' : django_forms.PasswordInput(),
        }
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# 기존 코드
# from django.contrib.auth import forms as admin_forms
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

# User = get_user_model()


# class UserChangeForm(admin_forms.UserChangeForm):
#     class Meta(admin_forms.UserChangeForm.Meta):
#         model = User


# class UserCreationForm(admin_forms.UserCreationForm):
#     class Meta(admin_forms.UserCreationForm.Meta):
#         model = User

#         error_messages = {
#             "username": {"unique": _("This username has already been taken.")}
#         }