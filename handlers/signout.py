#signout.py
"""Contains class defination for handler class SignOutHandler."""

from blog import BlogHandler

class SignOutHandler(BlogHandler):
    """Handler for SIGN-OUT page which allows users to logout."""

    def get(self):
        """Logout the user and redirects to HOME page."""
        self.logout()
        self.redirect('/')
