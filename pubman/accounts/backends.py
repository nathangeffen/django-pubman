'''Backend to allow email login.

From Djangosnippets:
http://djangosnippets.org/snippets/1001/

Classes:
    EmailOrUsernameModelBackend: Allow users to login with email or username.

'''

from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(object):
    '''Allows users to login with username or email address.
    '''
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
        except User.MultipleObjectsReturned:
            user = User.objects.filter(**kwargs)[0]
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
