#blog.py
"""Contains class defination for handler class MyPostHandler."""

from google.appengine.ext import db

from blog import BlogHandler
from models.post import POST
from models.comment import COMMENT

class MyPostHandler(BlogHandler):
    """Handler for MY-POST page which show users their own blog posts."""

    def get(self):
        """Renders MY-POST page if user has logged in after querying
           appropriate data otherwise renders SIGN-IN page."""

        if self.user:
            posts = POST.by_user_id(str(self.user.key().id()))
            comments = []

            for post in posts:
                query_comments = db.GqlQuery("SELECT * FROM COMMENT "
                                             "WHERE post_id = '%s'"
                                             % str(post.key().id()))
                if query_comments:
                    for comment in query_comments:
                        comments.append(comment)

            liked_post = []
            for post in posts:
                if str(post.key().id()) in self.user.liked_post:
                    liked_post.append(str(post.key().id()))

            self.render("mypost.html",
                        posts = posts,
                        comments = comments,
                        liked_post = liked_post,
                        user_id = str(self.user.key().id()),
                        username = self.user.username,
                        page_title = "MY-POST")
        else:
            self.redirect("/signin")
