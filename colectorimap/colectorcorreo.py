#!/usr/bin/env python
# -*- coding: latin-1 -*-
import imaplib,email,os
import re
import psycopg2
import datetime
import pdb
from stripogram import html2text
###############################################################
#colectorcorreo.py: cutrescript que recolecta todo lo que hay
#en una casilla de correo y lo inserta en la bdd de Django.
#Version basica , sin control de errores !
#Ramito2009
###############################################################

#Definimos los parametros de conexion de la BDD
conn = psycopg2.connect("\
        dbname='djangodb'\
        user='djangouser'\
        host='localhost'\
	password='vayapassword'\
");

c = conn.cursor()
#Conexion contra servidor

M = imaplib.IMAP4("172.17.1.50")
#Login con usuario y pass
M.login("problemas","novanadayavatodo")
#Selecciona mensajes , y retorna el numero de mensajes totales
M.select()

typ,busqueda = M.search(None, 'ALL')
#typ,busqueda=M.fetch(1,('RFC822'))
for num in busqueda[0].split():
	typ,remitente = M.fetch(num,'(BODY[HEADER.FIELDS (FROM)])')
	#encontramos la direccion de la persona que envia la incidencia
	m = re.search('(\w+@\w+(?:\.\w+)+)',remitente[0][1])
	direccion = m.group(0)
	##print (direccion)
	##print ("------------------------------------------")
	m = re.sub('From: ','',remitente[0][1])
	n = re.sub('<(\w+@\w+(?:\.\w+)+)>','',m)
	remitente = n
	##print (remitente)
	##print ("------------------------------------------")
	typ,asunto =  M.fetch(num,'(BODY[HEADER.FIELDS (SUBJECT)])')
	#Quitamos la palabra "Subject" por un espacio en blanco
	m = re.sub('^Subject: ','',asunto[0][1])
	textoasunto = m
	##print (textoasunto)
	##print ("------------------------------------------")
	typ,cuerpo = M.fetch(num,'(BODY[TEXT])')
	texto = cuerpo[0][1]
	#la parte del update
	propietarioI=remitente
	emailpropietarioI=direccion
	asuntoI=textoasunto
	#Esto hace que el cuerpo se pueda insertar de manera correcta...
	#textoI= unicode(texto,"latin-1")
	textoI2=unicode(html2text(texto,ignore_tags=("img",),indent_width=4,page_width=80),"latin-1")
	fechaI=datetime.datetime.now()
	#
	#Insertar la incidencia como pendiente , mirar siempre que sea relativa al estado que toda de los pendientes...
	#
	relestado_idI='1'
	c.execute("INSERT INTO gestorincidencias_incidencias (propietario,emailpropietario,asunto,texto,fecha,relestado_id) VALUES (%s,%s,%s,%s,%s,%s)",(propietarioI,emailpropietarioI,asuntoI,textoI2,fechaI,relestado_idI))
	conn.commit()
	M.store(num, '+FLAGS', '\\Deleted')
M.expunge()
M.close()
M.logout()
