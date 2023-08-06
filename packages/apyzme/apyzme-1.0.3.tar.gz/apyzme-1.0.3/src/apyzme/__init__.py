#!/usr/bin/env python3

""" 
	Apyzme 
	---
	Ce module permet de générer facilement une API pour le scripting 
	de python dans Shell, à partir d'un simple décorateur et d'une 
	classe maîtresse, instanciée. 
	Version 1 - Julien Garderon <julien.garderon@gmail.com> 
	---
	1.0 
""" 

__all__ = [ 
	"api", "lancer" 
]

CODES_RETOUR = {
	"OK": 0, 
	"ACTION_INCONNUE": 1, 
	"ACTION_ALERTE" : 2 
}

API = {
	"actions": {}, 
	"arguments": {}, 
	"objet" : None  
} 

def api( api_type, api_nom ):
	global API 
	if api_type not in API: 
		API[api_type] = {} 
	def decorateur( fct ): 
		try: 
			API[api_type][api_nom] = ( fct, fct.__doc__.split("---")[0] ) 
		except Exception as err: 
			print( f"l'applicatif a des entrées d'API incorrecte : {err}" )
		return fct 
	return decorateur 

def lancer( classe_api, *args, **kwargs ): 
	global API 
	import argparse 
	API["objet"] = classe_api( *args, **kwargs ) 
	app_titre, app_presentation, app_version = [ 
		item.strip() for item in __doc__.split("---") 
	]  
	parser = argparse.ArgumentParser( 
		prog=app_titre, 
		description=app_presentation 
	) 
	for argument in API["arguments"]: 
		parser.add_argument(
			f"--{argument}", 
			required=False,
			type=API["arguments"][argument][0],  
			action="append", 
			help=API["arguments"][argument][1] 
		) 
	parser.add_argument( 
		"--version", 
		action = "version", 
		version = f"{app_titre} {app_version}" 
	) 
	parser.add_argument(
		'action', 
		help='quelle action entreprendre ?' 
	) 
	arguments = parser.parse_args() 
	if arguments.action in API["actions"]: 
		API["actions"][arguments.action][0]( 
			API["objet"], 
			arguments 
		) 
		exit( CODES_RETOUR["OK"] ) 
	else: 
		print( "cette action n'est pas connu !" ) 
		exit( CODES_RETOUR["ACTION_INCONNUE"] ) 

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


