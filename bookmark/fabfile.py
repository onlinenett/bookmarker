import socket
import os
import pwd
import getpass

from fabric.api import *
from fabric.contrib import *

# Get the current running user id
uid = getpass.getuser()

env.hosts = ['funkhq.com']

# Global definitions
SERVERUSER = 'funkomg'
PROJECTPATH = '/home/funkomg'
APPNAME = 'omgmark'
DEPLOYPATH = '%s/app/' % (PROJECTPATH)
RUNPATH = '%s/run/' % (PROJECTPATH)

def hostname():
    run('uname -a')

def gitpull():
    local('git pull')

def start():
    local('python manage.py runserver', capture = False)

def startwsgi():
    if (socket.gethostname() == 'funkhq.com' and (uid == SERVERUSER)):
        local('python manage.py runfcgi socket=%s/funkomg.sock pidfile=%s/run/funkomg.pid method=threaded' % (RUNPATH))

def stopwsgi():
    if (socket.gethostname() == 'funkhq.com' and (uid == SERVERUSER)):
        local('kill `cat %s/%s.pid`' % (RUNPATH, APPNAME), capture = False)

def deploy():
    if (socket.gethostname() == 'funkhq.com' and (uid == SERVERUSER)):
        stopwsgi()
        gitpull()
        startwsgi()
    else:
        gitpull()
        start()

