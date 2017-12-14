"""
import chatapi to send message to wit.ai, api.ai, or luis.ai

I'll have to come back to this to write some examples.

There is supposed to be a config.ini file with keys sitting in the same folder
"""
import requests, json, time, ConfigParser
from flask import session

config = ConfigParser.RawConfigParser()
config.read('config.ini')

def wit_interpret(text):
	#remember to ONLY send text, or a data object.
	# FIRST send a q, in response to an action, send a POST on the same session with no q, but with data body, 'update the context', 
	# the response to THAT post will be the question...
	# send query
	#send data with table in the body
	endpoint = "https://api.wit.ai/message"
	headers = {"Authorization":"Bearer " + config.get('witai',"WIT_TOKEN") ,"Content-Type": "application/json","Accept": "application/json"}
	params={"v":config.get('witai','WIT_VERSION'), "session_id": session.get('key','test'), "q":text}
	# I was trying to pass context keys in as data of the POST request as suggested by Context Example for timezone...
	#is it necessary fot the context to stick around in the next request?
	openTime = time.time()
	apiResult = requests.post(endpoint, headers=headers, params=params)
	closeTime = time.time()	
	
	try:
		witObj = apiResult.json()
		witObj['source'] = 'wit'
		witObj['roundTripTime'] = closeTime - openTime
		print("WIT2")
		print(witObj)
		return witObj
	except:
		witObj = {"error":"400"}
		print(witObj)
		return witObj

def apiai_interpret(text):
	endpoint = "https://api.api.ai/v1/query"
	headers = {"Authorization":"Bearer " + config.get('apiai',"APIAI_TOKEN")} 
	params = {"v":"20150910", "query":text, "lang":"en", "sessionId": session.get('key','test')} #this sessionId is used to track state, so this should change with user / user-session
	openTime = time.time()	
	apiObj = requests.get(endpoint, headers=headers, params=params)
	apiObj = apiObj.json()
	closeTime = time.time()	
	apiObj['source'] = 'apiai'
	apiObj['roundTripTime'] = closeTime - openTime
	return apiObj



def luis_interpret(text):
	endpoint = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/07c74d9b-04f4-489d-acec-a2bf7dbe2160"
	params = {"subscription-key": config.get('luis','LUIS_TOKEN'), "q":text, "verboe":"true"}
	openTime = time.time()	
	luisObj = requests.get(endpoint, params=params)
	luisObj = luisObj.json()	
	closeTime = time.time()
	luisObj['source'] = 'luis'
	luisObj['roundTripTime'] = closeTime - openTime
	return luisObj
