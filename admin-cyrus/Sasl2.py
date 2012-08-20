# -*- Mode: Python; tab-width: 4 -*-
#
# Python Sasl2 db backend
#
# Copyright (C) 2003-2006 Gianluigi Tiesi <sherpya@netfarm.it>
# Copyright (C) 2003-2006 NetFarm S.r.l.  [http://www.netfarm.it]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# ======================================================================

__version__= '0.4'
__doc__="""Sasl2 module dbm backend, provides 'atomic' operation around sasldb"""
__all__ = [ 'deleteuser',
            'createuser',
            'setpass',
            'getuser',
            'getuserlist' ]

SASLDB='/etc/sasldb2'
SASLDBMODE=660
KEY='userPassword'

OBSOLETES = [ 'cmusaslsecretCRAM-MD5',
              'cmusaslsecretDIGEST-MD5',
              'cmusaslsecretPLAIN' ]

ALLKEYS = [ KEY ] + OBSOLETES

SEP='\x00'

import anydbm
from socket import gethostname

### Settable at run time using Sasl2.realm = 'foobar'
realm = gethostname()

if not realm:
    raise Exception, 'Sasl2: Cannot find realm, broken gethostname()?'

def _opendb():
    return anydbm.open(SASLDB, 'c', SASLDBMODE)

def _compose(user, key):
    return SEP.join([user, realm, key])

def _deloldkeys(db, user):
    ### Delete old keys
    for ob in OBSOLETES:
        mykey = _compose(user, ob)
        try:
            del db[mykey]
        except: pass
    db.sync()

def setpass(user, password):
    db = _opendb()

    _deloldkeys(db, user)

    ### Add new entry
    mykey = _compose(user, KEY)
    try:
        db[mykey] = password
    except:
        db.close()
        raise Exception, 'Sasl2: Error Inserting key in the sasldb'
    db.close()

def createuser(user, password):
    db = _opendb()
    userexists = 0;

    ### Check first old keys
    for ob in ALLKEYS:
        mykey = _compose(user, ob)
        if db.has_key(mykey):
            userexists = 1
            break

    if userexists:
        db.close()
        raise Exception, 'Sasl2: User already exists'

    ### Set the key
    mykey = _compose(user, KEY)
    try:
        db[mykey] = password
    except:
        db.close()
        raise Exception, 'Sasl2: Error Setting key in the sasldb'
    db.close()

def deleteuser(user):
    db = _opendb()

    _deloldkeys(db, user)

    ### Delete main key
    mykey = _compose(user, KEY)
    try:
        del db[mykey]
    except: pass

    db.close()

def getuser(user):
    db = _opendb()
    username = _compose(user, KEY)
    res = None
    if db.has_key(username):
        res = { 'username': user,
                'password': db[username],
                'realm'   : realm }

    db.close()
    return res

def getuserlist():
    db = _opendb()

    users = []
    raw = db.keys()
    for u in raw:
        try:
            users.append(u.split(SEP, 1)[0])
        except: pass

    db.close()
    return users
