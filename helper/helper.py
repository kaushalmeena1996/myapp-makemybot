#helper.py
"""Python function definations for helper function."""

#python modules
import codecs
import re
import hashlib
import hmac
import random
import string

from secret.secret import get_secret

# secret string
SECRET = get_secret()

# regular expression patterns
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# helper function definations
def make_salt(length=5):
    """Creates random string of length same as passed parameter."""

    salt = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in xrange(length))
    return salt


def make_password_hash(username, password, salt=None):
    """Creates hash using passed parameters."""

    if not salt:
        salt = make_salt()
    hash_val = hashlib.sha256(username + password + salt).hexdigest()

    return '%s,%s' % (salt, hash_val)


def validate_password(username, password, hash_val):
    """Validates username and password using hash value."""

    salt = hash_val.split(',')[0]
    return hash_val == make_password_hash(username, password, salt)


def hash_str(string):
    """Returns a hash value of passed string."""

    return hmac.new(SECRET, string).hexdigest()


def read_secure_cookie(key):
    """Reads cookie from browser for passed parameters."""

    cookie_val = request.cookies.get(key)
    return cookie_val and check_secure_val(cookie_val)


def make_secure_val(string):
    """Creates a password hash using passed string."""

    return "%s|%s" % (string, hash_str(string))


def check_secure_val(hash_val):
    """Checks if passed hash value is correct or not."""

    val = hash_val.split('|')[0]
    if hash_val == make_secure_val(val):
        return val


def valid_username(username):
    """Validates username using regular expressions."""

    return USERNAME_RE.match(username)


def valid_password(password):
    """Validates password using regular expressions."""

    return PASSWORD_RE.match(password)


def valid_email(email):
    """Validates email using regular expressions."""

    return EMAIL_RE.match(email)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def show_pagination00 (action, page, last, pLimit):
    response = "<table class='w3-center w3-text-col-red w3-margin-bottom'><tr><td>";

    response += "<button "
    if page == 1: 
        response += "disabled "
    response += "onclick='botAction(%d, 1, this)' class='w3-xlarge w3-botButton'>[ <i class='fa fa-angle-double-left'></i> ]</button>" % action
    
    response += "<button "
    if page == 1: 
        response += "disabled " 
    response += "onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton'>[ <i class='fa fa-angle-left'></i> ]</button>" % (action, (page-1))
                
    if (page-1) > pLimit:
        response += "<button onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton w3-padding-left'>...</button>" % (action, (page-pLimit))
      
    if (page-1) < pLimit:
        counter = 1
    else:
        counter = (page-pLimit)

    end = min((page+pLimit), last)

    for counter in range(1, end + 1):
        response += "<button onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton w3-padding-left'>" % (action, counter) 
        if counter == page:
            response += "<u>%d</u>" % counter
        else:
            response += str(counter)
        response += "</button>"
                
    if (last-page) > pLimit:
        response += "<button onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton w3-padding-left'>...</button>" % (action, (page+pLimit))
                
    response += "<button " 
    if page == last:
         response += "disabled "
    response += "onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton w3-padding-left'>[ <i class='fa fa-angle-right'></i> ]</button>" % (action, (page+1))
    
    response += "<button " 
    if(page == last): 
        response += "disabled "
    response += " onclick='botAction(%d, %d, this)' class='w3-xlarge w3-botButton'>[ <i class='fa fa-angle-double-right'></i> ]</button>" % (action, last)
    
    response += "</td></tr></table>"

    return response

def show_pagination01 (action, page, last, pLimit):
    response = "<tr><td class='w3-center w3-full-width w3-text-col-darkblue'>";

    response += "<button "
    if page == 1: 
            response += "disabled "
    response += "onclick='%s(1, this)' class='w3-xlarge w3-qButton'>[ <i class='fa fa-angle-double-left'></i> ]</button>" % action

    response += "<button "
    if page == 1: 
            response += "disabled " 
    response += "onclick='%s(%d, this)' class='w3-xlarge w3-qButton'>[ <i class='fa fa-angle-left'></i> ]</button>" % (action, (page-1))

    if (page-1) > pLimit:
            response += "<button onclick='%s(%d, this)' class='w3-xlarge w3-qButton w3-padding-left'>...</button>" % (action, (page-pLimit))

    if (page-1) < pLimit:
            counter = 1
    else:
            counter = (page-pLimit)

    end = min((page+pLimit), last)
    
    for counter in range(1, end + 1):
            response += "<button onclick='%s(%d, this)' class='w3-xlarge w3-qButton w3-padding-left'>" % (action, counter) 
            if counter == page:
                    response += "<u>%d</u>" % counter
            else:
                    response += str(counter)
            response += "</button>"

    if (last-page) > pLimit:
            response += "<button onclick='%s(%d, this)' class='w3-xlarge w3-qButton w3-padding-left'>...</button>" % (action, (page+pLimit))

    response += "<button " 
    if page == last:
            response += "disabled "
    response += "onclick='%s(%d, this)' class='w3-xlarge w3-qButton w3-padding-left'>[ <i class='fa fa-angle-right'></i> ]</button>" % (action, (page+1))

    response += "<button " 
    if(page == last): 
            response += "disabled "
    response += " onclick='%s(%d, this)' class='w3-xlarge w3-qButton'>[ <i class='fa fa-angle-double-right'></i> ]</button>" % (action, last)

    response += "</td></tr>"

    return response
        

