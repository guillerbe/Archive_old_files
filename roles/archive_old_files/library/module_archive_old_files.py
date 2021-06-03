#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import *

import os
import time
import shutil
import bz2
import re
from os import listdir
from os.path import isfile, join, getatime
from datetime import datetime, timedelta

def function_archive_old_files(path, time_up_to_deadline = 3650):
    counter = 0
    # Boucle de génération de la listes des fichiers
    for file in os.listdir(path):
        # Définition variable f : file. 
        # f : concaténation chemin absolue et nom de fichiers (join : concatenation)
        f = os.path.join(path, file)
        # Condition de génération de la liste des fichiers 
        if os.path.isdir(f):
            counter = counter + function_archive_old_files(f, time_up_to_deadline)
        if os.path.isfile(f):
            # -----------------------------------------------
            # Exclusion du traitement : ex > zip, iso, ...
            # re : Regular Expression - search : recherche dans toute la chaine
            # re.search(pattern, str) - je ne trouve pas de solution pour recherche 
            # de plusieurs patterns dans la même ligne
            exc1 = re.search(".*\.zip$", f)
            exc2 = re.search(".*\.iso$", f)
            # if (cond1 AND/OR COND2) AND/OR (cond3 AND/OR cond4):
            #if (exc1) or (exc2):
            if (not (exc1)) and (not (exc2)):
                # Si besoin affichage détection fichiers ZIP ou ISO.
                # Décommenter la ligne ci-dessous :
                #print("PAS FICHIER ZIP ou ISO")
                # ------------------------------------------------
                # Affichage des fichiers cible en chemin absolu depuis racine
                ## => print(f)
                # Déf variable : time_up_to_deadline : durée jusqu'à la date limite
                # La date lim étant la date en deça ou au dessus de laquelle l'action est effectuée.
                # # # time_up_to_deadline = 7
                # Date actuelle au format datetime : 
                # ex : 2021-05-10 12:32            function_archive_old_files(f):11.503663
                dat_now = datetime.now()
                # Affichage de la date date locale actuelle format datetime
                ## => print("Date actuelle :  ", dat_now)
                # Déf variable : unité de temps : correspond à l'unité de temps entre "maintenant" et la 
                # date lim. cible : weeks ou days, hours, minutes, seconds, microseconds, milliseconds.
                # ex : unit_of_time = weeks
                # Déf variable : date lim cible en deça ou au dessus de laquelle l'action est effectuée. 
                # timedelta : intervalle de temps soustrait à la date actuelle.
                # class datetime.timedelta(days=0, seconds=0, microseconds=0, 
                # milliseconds=0, minutes=0, hours=0, weeks=0)
                ###dat_lim_c = dat_now - timedelta(days = time_up_to_deadline)
                dat_lim_c = dat_now - time_up_to_deadline
                # Affichage de la date limite cible 
                ## => print("Date lim. cible :", dat_lim_c)
                # Conversion date limite en seconde = format "epoch"
                dat_lim_c_in_sec = dat_lim_c.timestamp()
                # Si besoin affichage date limite en seconde = format "epoch"
                # décommenter ligne ci-dessous :            
                ## => print("Date limite epoch :  ", dat_lim_c_in_sec)  
                # Définition de la variable de date de dernière consultation format epoch
                access_time = getatime(f)
                # Si besoin d'afficher dernière date d'accès en sec depuis "epoch"
                # décommenter la ligne => print [...] access_time, ci-dessous
                ## => print("Der. consult. epoch :", access_time)
                # Définition de la variable date de dernière consultation 
                # en temps local au format ctime 
                # ex : Thu Apr 29 15:26:26 2021
                local_time = time.ctime(access_time)
                # Affichage de la date locale de dernière consultation en format ctime 
                # ex : Thu Apr 29 15:26:26 2021
                ## => print("Der. consult. :", local_time)
                # Conditions déclenchant les actions :
                # Cond 1 : si date de der. consult. dépasse (antérieur) à date limite 
                if access_time < dat_lim_c_in_sec: # Renvoi True ou False 
                    ## => print("Der. consult. du fichier antérieur à date limite :", access_time < dat_lim_c_in_sec # Renvoi True ou False
                    ## => print(">>>>> A archiver ! <<<<<" + '\n') 
                    # ----------------------------------------------
                    # Archivage & compression : module shutil
                    # base_dir=os.path.basename(f) : permet d'archiver / compresser que le fichier seul (sans l'arbo)
                    shutil.make_archive(base_dir=os.path.basename(f), root_dir=path + '/', format='zip', base_name=f)
                    # ----------------------------------------------
                    # Suppression du fichier original (non archivé / compréssé)              
                    os.remove(f)
                    # -------------------------------------------------
                    # Cond 2 : autrement si date de der. consult. pas antérieur à la date lim 
                    # elif access_time > dat_lim_c_in_sec:
                    ## => print("Der. consult. du fichier antérieur à date limite :", access_time < dat_lim_c_in_sec) # Renvoi True ou False
                    ## => print(">>>>> Ne pas archiver ! <<<<<" + '\n')
                    # ++ correspond à counter = counter +1
                    counter = counter + 1
    return counter

def main():
    module = AnsibleModule( 
        argument_spec = dict(
            path = dict(required=True, type='str'), 
            timedelt = dict(type='int', default = 7, aliases=['interval']) 
        )
    )
    path = module.params['path']
    #timedelt = module.params['timedelt']
    interval = timedelta(days=module.params['timedelt'])
    #timedelt = timedelta(days=module.params['timedelt'])
    nbfichiers = function_archive_old_files(path, interval)
    test = False
    if nbfichiers > 0:
        test = True
    module.exit_json(changed=test)


if __name__ == '__main__':
    main()