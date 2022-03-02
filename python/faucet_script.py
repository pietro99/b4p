from dotenv import load_dotenv
import requests
import os
import time
load_dotenv()

faucet_address = os.getenv('FAUCET_ADDRESS')



url = "https://api.faucet.matic.network/transferTokens"

payload = "{\"network\":\"mumbai\",\"address\":\""+faucet_address+"\",\"token\":\"maticToken\"}"

headers = {
  'content-type': 'application/json;charset=UTF-8',
}

while True:
    response = {}
    try:  
      response = requests.request("POST", url, headers=headers, data=payload).json()
    except:
      print("an error occured waiting a bit longer...")
      time.sleep(320)
    if "hash" in response:
        print(response)
        print("0.5 Matic were sent to: " + faucet_address+"\n")
    elif "duration" in response:
        duration = abs(response["duration"])/1000
        print("account greylisted. waiting for "+str(duration)+" seconds\n")
        time.sleep(duration)
    else:
        print(response)
        print("limit reached")
        break

