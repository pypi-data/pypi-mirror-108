# Apyzme

## Présentation 

Ce module permet de générer facilement une API pour le scripting de python dans Shell, à partir d'un simple décorateur et d'une classe maîtresse, instanciée. 

Attention : une fois la fonction "lancer" du module, celle s'excute jusqu'à la sortie. Les "exception" ne sont pas volontairement pas gérés et sont laissés à la libre appréciation du développeur.  

---

## Métadonnées 

  - Version : 1 
  - Mainteneur : Julien Garderon <julien.garderon@gmail.com> 
  - URL du dépôt : https://git.services.nothus.fr/communaute/apyzme 
  - Licence : MIT 

---

## Exemple 

	$ python3 apyzme.py 
	usage: Apyzme [-h] [--arg1 ARG1] [--arg2 ARG2] [--version] action
	Apyzme: error: the following arguments are required: action

	$ python3 apyzme.py -h
	usage: Apyzme [-h] [--arg1 ARG1] [--arg2 ARG2] [--version] action
     
	Ce module permet de générer facilement une API pour le scripting de python dans Shell, à partir d'un simple décorateur et d'une classe maîtresse, instanciée. Version 1 - Julien Garderon <julien.garderon@gmail.com>
     
	positional arguments:
	  action       quelle action entreprendre ?
     
	optional arguments:
	  -h, --help   show this help message and exit
	  --arg1 ARG1  Ceci une courte description de l'argument n°1.
	  --arg2 ARG2  Ceci une courte description de l'argument n°2.
	  --version    show program's version number and exit

	$ python3 apyzme.py --arg1 truc toto
	arg1 : 'truc'
	action 'toto' sur les arguments : Namespace(action='toto', arg1=["arg1 : 'truc'"], arg2=None)

	$ python3 apyzme.py --arg1 truc toto
	arg1 : 'truc'
	action 'toto' sur les arguments : Namespace(action='toto', arg1=["arg1 : 'truc'"], arg2=None)

	$ python3 apyzme.py --arg1 truc --arg1 bidule toto
	arg1 : 'truc'
	arg1 : 'bidule'
	action 'toto' sur les arguments : Namespace(action='toto', arg1=["arg1 : 'truc'", "arg1 : 'bidule'"], arg2=None)




