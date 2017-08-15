# helper.py
"""Python function definations for helper function."""

# python modules
import re
import os
import hashlib

# regular expression patterns
USERNAME_RE = re.compile(
    r"^[a-zA-Z0-9_@!#\$\^%&*()+=\-\[\]\\\';,\.\/\{\}\|\":<>\?]{3,20}$")
PASSWORD_RE = re.compile(
    r"^[a-zA-Z0-9_@!#\$\^%&*()+=\-\[\]\\\';,\.\/\{\}\|\":<>\?]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# page colors
PAGE_COLOR = {'home': 'grey',
              'login': 'purple',
              'register': 'purple',
              'chatbots': 'red',
              'guide': 'blue',
              'faqs': 'green',
              'contact': 'orange',
              'chat': 'darkred',
              'teach': 'darkblue',
              'settings': 'darkgreen',
              'embed': 'darkorange'}

# extention folder
EXTENSION_FOLDER = {'rive': 'brain',
                    'txt': 'log',
                    'jpg': 'avtaar',
                    'jpeg': 'avtaar',
                    'png': 'avtaar',
                    'gif': 'avtaar'}

# helper function definations


def valid_username(username):
    """Validates username using regular expressions."""

    return USERNAME_RE.match(username)


def valid_password(password):
    """Validates password using regular expressions."""

    return PASSWORD_RE.match(password)


def valid_email(email):
    """Validates email using regular expressions."""

    return EMAIL_RE.match(email)


def generate_context(request, title):
    page_color = PAGE_COLOR[title]
    context = {
        'pageTitle': title,
        'pageColor': 'bg-{}'.format(page_color),
        'buttonColor': 'btn-{}'.format(page_color),
        'textColor': 'text-{}'.format(page_color)
    }

    if request.user.is_authenticated:
        context['username'] = request.user.get_username()

    return context


def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    folder = EXTENSION_FOLDER[extension]
    hashid = hashlib.sha256(str(instance.user.id)).hexdigest()
    filename = "%s_%s.%s" % (folder, hashid, extension)
    return os.path.join(folder, filename)
