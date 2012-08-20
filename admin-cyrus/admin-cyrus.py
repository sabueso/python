#!/usr/bin/env python
import os,sys,commands,cyruslib
from Sasl2 import createuser, deleteuser, setpass

useradmin="cyrus"
passadmin="pikax1"
conexioncyrus = cyruslib.CYRUS ()

if len(sys.argv) == 1:
        print "Esta aplicacion necesita un parametro para ser ejecutada, pruebe con './admin-cyrus.py ayuda')"
        sys.exit()

elif sys.argv[1] == 'listarusuarios' or sys.argv[1] == 'lu':

	conexioncyrus.login(""+useradmin+"", ""+passadmin+"")
	listado=str(conexioncyrus.lm())
	print listado
	conexioncyrus.logout
	sys.exit()

elif sys.argv[1] == 'crearusuario' or sys.argv[1] == 'cu':
	#print "Creando usuario..."
	if  len(sys.argv) != 4:
		print "Se necesita un nombre de usuario para crear un mailbox EJ: ./admincyrus.py crearusuario pepito passpepito"
		sys.exit()
	usuarionuevo = sys.argv[2]
	conexioncyrus.login (""+useradmin+"", ""+passadmin+"")
	if sys.argv[1] in str(conexioncyrus.lm()):
		print "El usuario ya existe en Cyrus , borrelo para volver a crearlo"
		sys.exit()
	if conexioncyrus.cm("user",""+usuarionuevo+"") == 0:
		print "El usuarios CYRUS no se ha podido crear"
	else:
		print "Usuario CYRUS creado"
	conexioncyrus.logout
	try:
		createuser(sys.argv[2],sys.argv[3])
	except (Exception, 'Sasl2: User already exists'):
		print "Usuario existente en la BD Sasl2"
	else:
		print "Usuario SASL2 creado"
	
	sys.exit()

elif sys.argv[1] == 'borrarusuario' or sys.argv[1] == 'bu':
        if  len(sys.argv) != 3:
                print "Se necesita un nombre de usuario para BORRAR un mailbox EJ: ./admincyrus.py crearusuario pepito"
                sys.exit()
	usuarioaborrar = sys.argv[2]
	conexioncyrus.login(""+useradmin+"", ""+passadmin+"")
	conexioncyrus.sam("user",""+usuarioaborrar+"", "cyrus", "all")
	if conexioncyrus.dm("user",""+usuarioaborrar+"") == 0:
		print "No se ha podido borrar el usuario"
	else:
		print "Usuario borrado"
		conexioncyrus.logout 	
	deleteuser(sys.argv[2])
	sys.exit()

elif sys.argv[1] == 'ayuda':
	print "========================================================================="
	print "./admincyrus.py listarusuarios ---> lista mailboxes cyrus"
	print "./admincyrus.py crearusuario pepito ---> agrega mailbox de cyrus , "
	print "./admincyrus.py borrarusuario pepito ---> agrega mailbox de cyrus , "
	print "========================================================================="
else:

	print "No se reconoce la opcion pasada"

sys.exit(100)
