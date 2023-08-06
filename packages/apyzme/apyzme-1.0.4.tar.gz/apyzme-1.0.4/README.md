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

Après avoir installé le module, vous pouvez directement appeler la fonction "lancer" et lui fournir la classe portant l'API: 
	- les arguments par leur fonction "sanitize" (de nettoyage et de contrôle), 
	- les actions par leur fonction de réalisation. 

Si la classe portant l'API n'est pas documenté, le module tentera de récupérer la documentation du script "\_\_main\_\_". A défaut, le lancement échouera. Cette partie de la documentation devra toujours répondre à 3 parties séparées par "---" : 
	- le titre du script 
	- une courte description 
	- la version à afficher

	#!/usr/bin/env python3

	""" 
		Test 
		---
		Je ne fais pas grand chose... 
		---
		n 
	""" 

	################ ---------------------------------------------------------

	from apyzme import api, lancer 

	################ ---------------------------------------------------------

	if __name__=="__main__": 

		class Exemple: 

			@api( "arguments", "arg1" ) 
			def arg1_sanitize( argument ): 
				"""Ceci une courte description de l'argument n°1. 
				---
				Que j'approfondie ici.""" 
				r = f"arg1 : '{argument}'" 
				print( r ) 
				return r

			@api( "arguments", "arg2" ) 
			def arg2_sanitize( argument ): 
				"""Ceci une courte description de l'argument n°2.
				---
				Que j'approfondie ici.""" 
				r = f"arg2 : '{argument}'" 
				print( r ) 
				return r

			@api( "actions", "toto" ) 
			def act1_resoudre( self, arguments ): 
				"""Ceci une courte description de l'action 'toto'.
				---
				Que j'approfondie ici.""" 
				print( "action 'toto' sur les arguments :", arguments ) 
				exit( CODES_RETOUR["ACTION_ALERTE"] )

			@api( "actions", "titi" ) 
			def act1_resoudre( self, arguments ): 
				"""Ceci une courte description de l'action 'titi'.
				---
				Que j'approfondie ici.""" 
				print( "action 'titi' sur les arguments :", arguments ) 

		lancer( Exemple ) 









	$ python3 exemple.py 
	usage: Apyzme [-h] [--arg1 ARG1] [--arg2 ARG2] [--version] action
	Apyzme: error: the following arguments are required: action

	$ python3 exemple.py -h
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




