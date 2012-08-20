#!/usr/bin/env python
import pyinotify,commands
import codecs
import re
import os
import datetime
##
ruta=['/home/django/']
##
ficherosmonitorizados=[]
ficherointermedio=[]

for i in ruta:
	#El pensamiento CaNI al poder 
	#buscamos todos los ficheros .py , le decimos que quie los __ que son de ficheros compilados
	#y que nos quite los ocultos :-P
	ficheros=commands.getoutput('find -P '+i+' -name \'*.py\' |grep -v "__"|egrep  -v \'(\/\.)\'')
	for line in ficheros.split():
		ficherosmonitorizados.append(line)
#for a in ficheros.split():
#	print a

wm = pyinotify.WatchManager()

mask = pyinotify.IN_MODIFY | pyinotify.IN_CREATE

excl_lst = [".*\.txt",\
".*\.wsgi",\
".*\.swp",\
"/home/django/discovirtual/apache/django.wsgi",\
"/home/django/discovirtual/apache/",\
"^/home/django/discovirtual/apache/.*",\
]
excl = pyinotify.ExcludeFilter(excl_lst)

#for j in ruta:
for j in ficherosmonitorizados:
        wm.add_watch(''+j+'', mask, rec=True)
        print "Agregado monitor a fichero -> "+j+""

class EventHandler(pyinotify.ProcessEvent):
	global ficherointermedio
	ficherointermedio=[]
	#Si amiguitos , preparo un monton de retoques sobre los eventos de los que no uso todos
	#pero como dice la publi de pantene , porque yo lo valgo!
	def process_IN_MOVE_SELF(self,event):
		print "movimiento"
        def process_IN_DELETE_SELF(self,event):
                print "borrado"
        def process_IN_IGNORED(self,event):
                print "ignorado"
        def process_IN_CREATE(self,event):
                global ficherointermedio
                print "Evento CREACION (debe ser VIM el que edita ...)"
                print "variable pathname ->"+event.pathname+""
                print "variable path ->"+event.path+""
                print "MOFIDIFICACION "+str(datetime.datetime.now())+""
                print "---------------------"
                if re.search('(^\/\w+\/\w+\/\w+\/)',event.pathname):
                        m=re.search('(^\/\w+\/\w+\/\w+\/)',event.pathname)
                        #print m.group(0)
                        print "Inicio "+str(m.group(0))+"apache/django.wsgi"
                        if os.path.exists(''+str(m.group(0))+'apache/django.wsgi'):
                                print "existe dentro de la carpeta de proyecto"
                                path1=""+str(m.group(0))+"apache/django.stock"
                                ficheroinicial=open(''+path1+'','r+')
                                for lineaf in ficheroinicial.xreadlines():
                                        print "LECTURA"
                                        #print lineaf
                                        ficherointermedio.append(lineaf)
                                ficheroinicial.close()
                                path2=""+str(m.group(0))+"apache/django.wsgi"
                                ficherofinal=open(''+path2+'','w')
                                for lineai in ficherointermedio:
                                        print "ESCRITURA"
                                        ficherofinal.write(lineai)
                                ficherofinal.close()
                                print "<-fichero modificado->"
                                ficherointermedio=[]
                                return
                        else:
                                print "no existe el fichero wsgi dentro del dir de codigo"
                else:
                        print "No hay match con el path"
                        pass
        def process_IN_MODIFY(self,event):
		global ficherointermedio	
                print "modificado"
		print "variable pathname ->"+event.pathname+""
		print "variable path ->"+event.path+""
                print "MOFIDIFICACION "+str(datetime.datetime.now())+""
		print "---------------------"
		if re.search('(^\/\w+\/\w+\/\w+\/)',event.pathname):
			m=re.search('(^\/\w+\/\w+\/\w+\/)',event.pathname)
	               	#print m.group(0)
			print "Inicio "+str(m.group(0))+"apache/django.wsgi"
			if os.path.exists(''+str(m.group(0))+'apache/django.wsgi'):
				print "existe dentro de la carpeta de proyecto"
				path1=""+str(m.group(0))+"apache/django.stock"
				ficheroinicial=open(''+path1+'','r+')
				for lineaf in ficheroinicial.xreadlines():
					print "LECTURA"
					#print lineaf
					ficherointermedio.append(lineaf)
				ficheroinicial.close()
                                path2=""+str(m.group(0))+"apache/django.wsgi"
				ficherofinal=open(''+path2+'','w')
				for lineai in ficherointermedio:
					print "ESCRITURA"
					ficherofinal.write(lineai)
				ficherofinal.close()
				print "fichero modificado"
				ficherointermedio=[]
				return
			else:
				print "no existe el fichero wsgi dentro del dir de codigo"
	        else:
			print "No hay match con el path"
			pass
	def procees_IN_CLOSE_WRITE(self,event):
		print "cerrado y modificado"

handler = EventHandler()
notificador = pyinotify.Notifier(wm, handler)

# Internally, 'handler' is a callable object which on new events will be called like this: handler(new_event)
##for j in ficherosmonitorizados:
##	wm.add_watch(''+j+'', mask)
##	print j
	#print j
	#if re.search('(^\/\w+\/\w+\/\w+\/)',j):
	#	m=re.search('(^\/\w+\/\w+\/\w+\/)',j)
	#	print m.group(0)
	#else:
	#	pass

#wm.add_watch('/home/django/discovirtual/nucleo/views.py', mask)
#wm.add_watch('/home/django/mysiteinformatica/gestorincidencias/views.py',mask)
notificador.loop()
