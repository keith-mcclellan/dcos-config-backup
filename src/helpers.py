#!/usr/bin/env python3
#
# helpers.py: helper functions for other processes in the project to use
#
# Author: Fernando Sanchez [ fernando at mesosphere.com ]
#
# Set of functions repeatedly used in other parts of this project. 
# Put on a separate module for clarity and readability.

import os
import json

# FUNCTION get_conf
def get_config ( config_path ) :
	"""
	Get the full program configuration from the file and returns a dictionary with 
	all its parameters. Program configuration is stored in raw JSON so we just need
	to load it and use standard `json` to parse it into a dictionary.
	"""

	config_file = open( config_path, 'r' )  	#open the config file for reading
	read_config = config_file.read()			#read the entire file into a dict with JSON format
	config_file.close()
	config = json.loads( read_config )			#parse read config as JSON into readable dictionary

	return config

def escape ( a_string ) :
	"""
	Escape characters that create issues for URLs
	"""
	escaped = a_string.replace("/", "%252F")

	return escaped

def single_to_double_quotes ( a_string ) :
	"""
	swap out single to double quotes
	"""
	doubled = a_string.replace("'", '"')

	return doubled

def walk_and_print( item, name, field ):
	"""
	Walks a recursive tree-like structure for items printing them.
	Structure is assumed to have children under 'groups' and name under 'id'
	Receives the tree item and an 'id' as a name to identify each node.
	"""
	if item[field]:
		for i in item[field]:
			walk_and_print( i, name, field )
	else:
		print( "{0}: {1}".format( name, item['id'] ) )

	return True

def format_service_group( service_group ):
	"""
	Walks a (potentially recursive tree-like structure of) service group in a dict that potentially include apps.
	Removes fields that can't be posted initially from the service group:
	- apps (empty it)
	- version (remove it)
	Changes the format of the "id" field to remove "/"
	Modifies the object passed as a parameter, return value should not be used.
	"""

	#remove my children's apps
	for group in service_group['groups']:
		if 'groups' in group:
			format_service_group( group )
	
	#remove my own apps
	service_group['apps'] = [] #apps is an empty list
	if 'version' in service_group: del service_group['version']
	if 'health' in service_group: del service_group['health']

	return service_group

def format_app( app ):
	"""
	Formats an app from the state where it has been received from DC/OS to that in which it can be posted. Some fields need to be edited:
	- version (remove it)
	Changes the format of the "id" field to remove "/"
	Modifies the object passed as a parameter, return value should not be used.
	"""

	if 'version' in app: del app['version']
	if 'versionInfo' in app: del app['versionInfo']
	if 'tasksHealthy' in app: del app['tasksHealthy']
	if 'tasksUnhealthy' in app: del app['tasksUnhealthy']
	if 'tasksStaged' in app: del app['tasksStaged']
	if 'tasksRunning' in app: del app['tasksRunning']
	if 'deployments' in app: del app['deployments']

	return app
	