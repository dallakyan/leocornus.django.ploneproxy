
# backends.py

"""
Django authentication backend implementation for ploneproxy.
"""

import urllib2

from django.db import connection
from django.contrib.auth.models import User

from leocornus.django.ploneproxy.auth.models import PloneAuthenState

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class PloneModelBackend(object):
    """
    Authenticates against a Plone site!
    """

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):

        ploneUser = self.authPloneUser(username, password)
        if ploneUser:
            cookieName, cookieValue, fullName, email = ploneUser
            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                # create a user object for this new user.
                # save first name, email, ...
                user = User.objects.create(username=username, email=email)
                user.set_unusable_password()

            # setup the cookie object based on the user id.
            ploneCookie = PloneAuthenState(user_id=user.id, status='valid',
                                           cookie_name=cookieName,
                                           cookie_value=cookieValue)
            ploneCookie.save()
            return user
        elif lockout:
            # Plone user locked out, provide proper message!
            # ask for password reset process.
            # return the user object with different cookie value!
            return None
        else:
            # not valid plone user
            return None

    def authPloneUser(self, username, password):

        #ploneAuthUrl = 'http://localhost:8080/default_site/ctsAccessAuthenticate'
        #f = urllib2.urlopen('%s?username=%s&password=%s' % \
        #                    (ploneAuthUrl, username, password))
        #result = f.read()
        result = '__ac<SPLIT>HI76Laxx8zTZE6Omb4uvNnadUg8gY2hlbnNl'
        cookieName, cookieValue = result.split('<SPLIT>')
        fullName = ''
        email = ''

        return (cookieName, cookieValue, fullName, email)

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None