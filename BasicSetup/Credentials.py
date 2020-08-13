from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials

DataSourceCredentials().addCredentials("datastream", "Username", "Password")
DataSourceCredentials().readCredentials("datastream").print()