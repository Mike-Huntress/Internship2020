from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "username", "password")
DataSourceCredentials().readCredentials("datastream").print()
