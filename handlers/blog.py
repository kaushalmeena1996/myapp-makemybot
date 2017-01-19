#blog.py
"""Contains class defination for handler class BlogHandler."""

import webapp2

from models.user import USER
from helper.helper import render_str, render_template_str, make_secure_val, check_secure_val   

class BlogHandler(webapp2.RequestHandler):
    """Main handler for BLOG website which is parent of all other
       handler classes."""

    def write(self, *a, **kw):
        """Writes the passed parameters in webpage."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Renders template using passed parameters in webpage."""

        params['user'] = self.user
        return render_str(template, **params)

    def render_template_str(self, template, template_values):
        """Renders template using passed dictionary in webpage."""

        return render_template_str(template, template_values)

    def render(self, template, **kw):
        """Writes template using passed parameters in webpage."""

        self.write(self.render_str(template, **kw))

    def render_template(self, template, template_values):
        """Writes template using passed dictionary in webpage."""

        self.write(self.render_template_str(template, template_values))

    def set_secure_cookie(self, username, val):
        """Sets cookie for current user in browser."""

        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/'
                                         % (username, cookie_val))

    def read_secure_cookie(self, username):
        """Reads cookie from browser for passed parameters."""

        cookie_val = self.request.cookies.get(username)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """Sets cookie in browser for passed parameter."""

        self.user = user
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """Deletes cookie from browser for current user."""

        self.response.headers.add_header('Set-Cookie',
                                         'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """Initializes class's USER entitity from cookie info
           stored in browser."""

        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and USER.by_id(int(user_id))
