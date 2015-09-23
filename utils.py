__author__ = 'thxer'

from flask import session
from flask import g, request, redirect, url_for
from functools import wraps

def is_logged(session) :
    try :
        if session['login'] and session['username']:
            if session['login'] == True :
                return True
        else :
            return False
    except KeyError:
        return False

