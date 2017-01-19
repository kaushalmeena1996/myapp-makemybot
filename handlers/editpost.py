#editpost.py
"""Contains class defination for handler class EditPostHandler."""

from blog import BlogHandler
from models.post import POST

class EditPostHandler(BlogHandler):
    """Handler for EDITING a blog post of user."""

    def get(self, post_id):
        """Renders EDIT-POST page if user has logged in after querying
           appropriate data otherwise redirects to SIGN-IN page."""

        if self.user:
            post = POST.by_id(int(post_id))
            if post:
                if post.user_id == str(self.user.key().id()):
                    self.render("editpost.html",
                                post_subject = post.post_subject,
                                post_content = post.post_content,
                                username = self.user.username,
                                page_title = "EDIT-POST")
                else:
                    page_error = "ERROR 500 : You don't own this post."
                    self.render("error.html",
                                page_error = page_error,
                                username = self.user.username,
                                page_title = "ERROR")
            else:
                page_error = "ERROR 404 : Blog post not found."
                self.render("error.html",
                            page_error = page_error,
                            username = self.user.username,
                            page_title = "ERROR")

        else:
            self.redirect("/signin")

    def post(self, post_id):
        """Checks the posted blog post's form information for
           errors and accordingly changes the values of appropriate
           entities and redirects the page."""

        post_subject = self.request.get("subject")
        post_content = self.request.get("content")

        if post_subject and post_content:
            post = POST.by_id(int(post_id))
            
            if post.user_id == str(self.user.key().id()):
                post.post_subject = post_subject
                post.post_content = post_content
                post.put()
                self.redirect("/mypost")
            else:
                page_error = "ERROR 500 : You don't own this post."
                self.render("error.html",
                            page_error = page_error,
                            username = self.user.username,
                            page_title = "ERROR")
            
        else :
            err_msg = "Both SUBJECT and CONTENT can't be left empty."
            self.render("editpost.html",
                        err_msg = err_msg,
                        post_subject = post_subject,
                        post_content = post_content,
                        page_title = "EDIT-POST")
