from flask import Flask, render_template,url_for
from Savoir import Savoir
import json

multichainRPCUser = 'multichainrpc'
multichainRPCPassword = 'test'
multichainRPCHost = '131.247.196.108'
multichainRPCPort = '2690'
multichainRPCChainName = 'maPitchChain'

global multichainmultichainSavoirObject

multichainSavoirObject = Savoir(multichainRPCUser, multichainRPCPassword, multichainRPCHost, multichainRPCPort, multichainRPCChainName)

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/hello')
def hello():
	return 'Hello world'
	
@app.route('/results')
def resultant():
	return render_template("results.html")
	
@app.route('/testuser1')
def testUser1():
	return "Welcome back, " + str(getUserRealName("TestUser1", multichainSavoirObject)) + "!<br>Current balance:" + str(getUserAccountBalance("TestUser1",multichainSavoirObject))


def getUserAddressBalance(userAddress, multichainSavoirObject):
	if userAddress == "1Kyj1SW8JK25YyW5RaVQSCjnHQ7YUMSbxgHZX2 ":
		i = 1
	else:
		i = 0
	userBalances = multichainSavoirObject.getaddressbalances(userAddress)[i]
	userBalancesJSON = json.dumps(userBalances)
	userJSONRead = json.loads(userBalancesJSON)
	userBalance = userJSONRead['qty']
	return userBalance
	
def getUserRealName(userName, multichainSavoirObject):
	userRealNameList = multichainSavoirObject.liststreamkeyitems('realNames',userName)
	i = len(userRealNameList) - 1
	userRealNameEntry = userRealNameList[i]
	userRealNameStreamJSON = json.dumps(userRealNameEntry)
	userRealNameJSONRead = json.loads(userRealNameStreamJSON)
	userRealNameHex = userRealNameJSONRead['data']
	userRealName = convertHexAddressToString(userRealNameHex)
	return userRealName


def convertHexAddressToString(hexAddressToConvert):
	return bytes.fromhex(hexAddressToConvert).decode('ascii')
	
def getUserHexAddress(userName, multichainSavoirObject):
	userStreamItem = multichainSavoirObject.liststreamkeyitems('users',userName)[0]
	userStreamJSON = json.dumps(userStreamItem)
	userJSONRead = json.loads(userStreamJSON)
	userHexAddress = userJSONRead['data']
	return userHexAddress

def getUserAddress(userName, multichainSavoirObject):
	userHexAddress = getUserHexAddress(userName, multichainSavoirObject)
	userAddress = convertHexAddressToString(userHexAddress)
	return userAddress
	
def getUserAccountBalance(userName, multichainSavoirObject):
	userAddress = getUserAddress(userName, multichainSavoirObject)
	userAccountBalance = getUserAddressBalance(userAddress, multichainSavoirObject)
	return userAccountBalance





