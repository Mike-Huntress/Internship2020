from DataIO.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "ZBDW073", "MOTOR315")
DataSourceCredentials().readCredentials("datastream").print()