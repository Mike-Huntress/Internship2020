import getpass

from BasicSetupUtilities.CredentialsStoreBuilder import DataSourceCredentials

DataSourceCredentials().addCredentials(
    "datastream",
    input("Username: "),
    getpass.getpass("Password: ")
)
DataSourceCredentials().readCredentials("datastream")
