import configparser


from ..base import SingletonMeta


class Task(metaclass=SingletonMeta):
    def __init__(self, args) -> None:
        self.conf_file = args.config

        self.bot_token: str = ""

        self.pfgo_url: str = ""
        self.username: str = ""
        self.password: str = ""
        self.hide: list = []

        self.webhook_url = ""
        self.webhook_port = ""
        self.running_host = ""
        self.running_port = 0

        self._init_conf()

    def _init_conf(self):
        config = configparser.ConfigParser()
        config.read(self.conf_file)
        self.bot_token = config.get("bot", "token")

        self.pfgo_url = config.get("pfgo", "url")
        self.username = config.get("pfgo", "username")
        self.password = config.get("pfgo", "password")
        self.hide += config.get("pfgo", "hide").split(",")

        self.webhook_url = config.get("webhook", "webhook_url")
        self.webhook_port = config.get("webhook", "webhook_port")
        self.running_host = config.get("webhook", "running_host")
        self.running_port = int(config.get("webhook", "running_port"))
