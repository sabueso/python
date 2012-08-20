#!/usr/bin/python

import os, sys, syslog, time, datetime, smtplib, commands
##
##Script que cumplio su funcion y paso a mejor vida :-P
##
empresa = sys.argv[1]
buffer = []
ficherovpn = '/etc/openvpn/server.conf'
#variables del mail#
remitente = 'pepito@pepito.com'
destino = ['pepito1@pepito.com','pepito2@pepito.com']
nmapred = str(commands.getoutput('nmap -sP '+sys.argv[2]+'/24'))
nmappuerto = str(commands.getoutput('nmap -p5405 '+sys.argv[2]+'/24'))
#fin variables mail#

from time import strftime
syslog.syslog('CAMBIORED.PY: la bestia se ha despertado a las '+strftime("%Y-%m-%d %H:%M:%S")+' con los comandos "'+sys.argv[1]+'" - "'+sys.argv[2]+'"' )

if sys.argv[1] == 'telefonica':
	if len(sys.argv) != 3:
	     print "Necesito 2 parametros para devolver una red a Telefonica\n ./cambiored.py 'telefonica' 'subdred'\n No hace falta PUERTA DE ENLANCE"
	     sys.exit()

	#Eliminamos del fichero de configuracion de la VPN la subred que queremos devolver a telefonica.
	#Omitimos la entrada de la linea en un array si contiene la subred especificada  , que despues se vuelca a un fichero.
	red = sys.argv[2]	
	vpn = open(ficherovpn,'r')
	for s in vpn.xreadlines ( ):
		if not red in s:
			buffer.append(s)
	vpn.close()
        #generamos la copia de seguridad del fichero
        print 'Generando copia de seguridad del fichero'
        if os.system('cp '+ficherovpn+' /tmp/server'+strftime("%Y%m%d")+'.conf') ==0:
               print 'Copia de seguridad OK'
        else:
               print 'No se ha podido generar la copia'
	#modificamos finalmente el fichero
        vpn = open(ficherovpn,'w')
        for line in buffer:
               vpn.write(line)
        vpn.close()
        print 'Fichero de tunel modificado modificado ...\n'

	#Quitamos la ruta de HUTCH
	print 'Quitando ruta de enrutador Coltprix...\n'
	if os.system('ssh colt@172.17.0.5 sudo route del -net '+sys.argv[2]+' netmask 255.255.255.0 gw 172.17.45.5') == 0:
		print 'La ruta se ha quitado correctamente\n'
	else:
		print 'No se ha podido quitar la ruta!\n'
	#Escribimos al syslog
	
        print 'Reiniciando OpenVpn'
        if os.system('sudo /etc/init.d/./openvpn restart') == 0:
        	print 'Se ha reinciado el tunel con exito'
	else:
		print 'No se ha podido reiniciar el tunel'
		
	syslog.syslog('CAMBIORED.PY: Se ha devuelto a telefonica la red '+sys.argv[2]+'\n')

elif sys.argv[1] ==  'colt':
	#Comprobacion de opciones pasadas a la aplicacion
	if len(sys.argv) != 4:
	        print "Necesito 3 parametros para hacer la migracion a Colt!\n ./cambiored.py 'colt' 'subdred' 'puerta de enlace'\n"
		sys.exit()
	#Comprobacion de conectividad contra el enrutador , si no se ve el enrutador via ICMP , se aborta
	print 'Vamos a comprobar que podamos ver el enrutador\n'
	if os.system('ping -c 10 '+sys.argv[3]+'') == 0:
		print 'Puedo ver el enrutador de Colt de la subred '+sys.argv[2]+' ,continuamos ...\n\n'
	else:
		print 'No veo el enrutador por lo que la migracion no funcionara , estan todos los cables conectados correctamente?\n\n'
		sys.exit()
	
	#Vamos a comprobar que no exista el valor de la subred dentro del fichero de configuracion
	#Si existe el valor dentro del fichero de configuracion, es que la subred ya ha sido migrada. Si es asi , se aborta la ejecucion.
	#Sino , se continua
	vpn = open (ficherovpn,'r+')
	if not sys.argv[2] in vpn.read():
		print 'La ruta no existe en el fichero, vamos a modificarlo\n\n'
	else:
		print 'Ya existe la subred '+sys.argv[2]+' en el fichero de la vpn ! Prueba de pasarlo a Telefonica y volver a migrarlo hacia Colt..Abortamos!\n\n'
		sys.exit()
	vpn.close()

        #El fichero se abre en modo adicion para agrgar al final la linea que contiene la subred de colt a migrar.
	vpn = open (ficherovpn,'a+')
	vpn.write('push "route '+ sys.argv[2]+' 255.255.255.0"\n')
	print 'Fichero de ruta modificado\n\n'

	#else: 
	#	print 'No se ha podido modificar el fichero de rutas\n\n'
	vpn.close()

        print 'Reiniciando OpenVpn'
        if os.system('sudo /etc/init.d/./openvpn restart') == 0:
        	print 'Se ha reinciado el tunel con exito'
        else:
        	print 'No se ha podido reiniciar el tunel'
	
	#Agregamos la ruta al enrutador HUTCH
	print 'Agregando ruta al enrutador Hutch\n'
	if os.system('ssh colt@172.17.0.5 sudo route add -net '+sys.argv[2]+' netmask 255.255.255.0 gw 172.17.45.5') == 0:
		print 'La ruta se ha agregado correctamente\n\n'
		print '###Enviando notificacion por correo\n'
		mensaje = 'Subject:Se ha migrado la tienda '+sys.argv[2]+'' '\nDetras del enrutador estan los siguientes equipos levantados!\n''\n'+nmapred+'' '\n\nLos siguientes equipos tienen el puerto 5405 abierto y visible a traves del router de Colt\n\n' ''+nmappuerto+''
		#Ahora enviamos el correo ...
		server = smtplib.SMTP('172.17.1.50')
		#server.set_debuglevel(1)
		server.sendmail(remitente,destino,mensaje)
		server.quit()
		print '###Notificacion enviada###\n'
	else:
		print 'No se ha podido agregar la ruta!\n\n'
	#Notificamos via syslog que se ha migrado correctamente.
	syslog.syslog('CAMBIORED.PY: Se ha agregado la red de COLT la subred '+sys.argv[2]+' a el host Coltprix\n')
sys.exit()
