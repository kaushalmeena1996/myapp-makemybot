#like.py
"""Contains class defination for handler class LikeHandler."""

from blog import BlogHandler
from models.post import POST

class LikeHandler(BlogHandler):
    """Handler for LIKING a blog post."""

    def get(self, post_id):
        """Adds the passed post_id in user's list of liked_post
           and redirects the page accordingly."""

        if self.user:
            post = POST.by_id(int(post_id))
            if post:
                if not post.user_id == str(self.user.key().id()):
                    self.user.liked_post.append(post_id)
                    self.user.liked_post = list(set(self.user.liked_post))
                    self.user.put()
                    post.put()

                    referrer = self.request.headers.get('referer')
                    if referrer:
                        self.redirect(referrer)
                    else:
                        self.redirect('/')
                else:
                    page_error = "ERROR 500 : You can't like your own post."
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
