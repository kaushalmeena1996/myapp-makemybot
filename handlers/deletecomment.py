#deletecomment.py
"""Contains class defination for handler class DeleteCommentHandler."""

from blog import BlogHandler
from models.comment import COMMENT

class DeleteCommentHandler(BlogHandler):
    """Handler for DELETING a comment post of user."""

    def get(self, comment_id):
        """Validates the posted comment's form information for
           errors and accordingly deletes the values of appropriate
           entities and redirects the page."""

        if self.user:
            comment = COMMENT.by_id(int(comment_id))

            if comment:
                if comment.user_id == str(self.user.key().id()):
                    comment.delete()

                    referrer = self.request.headers.get('referer')
                    if referrer:
                        self.redirect(referrer)
                    else:
                        self.redirect('/')
                else:
                    page_error = "ERROR 500 : You don't own this comment."
                    self.render("error.html",
                                page_error = page_error,
                                username = self.user.username,
                                page_title = "ERROR")
            else:
                page_error = "ERROR 404 : Comment post not found."
                self.render("error.html",
                            page_error = page_error,
                            username = self.user.username,
                            page_title= "ERROR")

        else:
            self.redirect("/signin")
