# Readme

This repository contains the sample script that can be used to invoke Safeguarded Copy on IBM DS8K using IBM Copy Services Manager (CSM) API commands.

## Disclaimer ##

The script is purely created as a PoC and it is developed and tested in controlled lab environment. There is **_no_** official support on the script. You may use the script as a template to create your own workflow. 

### Workflow ###

For both control and data path use cases, we heavily depend on the audit logs, network flows in order to track the actions. IBM QRadar is used for threat detection. The audit logs from storage and network flows / logs are used to determine whether the storage is under attack. This is done using IBM QRadar's rules engine, and when the threat is detected a pre-defined custom action is triggered ( in this case .py ) that will execute series API calls using CSM server on DS8K storage system to an immutable backup of the data. 

### Pre-requisites ###

Following section lists the pre-requisites.

 - Copy Services Manager installation
 - Identification of volumes that needs safeguarding
 - Metro/Global mirror copy relationship of the volumes ( if required )
 - Safeguarded Copy volumes alocation

## run-cr-wflow-ds8k.py ##

The script is a python implementation of a wrapper to invoke CSM API commands to interact with DS8K storage to invoke DS8K - Safeguarded Copy functionality. It is deployed in IBM QRadar environment with a set of parameters shown below by the Usage section.

### Usage ###

Usage: run-cr-wflow-ds8k.py [-h] -s CSM_SERVER [-P CSM_PORT] -u CSM_USER -p CSM_USER_PASSWD -t CSM_TASK

Following arguments are required: <br>
      -s/--csm_server <br>
      -u/--csm_user   <br>
      -p/--csm_user_passwd <br>
      -t/--csm_task <br>

## Other resources ##

### [Blueprint](https://www.redbooks.ibm.com/abstracts/redp5677.html?Open) ###
