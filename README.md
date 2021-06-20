# Module Ansible Archive_old_files
Ce projet de création de module Ansible en Python s'inscrit dans le cadre de mon cursus de formation d'AIC dispensé par OC. 
Il constitue ma première expérience Python et Ansible, Git / GitHub et partage de code avec la communauté en open source. 

## Description :
Contexte du "lab" : La quantité de données stockées sur les serveurs de fichiers de plusieurs clients est en croissance élevée. En tant que prestataire informatique nous proposons une phase intermediaire de traitement avec pour objectif de réduire la taille des données dans ces espaces de stockage. 

Le projet de module Ansible "Archive_old_files" est l'un  des outils utilisé dans cette phase intermédiaire. Ce module, initié sous Python 3.9, sert à automatiser l'archivage / compression des fichiers dont la date de dernière consultation est considérée comme trop ancienne par les clients. 
Les fichiers originaux après archivage / compression au format zip sont supprimés de l'espace de stockage. Les archives sont laissées à l'emplacement des fichiers originaux.

Exemple de gain d'espace de stockage attendu : environ 20 à 25% pour un fichier texte au format odt, doc, docx, txt... compressé en .zip.

## Table des matières :  
- [Fonctionnement:](#Fonctionnement)
- [Installation:](#Installation)
- [Utilisation:](#Utilisation)
- [Prerequis:](#Prerequis)
- [Version:](#Version)
- [License:](#License)


## Fonctionnement
* Le module utilise comme premier argument le chemin pointant vers le répertoire à traiter (via la variable ***path***). 
* Il utilise comme second argument l'intervalle de temps en secondes jusqu’à la date limite cible (via la variable ***timedelt***).
* Le module balaye les fichiers et tous les sous-répertoires du répertoire cible (traitement fonctionnel récursif)
* Il exclu du balayage et de l'archivage / compression les fichiers aux formats choisis comme devant être exclus. Sont exclus à titre d'exemple dans notre cas les fichiers iso et zip. 
* Il compare la date de dernière consultation des fichiers avec la date limite cible. 
* Il archive / compresse au format .zip les fichiers dont la  dernière consultation est antérieure à la date choisie.
* Il supprime de l'espace de stockage les fichiers originaux après leur archivage / compression.
* Il laisse les fichiers archivés à l'emplacement des fichiers originaux.


## Installation
Pour installer les fichiers du projet, voici 2 options :
1. **Copie des fichiers:**
Téléchargez l'archive des éléments Ansible du projet en cliquant sur ce [lien](https://github.com/guillerbe/Archive_old_files/archive/refs/heads/dev.zip) . Décompréssez l'archive dans votre espace de travail Ansible.
2. **Clonage Git du projet:**
Placez vous dans le répertoire que vous aurez choisi, par exemple dans le répertoire temporaire puis tapez la commande suivante : 
```
cd /tmp/

git clone https://github.com/guillerbe/Archive_old_files.git  
```  

## Utilisation
* Accédez à l'espace de travail Ansible, l'espace où se situe les fichiers d'inventaire, le fichier playbook et le répertoire rôles. Ce dernier est composé du sous dossiers ***library*** qui contient le module ***module_archive_old_files.py*** et du sous dossier ***tasks*** qui contient le fichier d'instructions ***main.yml***. 
* Le fichier d'inventaire se nomme ***00_inventory.yml***. Editez le en entrant : le nom du groupe ou des groupes de machines et le nom des machines.
```
vim 00_inventory.yml
```  

```  
all:
  children:
    fservers:
      hosts:
        ubsfs01:
        ubdit01:
```  
* Le fichier playbook se nomme ***playbook_roles.yml***. Assurez-vous que les noms : des machines, de l'utilisateur Ansible et du rôle ''appelé'' correspondent aux configurations attendues. 
```
vim playbook_roles.yml
```  
```
---
- name: Mon playbook archive old files
  hosts: all 
  remote_user: user-ansible
  become_user: yes
  roles:
  - archive_old_files
```

* Les arguments utilisés par le module se nomment ***path*** et ***timedelt***. Leur valeur est affectée aux variables de mêmes nom : ***path*** et ***timedelt***. Assurez-vous de ces valeurs  dans le fichier ***main.yml*** du sous répertoire ***"tasks"***  contenu dans le répertoire du rôle dédié au projet: ***roles/archive_old_files/tasks/main.yml*** .  
```
vim roles/archive_old_files/tasks/main.yml
```  
```  
---
- name: module_archive_old_files
  module_archive_old_files:
    path: "/home/guillerbe/Shared"
    timedelt: 3
```  
* L'unité de temps de l'intervalle jusqu'à la date limite de dernière consultation des fichiers est en secondes. C'est donc une **valeur en secondes** qui devra être affectée à la variable ***timedelt:***

* Exécuter le playbook avec la commande Ansible suivante :
```
ansible-playbook -i 00_inventory.yml -k playbook_roles.yml  
```    
## Prerequis :  
* Un serveur node contrôleur (ou node manager) Ansible est en service.
* Ce serveur communique en ssh avec les machines cibles (avec les nodes managés).
* Toutes les machines disposent d'un compte utilisateur ***"user-ansible"*** configuré avec les privilèges sudo.
* Toutes les machines sont déclarées dans le fichier ***"/etc/hosts"*** des autres machines si pas de résolution de nom géré par un serveur DNS.  
  
## Version :  
0.3.0

## License :  
#### GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)