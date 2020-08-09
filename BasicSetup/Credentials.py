import sys
sys.path.append('.')

from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "Your Username", "Your Password")
DataSourceCredentials().readCredentials("datastream").print()
