#newpost.py
"""Contains class defination for handler class NewPostHandler."""

from blog import BlogHandler
from models.post import POST
from models.comment import COMMENT


class NewPostHandler(BlogHandler):
    """Handler for NEW-POST page which allows users to create
       new blog posts."""

    def get(self):
        """Renders NEW-POST page if user has logged in otherwise
           renders SIGN-IN page."""

        if self.user:
            self.render("newpost.html",
                        username = self.user.username,
                        page_title = "NEW-POST")
        else:
            self.redirect("/signin")

    def post(self):
        """Validates the posted blog post's form information for
           errors and accordingly creates the appropriate entities
           and redirects the page."""

        post_subject = self.request.get("subject")
        post_content = self.request.get("content")

        if post_subject and post_content:
            post = POST.create_post(user_id = str(self.user.key().id()),
                                    post_subject = post_subject,
                                    post_content = post_content)
            post.put()
            self.redirect("/post/" + str(post.key().id()))
        else :
            self.render("newpost.html",
                        err_msg = "Both SUBJECT and CONTENT can't be left empty.",
                        post_subject = post_subject,
                        post_content = post_content,
                        page_title = "NEW-POST")
