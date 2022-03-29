# Safeguarding Data with IBM QRadar and IBM Copy Services Manager on IBM DS8000 #

This repository contains the sample script used as part of Cyber Resiliency (CR) workflow. The CR workflow is a response to a threat detected by IBM QRadar. Upon invocation, the script makes several API calls to IBM Copy Services Manager (CSM) to execute SafeguardedCopy function on DS8000 storage.

# IBM Documentation #

Refer to Resources section for various links to IBM Documentation about IBM DS8000, Copy Services Manager and also the solution blueprint.

# Support #

The **_sample_** Python code available in the repository is created as part of solution. There is no official support on the code. 

# Disclaimer #

The script is purely created as a PoC and it is developed and tested in controlled lab environment. There is **_no_** official support on the script. You may use the script as a template to create your own workflow. 

## Workflow ##

For both control and data path use cases, we heavily depend on the audit logs, network flows in order to track the actions. IBM QRadar is used for threat detection. The audit logs from storage and network flows / logs are used to determine whether the storage is under attack. This is done using IBM QRadar's rules engine, and when the threat is detected a pre-defined custom action is triggered ( in this case .py ) that will execute series API calls using CSM server on DS8K storage system to an immutable backup of the data. 

## Pre-requisites ##

Following section lists the pre-requisites.

 - Copy Services Manager installation
 - Identification of volumes that needs safeguarding
 - Metro/Global mirror copy relationship of the volumes ( if required )
 - Safeguarded Copy volumes alocation

## run-cr-wflow-ds8k.py ##

The script is a python implementation of a wrapper to invoke CSM API commands to interact with DS8K storage to invoke DS8K - Safeguarded Copy functionality. It is deployed in IBM QRadar environment with a set of parameters shown below by the Usage section.

## Usage ##
```
Usage: run-cr-wflow-ds8k.py [-h] -s CSM_SERVER [-P CSM_PORT] -u CSM_USER -p CSM_USER_PASSWD -t CSM_TASK

Following arguments are required:
      -s/--csm_server 
      -u/--csm_user   
      -p/--csm_user_passwd
      -t/--csm_task
```

## Resources ##

### [IBM DS8000 SafeguardedCopy](https://www.ibm.com/docs/en/ds8880/8.5.4?topic=license-safeguarded-copy) ###
### [IBM Copy Services Manager](https://www.ibm.com/docs/en/csm) ###
### [Solution Blueprint](https://www.redbooks.ibm.com/abstracts/redp5677.html?Open) ###
