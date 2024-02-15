import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI ='mysql://root:root@localhost/restaurant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTMAN_MAILER_API_KEY = "PMAK-65cb6a918a25cc0001fb39ec-3fd8966aa5b3debfe243b74991582008d9"
