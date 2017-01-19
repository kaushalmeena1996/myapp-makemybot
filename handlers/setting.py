#setting.py
"""Contains class defination for handler class SettingHandler."""

from blog import BlogHandler
from models.post import POST
from models.comment import COMMENT
from helper.helper import  valid_password, valid_email


class SettingHandler(BlogHandler):
    """Handler for SETTING page a which allows users to change
       their profile settings and passwords and also allows users
       to delete all their post, comments or even acount."""

    def get(self):
        """Renders SETTING page in if user has logged in otherwise
           redirects to SIGN-IN page after fetching appropriate data."""

        if self.user:
            self.render("setting.html",
                        username = self.user.username,
                        input_name = self.user.name,
                        input_email = self.user.email,
                        page_title = "SETTING")
        else:
            self.redirect("/signin")

    def post(self):
        """Checks the posted setting's form information for errors
           and accordingly changes the values of appropriate entities
           and redirects the page. Also perform the task of deleting
           all their posts, comments or even account if specified."""


        name = self.request.get("name")
        email = self.request.get("email")
        password = self.request.get("password")
        verify = self.request.get("verify")
        delete1 = self.request.get("delete1")
        delete2 = self.request.get("delete2")
        delete3 = self.request.get("delete3")

        setting_err = False
        err_email = ''
        err_password = ''
        err_verify = ''

        if not name == self.user.name:
            self.user.name = name
            self.user.put()

        if not email == self.user.email:
            if not valid_email(email):
                err_email = "Please enter valid e-mail !"
                setting_err = True
            else:
                self.user.email = email
                self.user.put()

        if password and password.strip():
            if not valid_password(password):
                err_password = "Password must contain atleast 3 characters !"
                setting_err = True

            if not valid_password(verify):
                err_verify = "Password must contain atleast 3 characters !"
                setting_err = True

            elif not password == verify:
                err_verify = "Password don't match !"
                setting_err = True

            else:
                password_hash = make_password_hash(self.user.username, password)
                self.user.password_hash = password_hash
                self.user.put()

        template_values = {
            'page_title': 'SETTING',
            'username' : self.user.username,
            'err_email': err_email,
            'err_password': err_password,
            'err_verify': err_verify,
            'input_name': name,
            'input_email': email,
            'input_password': password,
            'input_verify': verify,
        }

        if setting_err == False:
            if delete1:
                comments = COMMENT.by_user_id(str(self.user.key().id()))
                for comment in comments :
                    post = POST.by_id(int(comment.post_id))
                    post.put()
                    comment.delete()

            if delete2:
                posts = POST.by_user_id(str(self.user.key().id()))
                for post in posts :
                    if str(post.key().id()) in self.user.liked_post:
                        self.user.liked_post.remove(str(post.key().id()))
                    self.user.put()
                    comments = COMMENT.by_post_id(str(post.key().id()))
                    for comment in comments :
                        comment.delete()

                    post.delete()

            if delete3:
                comments = COMMENT.by_user_id(str(self.user.key().id()))
                posts = POST.by_user_id(str(self.user.key().id()))
                for post in posts :
                    post.delete()
                for comment in comments :
                    comment.delete()

                self.user.delete()
                self.logout()
                self.redirect("/")
            else:
                self.redirect("/setting")
        else:
            self.render_template("setting.html", template_values)
