#!/usr/bin/env python
import os,datetime
################################################################################################################
##Agregar al array los routers a hacer copia
##de seguridad, generar antes claves dsa de ssh
##subirlas , e importarlas al router en cuestion
##IMPORTANTE: http://wiki.mikrotik.com/wiki/Use_SSH_to_execute_commands_%28DSA_key_login%29
################################################################################################################

# TODO
# 1: implementar directorio con dia
# 2: generar un export para tener referencias y poder hacer greps
# Fichero generado con extension .backup , a borrar

routers=[
["RouterCasa","10.20.66.2","admin"],
["Rbcastella2","10.20.66.1","admin"],
["Rbcarboles","10.20.66.65","admin"],
["RbMiquelMumany2","10.20.68.1","admin"],
["RBCanOriol","10.20.68.4","admin"],
["RBCEIPRamonLLull","10.20.68.5","admin"],
["Lpazalea","10.228.195.129","admin"],
["Lpbartalisman","10.228.195.130","admin"],
["LpCanCortes","10.139.51.129","admin"],
]
########################################################

for i in routers:
		print "Copiando "+i[0]+"..."
		#generamos backup, copiamos, y borramos...
		os.system("ssh admin@"+i[1]+" -C \"/system backup save name="+i[0]+"-"+str(datetime.date.today())+"\"")
		os.system("scp admin@"+i[1]+":./"+i[0]+"-"+str(datetime.date.today())+".backup .")
		os.system("ssh admin@"+i[1]+" -C \"/file remove "+i[0]+"-"+str(datetime.date.today())+"\"" )
		#generamos export, copiamos, y borramos...
                os.system("ssh admin@"+i[1]+" -C \"/export file="+i[0]+"-"+str(datetime.date.today())+"\"")
                os.system("scp admin@"+i[1]+":./"+i[0]+"-"+str(datetime.date.today())+".rsc .")
                os.system("ssh admin@"+i[1]+" -C \"/file remove "+i[0]+"-"+str(datetime.date.today())+"\"" )
		print "Hecho"
