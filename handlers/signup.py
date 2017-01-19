#signup.py
"""Contains class defination for handler class SignUpHandler."""

from blog import BlogHandler
from models.user import USER
from helper.helper import valid_username, valid_password, valid_email

class SignUpHandler(BlogHandler):
    """Handler for SIGN-UP page which allows users to register."""

    def get(self):
        """Renders SIGN-UP page if user has not registered otherwise
           renders WELCOME page."""

        if self.user:
            self.redirect("/welcome")
        else:
            self.render("signup.html", page_title = "SIGN-UP")

    def post(self):
        """Validates user sign-up's form information for errors and
           accordingly redirects the page."""

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        name = self.request.get("name")
        email = self.request.get("email")

        err_username = ''
        err_password = ''
        err_verify = ''
        err_email = ''

        signup_err = False

        if not valid_username(username):
            err_username = "Please enter valid username !"
            signup_err = True

        if not valid_password(password):
            err_password = "Password must contain atleast 3 characters !"
            signup_err = True

        if not valid_password(verify):
            err_verify = "Password must contain atleast 3 characters !"
            signup_err = True

        elif not password == verify:
            err_verify = "Password don't match !"
            signup_err = True

        if email:
            if not valid_email(email):
                err_email = "Please enter valid e-mail !"
                signup_err = True

        template_values = {
            'page_title': 'SIGN-UP',
            'err_username': err_username,
            'err_password': err_password,
            'err_verify': err_verify,
            'err_email': err_email,
            'input_username': username,
            'input_password': password,
            'input_verify': verify,
            'input_email': email,
            'input_name': name,
        }

        if signup_err == False:
            user = USER.by_username(username)
            if user:
                self.render("signup.html",
                            err_username = "Specified username alredy exists.",
                            page_title = "SIGN-UP")
            else:
                user = USER.register(username,
                                     password,
                                     name,
                                     email)
                user.put()
                self.login(user)
                self.redirect("/welcome")
        else:
            self.render_template("signup.html", template_values)
