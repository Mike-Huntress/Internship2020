from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "", "")
DataSourceCredentials().readCredentials("datastream").print()