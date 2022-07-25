from forum.celery import app
from forum_comments.models import PasswordToken



'''
Tasks managed by celery in celery.py
'''

@app.task
def checkingtoken():
    PasswordToken.check_token()
    return True

