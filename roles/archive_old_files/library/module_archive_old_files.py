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

def function_archive_old_files(path, time_up_to_deadline = 31536000):
    # counter : Compteur qui sert à indiquer un changement dans le 
    # PLAY RECAP lors de l'exécution du playbook.
    # Quand il y a archivage / compression de fichier(s), l'indicateur 
    # "changed" passe de 0 à 1.
    counter = 0
    # Boucle de génération de la listes des fichiers
    for file in os.listdir(path):
        # Définition variable f : file. 
        # f : concaténation chemin absolu et nom de fichiers (join : concatenation)
        f = os.path.join(path, file)
        # Condition de génération de la liste des fichiers 
        if os.path.isdir(f):
            counter = counter + function_archive_old_files(f, time_up_to_deadline)
        if os.path.isfile(f):
            # ----------------------------------------------------
            # Exclusion du traitement : ex > zip, iso, ...
            # re : Regular Expression - search : recherche dans toute la chaine
            # Structure : re.search(pattern, str) 
            exclu1 = re.search(".*\.zip$", f)
            exclu2 = re.search(".*\.iso$", f)
            # Condition de conjonction de négation pour assurer l'exclusion 
            # des éléments (permet éviter la disjonction du "ou").
            if (not (exclu1)) and (not (exclu2)):
                # ------------------------------------------------
                # Date actuelle au format datetime : ex = 2021-05-10 12:32            
                dat_now = datetime.now()
                # Déf var date lim : date en deça de laquelle l'action est effectuée. 
                dat_lim_c = dat_now - time_up_to_deadline
                # Conversion date limite en seconde = format "epoch"
                dat_lim_c_in_sec = dat_lim_c.timestamp()
                # Définition de la variable date de dernière consultation format epoch
                access_time = getatime(f)
                # Conditions déclenchant actions : si date de der. consult. dépasse 
                # (antérieur) à date lim
                if access_time < dat_lim_c_in_sec: # Renvoi True ou False 
                    # ----------------------------------------------
                    # Archivage & compression : module shutil
                    # base_dir=os.path.basename(f) : permet d'archiver / compresser que le fichier seul (sans l'arbo)
                    shutil.make_archive(base_dir=os.path.basename(f), root_dir=path + '/', format='zip', base_name=f)
                    # ----------------------------------------------
                    # Suppression du fichier original (du fichier non archivé / compréssé)              
                    os.remove(f)
                    # -------------------------------------------------
                    # Incrémentation de +1 du compteur
                    counter = counter + 1
                    
    return counter

def main():
    module = AnsibleModule( 
        argument_spec = dict(
            path = dict(required=True, type='str'), 
            timedelt = dict(type='int', default = 7) 
        )
    )
    chemin = module.params['path']
    interval = timedelta(seconds=module.params['timedelt'])

    nbfichiers = function_archive_old_files(chemin, interval)
    result = False
    if nbfichiers > 0:
        result = True
    module.exit_json(changed=result)

if __name__ == '__main__':
    main()