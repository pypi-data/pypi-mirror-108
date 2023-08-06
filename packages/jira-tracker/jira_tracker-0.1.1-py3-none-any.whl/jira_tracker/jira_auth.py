from jira_tracker.logger import logger
import jira, yaml
import pathlib, os

class JiraAuth:
    def __init__(self):
        self.config = None

        # Intialize config
        self.load_config(self.config_location)

        if not "token" in self.config:
            self.stdin_configure()
            self.update_config(self.config_location)
        
        logger.debug("Successfully intialized JiraAuth!")

    

    def load_config(self, config_file):
        self.config = {}
        logger.debug(f"Loading config from: {config_file}")


        if self.config_location.exists():
            data = None

            # Load config file
            with open(config_file) as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
            
            # Update config with config data
            for key in data:
                self.config[key] = data[key]
        else:
            logger.warning(f"Config does not exist at: {config_file}")

    def update_config(self, config_file):
        if not config_file.exists():
            config_file.parent.mkdir(parents=True)

        with open(config_file, 'w') as f:
            data = yaml.dump(self.config, f)

    def stdin_configure(self):

        # Clear keys that need new inputs
        for key in ["server", "user", "token"]:
            self.config[key] = ""

        # Prompt sever
        print("Please enter the jira server to interface with")
        print("eg. jira.atlassian.com")
        while not "server" in self.config or self.config["server"] == "":
            self.config["server"] = input("Server: ")

        # Prompt Username
        print("Please enter your username")
        print("Example: user@domain.tld")
        while not "user" in self.config or self.config["user"] == "":
            self.config["user"] = input("Username: ")

        # Prompt Token
        print("Please generate a token and enter it here")
        print("https://id.atlassian.com/manage-profile/security/api-tokens")
        while not "token" in self.config or self.config["token"] == "":
            self.config["token"] = input("Token: ")

        if not "points_field" in self.config:
            self.config["points_field"] = "customfield_10016"

    def get_client(self):
        return jira.JIRA(self.config["server"], basic_auth=(self.config["user"], self.config["token"]))

    @property
    def config_location(self):
        return pathlib.Path(str(pathlib.Path.home()), ".jira-tracker", "config.yaml")