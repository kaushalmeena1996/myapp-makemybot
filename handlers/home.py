#home.py
"""Contains class defination for handler class MainHandler."""

from google.appengine.ext import db

from blog import BlogHandler
from models.post import POST
from models.comment import COMMENT

class MainHandler(BlogHandler):
    """Handler for HOME page which displays the blog posts along
       with their comments."""

    def get(self):
        """Renders HOME page after querying appropriate data for
           comments and post."""

        posts = db.GqlQuery("SELECT * FROM POST ORDER BY created DESC LIMIT 20")
        comments = []
        for post in posts:
            query_comments = db.GqlQuery("SELECT * FROM COMMENT "
                                         "WHERE post_id = '%s' "
                                         "LIMIT 10"
                                         % str(post.key().id()))
            if query_comments:
                for comment in query_comments:
                    comments.append(comment)

        if self.user:
            liked_post = []
            for post in posts:
                if str(post.key().id()) in self.user.liked_post:
                    liked_post.append(str(post.key().id()))

            self.render("home.html",
                        posts = posts,
                        comments = comments,
                        liked_post = liked_post,
                        user_id = str(self.user.key().id()),
                        username = self.user.username,
                        page_title = "HOME")
        else:
            self.render("home.html",
                        posts = posts,
                        comments = comments,
                        page_title = "HOME")
