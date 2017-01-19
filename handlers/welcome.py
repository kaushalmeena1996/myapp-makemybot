#welcome.py
"""Contains class defination for handler class WelcomeHandler."""

import blog

class WelcomeHandler(blog.BlogHandler):
    """Handler for WELCOME page which is showed to users after login."""

    def get(self):
        """Renders WELCOME page if user has logged in otherwise
           renders SIGN-IN page."""

        if self.user:
            self.render("welcome.html",
                        input_username = self.user.username,
                        username = self.user.username,
                        page_title = "WELCOME")
        else:
            self.redirect("/signin")
