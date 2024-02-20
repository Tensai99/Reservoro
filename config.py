import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI ='mysql://root:root@localhost/restaurant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
