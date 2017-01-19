#deletepost.py
"""Contains class defination for handler class DeletePostHandler."""

from blog import BlogHandler
from models.post import POST

class DeletePostHandler(BlogHandler):
    """Handler for DELETING a blog post of user."""

    def get(self, post_id):
        """Validates the posted blog post's form information for
           errors and accordingly deletes the values of appropriate
           entities and redirects the page."""

        if self.user:
            post = POST.by_id(int(post_id))
            if post:
                if post.user_id == str(self.user.key().id()):
                    if post_id in self.user.liked_post:
                        self.user.liked_post.remove(post_id)
                        self.user.put()
                    post.delete()

                    referrer = self.request.headers.get('referer')
                    if referrer:
                        self.redirect(referrer)
                    else:
                        self.redirect('/')
                else:
                    page_error = "ERROR 500 : You don't own this post."
                    self.render("error.html",
                                page_error = page_error,
                                username = self.user.username,
                                page_title= "ERROR")
                    
            else:
                page_error = "ERROR 404 : Blog post not found."
                self.render("error.html",
                            page_error = page_error,
                            username = self.user.username,
                            page_title= "ERROR")

        else:
            self.redirect("/signin")
