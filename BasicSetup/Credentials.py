import sys
sys.path.append('.')

from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials
import json

myCredentials_filename = "/Users/rogerio/Desktop/Bridgewater/Intership2020/BasicSetup/credentials_Rogerio.Guimaraes.json"

with open(myCredentials_filename) as f:
    credentials = json.load(f)
    username = credentials['username']
    password = credentials['password']

DataSourceCredentials().addCredentials("datastream", username, password)
DataSourceCredentials().readCredentials("datastream").print()