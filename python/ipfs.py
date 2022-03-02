import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()

class IpfsManager():
    def __init__(self):
        self.auth = (os.getenv('INFURA_IPFS_ID'), os.getenv('INFURA_IPFS_SECRET'))
        self.BASE_DIR = "https://ipfs.infura.io:5001/api/v0/"

    def add(self, data):
        files = {'file': json.dumps(data)}
        return requests.post(self.BASE_DIR+"add", files=files, auth=self.auth).json()

    def cat(self, hash):
        params = (('arg',hash),)
        return requests.post(self.BASE_DIR+"cat", params=params, auth=self.auth).json()

    def pin(self, hash):
        params = (('arg',hash),)
        return requests.post(self.BASE_DIR+"pin/add", params=params, auth=self.auth).json()

    def unpin(self, hash):
        params = (('arg',hash),)
        return requests.post(self.BASE_DIR+"pin/rm", params=params, auth=self.auth).json()