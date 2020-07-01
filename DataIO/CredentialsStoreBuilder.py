import os, shutil, configparser

class SourceCredentials:
    def __init__(self, source, user, password):
        self.source = source
        self.user = user
        self.password = password
    def source(self):
        self.source
    def user(self):
        self.user
    def password(self):
        self.password

def buildConfig(source, user,password):
    config = configparser.ConfigParser()

    config.add_section(source)
    config[source]['user'] = user
    config[source]['password'] = password

    with open("default_config.ini", 'w') as f:
        config.write(f)

def addCredentials(source, user, password):
    user_config_dir = os.path.expanduser("~") + "/ConfigKeys"
    user_config = user_config_dir + "/user_config.ini"

    if not os.path.isfile(user_config):
        os.makedirs(user_config_dir, exist_ok=True)
        buildConfig(source, user, password)
        shutil.copyfile("default_config.ini", user_config)
        os.remove("default_config.ini")

    config = configparser.ConfigParser()
    config.read(user_config)

    if not config.has_section(source):
        config.add_section(source)

    config[source]['user'] = user
    config[source]['password'] = password

    ##Write
    with open(user_config, 'w') as f:
        config.write(f)






addCredentials("datastream", "MikeH", "TestPassword")




