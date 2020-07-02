from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm,PasswordChangeForm
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User=get_user_model()

class login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', 'placeholder': 'Enter Username'}
    ), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control ', 'placeholder': 'Enter password'}
    ), required=True, max_length=50)
    
class PasswordChangeForm(PasswordChangeForm):
     def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
        self.fields['new_password1'].label = 'New Password'

        for fieldname in ['new_password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = 'Confirm Password'
            
            
class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email"), max_length=254)




class SetPasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        print(password1)
        if password1 and password2:
            if len(password1) < 6:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
            if len(password2) < 6:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
            
        return password2


# Your password can't be too similar to your other personal information.
# Your password must contain at least 8 characters.
# Your password can't be a commonly used password.
# Your password can't be entirely numeric.
            

    