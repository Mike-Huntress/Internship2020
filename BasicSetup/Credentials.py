from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials


DataSourceCredentials().addCredentials("datastream", "meganhoward@college.harvard.edu", "Brag352iffy412?")
DataSourceCredentials().readCredentials("datastream").print()