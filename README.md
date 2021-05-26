# Archive_old_files
Ce projet s'inscrit dans le cadre de mon cursus de formation d'AIC dispensé par OC. 
Il constitue ma première expérience Python, Ansible, Git / GitHub, partage de code avec la communaute en open source. [...] 

## Description :
Contexte du "lab" :
La quantité de données stockées sur les serveurs de fichiers de plusieurs clients est en croissance trop élevée. Une phase intermediaire de traitement de ce problème est proposée. Elle vise à atténuer simplement l'augmentation rapide et importante de la taille des espaces de stockage. Pour ce faire des opérations automatiques d'archivage et de compression des données sont exécutées. Les données archivés et compressées sont les données qui ne sont plus consultées depuis une période décidée avec le client.

Le projet Archive_old_files est un des outils utilisé dans cette étape intermédiaire. Ce projet, initié sous Python 3.9, a pour but d'automatiser l'archivage / compression de fichiers dont la date de dernière consultation est considérée comme trop ancienne. 
Le fichier original après archivage / compression est supprimé de l'espace de stockage. 


## Table des matières :  
- [Fonctionnement:](#Fonctionnement)
- [Utilisation:](#Utilisation)
- [Prerequis:](#Prerequis)
- [Version:](#Version)
- [License:](#License)
- [...]

## Fonctionnement
Fonctionnement [...]

## Utilisation
Utilisation [...]

## Prerequis :  
* Le service Ansible doit être installé sur un ordinateur.
* Cette machine communique en ssh avec les machines cibles.


## Version :  
0.2.5

## License :  
#### GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)