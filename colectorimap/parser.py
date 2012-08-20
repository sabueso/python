#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib,email,os
import email
import re
#Definimos los parametros de conexion de la BDD
#Variables que usaremos para pasarle al INSERT los valores
#c = conn.cursor()
#import email
prueba=[]
#Conexion contra servidor
M = imaplib.IMAP4("172.17.1.50")
#Antiguo login , con usuario de sistemas y peticion de pas
#M.login(getpass.getuser(), getpass.getpass())
#Login con usuario y pass
M.login("problemas","novanadayavatodo")
#Selecciona la cantidad de mensajes , y retorna el numero de mensajes totales
M.select()
typ,busqueda = M.search(None, 'ALL')
#typ,busqueda=M.fetch(1,('RFC822'))
for num in busqueda[0].split():
        typ,remitente = M.fetch(num,'(BODY[HEADER.FIELDS (FROM)])')
        #encontramos la direccion de la persona que envia la incidencia 
        m = re.search('(\w+@\w+(?:\.\w+)+)',remitente[0][1])
        direccion=m.group(0)
        print direccion
        print "------------------------------------------"
        m = re.sub('From: ','',remitente[0][1])
        n = re.sub('<(\w+@\w+(?:\.\w+)+)>','',m)
        remitente = n
        print remitente
        print "------------------------------------------"
        typ,asunto =  M.fetch(num,'(BODY[HEADER.FIELDS (SUBJECT)])')
        #Quitamos la palabra "Subject" por un espacio en blanco
        m = re.sub('^Subject: ','',asunto[0][1])
        textoasunto = m
        print textoasunto
        print "------------------------------------------"
        typ,cuerpo = M.fetch(num,'(BODY[TEXT])')
	#yp,cuerpo = M.fetch(num,'(RFC822)')
        texto =(cuerpo[0][1])
	#p = unicode(cuerpo[0][1])
        print type(texto)
#.close()
#.logout()


