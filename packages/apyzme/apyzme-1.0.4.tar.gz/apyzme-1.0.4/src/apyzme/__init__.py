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

import sys 
print(  )

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
	doc = sys.modules["__main__"].__doc__ if classe_api.__doc__ == None else classe_api.__doc__ 
	app_titre, app_presentation, app_version = [ 
		item.strip() for item in doc.split("---") 
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

