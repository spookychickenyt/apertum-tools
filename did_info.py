#!/usr/bin/python

import sys
from web3 import Web3
import jsonpickle
import json
import types
import datetime
from pycurl import Curl
from io import BytesIO
from io import StringIO




def print_break():
	print("==================================================================================");

#Parse Args
if len(sys.argv) != 2 or int(sys.argv[1]) < 0:
	sys.exit(f"Usage: {sys.argv[0]} DID")


# Connect to Apertum RPC
APERTUM_RPC = "https://rpc.apertum.io/ext/bc/YDJ1r9RMkewATmA7B35q1bdV18aywzmdiXwd9zGBq3uQjsCnn/rpc"
web3 = Web3(Web3.HTTPProvider(APERTUM_RPC))

# Contract and Token Details
contract_address = web3.to_checksum_address("0xDE72695e54Bb44bEB1844C35CD3eA50f4F785F2D")
tid = int(sys.argv[1])


with open("did_abi.json","r") as file:
	did_abi = json.load(file)


with open("miner_abi.json","r") as file:
	minebot_abi = json.load(file)


# --- INTERACT WITH CONTRACT ---


try:
	contract = web3.eth.contract(address=contract_address, abi=did_abi)




	owner = contract.functions.ownerOf(tid).call()
			

	parent = contract.functions.getParentId(tid).call()
	sponsorwallet = contract.functions.ownerOf(parent).call()

	childrencount = contract.functions.getChildrenCount(tid).call()
	kyc = contract.functions.isKycValid(tid).call()



	print(f"Information for DID {tid}")
	print_break()
	print(f"Owner Wallet    : {owner}")
	print(f"Sponsor ID      : {parent}")
	print(f"Sponsor Wallet  : {sponsorwallet}")
	
	print(f"KYC Status      : " + str(kyc))
	print(f"KYC Expiry      : " + str(datetime.datetime.fromtimestamp(contract.functions.getKycExpiry(tid).call())))


	buffer = BytesIO()

	token_url = "https://explorer.apertum.io/api/v2/addresses/" + owner
	c = Curl()
	c.setopt(c.URL, token_url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	response_body = buffer.getvalue()
	response = response_body.decode('utf-8')
	data = json.load(StringIO(response))


	balance = int(data["coin_balance"])*(10**-18)
	
	print(f"Balance         : {balance} APTM")
	
	buffer.truncate(0)  # Truncates the buffer to 0 bytes
	buffer.seek(0)

	print("")
	if childrencount > 0:

		print(f"This DID has {childrencount} direct children")	
		print_break()

		linect = 0

		for x in range(0,childrencount):
			child = contract.functions.getChild(tid,x).call()
			print(f"{child} ",end="")
			linect += 1
			if linect==15 and x != childrencount:
				linect=0
				print("")
		print("")
	else:
		print(f"This DID has no children on record")		
	

	print("")






	token_url = "https://explorer.apertum.io/api/v2/addresses/" + owner + "/token-balances"
	c = Curl()
	c.setopt(c.URL, token_url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	response_body = buffer.getvalue()
	response = response_body.decode('utf-8')
	data = json.load(StringIO(response))


	print("Token                     Symbol       Value")
	print_break()

	minebotcount = 0

	for x in range(0,len(data)):
	
		token_name = data[x]["token"]["name"]
		token_symbol = data[x]["token"]["symbol"]
		token_value = data[x]["value"]
		token_dec = data[x]["token"]["decimals"]
		if token_dec == None:
			token_dec=0
					
		
		try:
			real_value = int(token_value) * (10 ** (int(token_dec) * -1))
			print(token_name.ljust(26," ") ,end="")
			print(token_symbol.ljust(13," ") ,end="")
			print(str(real_value),end="")
			print()
			
			if token_symbol == "MineBot":
				minebotcount = real_value
			
			
		except Exception as e:
			print("Error:", e)
			
	buffer.truncate(0)  # Truncates the buffer to 0 bytes
	buffer.seek(0)



	token_url = "https://explorer.apertum.io/api/v2/addresses/" + owner + "/nft?type=ERC-721,ERC-404,ERC-1155"
	c = Curl()
	c.setopt(c.URL, token_url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	response_body = buffer.getvalue()
	response = response_body.decode('utf-8')
	data = json.load(StringIO(response))

	print()
	print("Token                     Symbol        Class                Price     Id")
	print_break()

	for x in range(0,len(data["items"])):
	
		nft_id = data["items"][x]["id"]
		nft_name = data["items"][x]["token"]["name"]
		nft_symbol = data["items"][x]["token"]["symbol"]

		if nft_name == "MineBot" or nft_name == "TradeBot":




		
			if data["items"][x]["metadata"] != None:

				metadata_name = str(data["items"][x]["metadata"]["name"])
				metadata_price = str(data["items"][x]["metadata"]["attributes"][2]["value"])
			

			else:

				metadata_name = "Unknown"
				metadata_price = "Unknown"
	

		
			try:




				minebot_address = web3.to_checksum_address("0xa1b761890c36e356f49F9DF8D495FcFFa76857ad")
				minebot = web3.eth.contract(address=minebot_address, abi=minebot_abi)
				owner = minebot.functions.ownerOf(int(nft_id)).call()
				getinfo = minebot.functions.getMinerInfo(int(nft_id)).call()
#			getminted = minebot.functions.mint(int(nft_id),owner,getinfo[1],31999999).call()




				print(nft_name.ljust(26," ") ,end="")
				print(nft_symbol.ljust(13," ") ,end="")
				print(" (" + str(getinfo[1]) + ")",end="")
				print(metadata_name.ljust(19," ") ,end="")
				print(str(metadata_price).ljust(8," ") ,end="")
#				print("  " + str(round(getinfo[7] / minebot.functions.ONE_COIN().call() ,5)).rjust(10," ") + " ",end="")

				print(" " + str(nft_id),end="")
				#print(str(nft_id),end="")
				#print(" : " + str(minebot.functions.ONE_COIN().call()))
				print()

			
	
			except Exception as e:
				print("Error:", e)
	
	

	
	
	buffer.truncate(0)  # Truncates the buffer to 0 bytes
	buffer.seek(0)

	
except Exception as e:
	print("Fatal Error:", e)




