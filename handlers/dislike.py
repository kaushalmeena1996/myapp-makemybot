#dislike.py
"""Contains class defination for handler class DislikeHandler."""

from blog import BlogHandler
from models.post import POST


class DislikeHandler(BlogHandler):
    """Handler for DISLIKING a blog post."""

    def get(self, post_id):
        """Deletes the passed post_id from user's list of liked_post
           and redirects the page accordingly."""

        if self.user:
            post = POST.by_id(int(post_id))
            if post:
                if not post.user_id == str(self.user.key().id()):
                    if post_id in self.user.liked_post:
                        self.user.liked_post.remove(post_id)
                        self.user.put()
                        post.put()

                    referrer = self.request.headers.get('referer')
                    if referrer:
                        self.redirect(referrer)
                    else:
                        self.redirect('/')
                else:
                    page_error = "ERROR 500 : You can't dislike your own post."
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
