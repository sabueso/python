#!/usr/bin/env python

#Sencillo script que sirve para ayudar a documentar
#algunos reportes para 3ros.
#El script cuenta con comandos que sacan (a parecer
#del autor) una serie de informacion necesaria para
#la comprension de algunas infraestructuras.

#Nada como ser haragan y no querer currar :-P

import os
posicion=0
#Agregar el comando en formato "etiqueta"->"comando"
comandos=	[
		['Actividad',"uptime"],
		['CPU',"cat /proc/cpuinfo|grep -E '(name|processor)'"],
		['Memoria',"free -mo"],
		['Direccionamiento IP',"ip addres show |grep -E '(state|inet)'|grep -v inet6"],
		]

#print len(comandos)
while posicion < len(comandos):
	print comandos[posicion][0]
	print "---------------------------------------"
	os.system(""+comandos[posicion][1]+"")
	print "\n"
	posicion=posicion+1
#





