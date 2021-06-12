from allauth.account.adapter import DefaultAccountAdapter

# Reference: https://stackoverflow.com/questions/53969386/how-to-save-extra-fields-on-registration-using-custom-user-model-in-drf-django
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.gender = data.get('gender')
        user.save()
        return user
