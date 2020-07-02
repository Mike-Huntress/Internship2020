from DataIO.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "Your Username", "Your Password")
DataSourceCredentials().readCredentials("datastream").print()