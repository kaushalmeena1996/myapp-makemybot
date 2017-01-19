# [Project : Item Catalog]

## [ Synopsis ]

A web application that provides a list of gameitems within a variety of categories and integrates third-party user registration and authentication.

## [ Prerequisities ]

- Python
  - https://www.python.org/downloads/
- Python Libraries
  - Flask==0.9
    - http://flask.pocoo.org/docs/0.11/installation/
  - oauth2client==3.0.0
    - https://oauth2client.readthedocs.io/en/latest/
  - httplib2==0.9.2
    - https://pypi.python.org/pypi/httplib2
  - SQLAlchemy==1.0.15
    - http://www.sqlalchemy.org/download.html
  - requests==2.11.1
    - http://docs.python-requests.org/en/master/user/install/

## [ Usage ]
As the app uses Google for authentication as the next step you have to obtain a client id and client secret from Google and Facebook:

For Google

- Go to the Google Developer Console.
- Create a new project.
- Go to APIs & auth - Consent screen and select a valid Email address.
- Go to APIs & auth - Credentials and create a new Client ID.
- Enter http://localhost:8000/oauth2callback/ in the Authorized redirect URIs field.
- Click DownloadJSON icon and save it as 'g_client_secrets.json' in secret folder.

For Facebook

- Go to Facebook Developers and login with your account. Select Add a New App from the dropdown in the upper right: When asked to select a platform, click Basic Setup
- Provide a Display Name and Contact Email. Select a Category and click Create App ID.
- On the Product Setup page that follows, click Get Started next to Facebook Login: Scroll down to the Client OAuth Settings section and enter the following URL in the Valid OAuth redirect URIs field: http://localhost:8000/oauth2callback Click on Save Changes.
- Select Settings in the left nav. Click Show to reveal the App Secret. (You may be required to re-enter your Facebook password.)
- Save a copy of the App ID and App Secret in 'app-id' and 'app-secret' fields of 'fb_client_secrets.json' in secret folder.
- On the same Basic Settings page, scroll down and click Add Platform: Select Website in the pop-up: In the Site URL field, enter the following: http://localhost:8000
- Click Yes on the App Review page of your app to make it available to the public.

Next you have to create the game-catalog.db To do so run in database folder
~~~~
python database_setup.py
~~~~

Optional : To fill dummyrecords in database run in database folder
~~~~
python dummyrecords.py
~~~~
## [ Run ]

To start the app simply run
~~~~
python server.py
~~~~
