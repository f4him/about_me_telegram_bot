from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()


config_object["MyInfo"] = {
    "name": "Fahim Shahriar",
    "institution": "Chittagong University of Engineering & Technology",
	"degree":"B.Sc."
	"dept":"Computer Science & Engineering"
}

config_object["SERVERCONFIG"] = {
    "host": "tutswiki.com",
    "port": "8080",
    "ipaddr": "8.8.8.8"
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
