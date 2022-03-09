#!/usr/bin/env python3

# ####################################################################################
# Copyright IBM Corp. 2016 All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ####################################################################################
#
# Purpose : The script is invoked as cyber resiliency workflow user action
#           to create safeguarded copy either using Copy Serice Manager (CSM)
#           Backup command or by invoking a predefined Scheduled Task in CSM
#           to create SafeguardedCopy backup on DS8K 
#           
#           The lab setup uses 2 copy services sessions (MM & GM)and they both are 
# 			suspended before invoking Safeguarded Copy backup.
#
# usage: run-cr.py [-h] -s CSM_SERVER [-P CSM_PORT] -u CSM_USER -p CSM_USER_PASSWD -t CSM_TASK
#
# ####################################################################################
#
#										Disclaimer
#
#	This script is written to demonstrate the cyber resiliency workflow in a controlled
#	lab environment. 
# 
#   There is no official support on the script from IBM.
#
#   Under no circumstances the script may be deployed in Production environment
#
#   Users are encouraged to develop their own programatical response based on this 
#   script.
#

import sys
import json
import base64
import argparse
import requests
from   requests.packages.urllib3.exceptions import *

def main():

	AUTH_TOKEN = getAuthToken()
	_hdr['X-Auth-Token'] = AUTH_TOKEN

	if AUTH_TOKEN is not None:
		runScheduledTask()
	

def getAuthToken():
	""" 
		Purpose: This function returns authorization token 
				 from CSM host post authentication.
		
		Params:
			- In : None
			- Out: authentication token
	"""
	
	_endpoint = URL + '/system/v1/tokens'

	_auth_data = { 
				  'username' : CSM_USER,
				  'password' : CSM_PASS
	}

	_response = mkAPIcall( _endpoint, 'post', _hdr, _auth_data, 'token' )

	return _response


def runScheduledTask():
	"""
		Purpose: This function executes the given scheduled task
		Params:
			- In : None
			- Out: None
	"""

	# Retrieve all tasks from endpoint
	_endpoint = URL + '/sessions/scheduledtasks'
	_response = mkAPIcall( _endpoint, 'get', _hdr, '', None )
	
	# Retrieve task_id for given scheduled task
	task_id = 0
	for task in _response:
		if task['name'] == CSM_TASK:
			task_id = task['id']
			break

	print('Found {0} with id => {1}' . format(CSM_TASK,task_id))

	# Invoke the scheduled task
	_endpoint = _endpoint + '/' + str(task_id)
	_response = mkAPIcall( _endpoint, 'post', _hdr, '', None )
	
	if _response['msg'] == "IWNR2211I":
		print('Task {0} invoked successfully !!' . format(CSM_TASK))
		return True


def mkAPIcall( URL, METHOD, HDR, DATA, RETURN_VAL ):
	"""
		Purpose: This function is used to make the api calls
	             to CSM host. 

		Parameters:
			- IN : 
				- URL - URL of CSM Host
				- METHOD - GET/POST
				- HDR - Header for the method
				- DATA - Json based Data values for the API Call
			- OUT:
				- RETURL_VAL - API Call output
	"""

	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

	try:
		if METHOD == 'post':
			_requests = requests.post(
				URL,
				headers=HDR,
				data=DATA,
				verify=False,
				timeout=30
			)
		else:
			_requests = requests.get(
				URL,
				headers=HDR,
				data=DATA,
				verify=False,
				timeout=30
			)

		try:
			_response = json.loads( _requests.text )

		except json.decoder.JSONDecodeError:
			print("Unknown response from server")
			sys.exit(1)

	except requests.exceptions.ConnectionError:
		print("ERROR: Connection refused. Check CSM Server IP & PORT")

	if RETURN_VAL is not None:
		return _response[RETURN_VAL]

	return _response


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument(
		'-s',
		'--csm_server', 
		type=str, 
		required=True, 
		help='<Mandatory> IP/FQDN of CSM server'
	)

	parser.add_argument(
		'-P',
		'--csm_port', 
		type=int, 
		required=False, 
		default=9559, 
		help='CSM Server port [default: 9559]'
	)

	parser.add_argument(
		'-u',
		'--csm_user', 
		type=str, 
		required=True,
		help='<Mandatory> Base64 encoded username'
	)

	parser.add_argument(
		'-p',
		'--csm_user_passwd', 
		type=str, 
		required=True, 
		help='<Mandatory> Base64 encoded password'
	)

	parser.add_argument(
		'-t',
		'--csm_task',
		type=str, 
		required=True, 
		help='CSM Scheduled Task name'
	)

	args = parser.parse_args()

	CSM_HOST   = args.csm_server.strip()
	CSM_PORT   = args.csm_port
	b64_USER   = args.csm_user.strip()
	b64_PASS   = args.csm_user_passwd.strip()
	CSM_TASK   = args.csm_task.strip()

	# the base64 value passed is received as ascii string
	# it needs be encoded from ascii to base64 and 
	# decoded back to ascii
	CSM_USER = base64.b64decode(b64_USER.encode('ascii')).decode('ascii').strip()
	CSM_PASS = base64.b64decode(b64_PASS.encode('ascii')).decode('ascii').strip()

	URL = 'https://{0}:{1}/CSM/web' . format(CSM_HOST,CSM_PORT)

	_hdr = {'Accept-Language': 'en-US',
			'Content-Type': 'application/x-www-form-urlencoded'
	}

	main()
