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
		['Kernel',"uname -a"],
		['Actividad',"uptime"],
		['CPU',"cat /proc/cpuinfo|grep -E '(name|processor)'"],
		['Memoria',"free -mo"],
		['Direccionamiento IP',"ip addres show |grep -E '(state|inet)'|grep -v inet6"],
		['Enrutamiento',"ip route show"],
		['FW basico',"iptables -L"],
		['FW nat',"iptables -L -t nat"],
		['FW mangle',"iptables -L -t mangle"],
		#['Particionado',"fdisk -l"],
		['Puntos de montaje',"mount"],
		['Espacio libre',"df -Ph"],
		['10 Procesos con mas carga: CPU,MEM ..',"ps -A -o %cpu,%mem,euser,ucmd --sort=pcpu|tail -n10"]
		]

#print len(comandos)
while posicion < len(comandos):
#	print "------------------------------------------------------------------------------"
	print comandos[posicion][0]
	print "------------------------------------------------------------------------------"
	os.system(""+comandos[posicion][1]+"")
	print "\r"
	posicion=posicion+1
#





