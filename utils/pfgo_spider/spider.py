import requests
import urllib.parse

from ..log import Logmanager


class PfgoSpider:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.logger = Logmanager.create_logger("PfgoSpider")
        self.url = url
        self.username = username
        self.password: str = urllib.parse.quote(password, safe="")
        self.cookie: str = ""

    def login(self) -> str:
        try:
            url = f"{self.url}/ajax/login"
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "DNT": "1",
                "Pragma": "no-cache",
                "Referer": f"{self.url}/login",
                "Sec-Ch-Ua": '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
                "X-Requested-With": "XMLHttpRequest",
            }
            data = {"username": self.username, "password": self.password}
            resp = requests.post(url, headers=headers, data=data)
            if not resp.text == '{"Ok":true}':
                self.logger.info("登录失败: 账户密码错误")
                return "登录失败: 账户密码错误"
            self.cookie = (resp.headers["set-cookie"]).split(";")[0]
            self.logger.info("登录成功")
            return ""
        except Exception as e:
            self.logger.info(f"登录失败: {e}")
            return f"登录失败: {e}"

    def get_forward_rules(self):
        self.login()
        rules = self._get_forward_rules()
        statistics = self._get_statistics()
        return self._rules_statistics_summary(rules, statistics)

    def _get_forward_rules(self) -> list:
        url = f"{self.url}/ajax/forward_rule"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "authority": self.url.split("//")[-1],
            "cache-control": "no-cache",
            "cookie": self.cookie,
            "dnt": "1",
            "pragma": "no-cache",
            "referer": f"{self.url}/forward_rules",
            "sec-ch-ua": '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
            "x-requested-with": "XMLHttpRequest",
        }
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        return resp_json["Data"]

    def _get_statistics(self):
        url = f"{self.url}/ajax/forward_rule/statistics"
        headers = {
            "authority": self.url.split("//")[-1],
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": self.cookie,
            "dnt": "1",
            "pragma": "no-cache",
            "referer": f"{self.url}/forward_rules",
            "sec-ch-ua": '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
            "x-requested-with": "XMLHttpRequest",
        }
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        return resp_json["Data"]

    def _rules_statistics_summary(self, rules: list, statistics: list):
        total = {}
        for rule in rules:
            total[rule["id"]] = {"name": rule["name"]}

        for one_statistics in statistics:
            if one_statistics["rule_id"] in total:
                if "traffic" in total[one_statistics["rule_id"]]:
                    total[one_statistics["rule_id"]]["traffic"] += one_statistics[
                        "traffic"
                    ]
                else:
                    total[one_statistics["rule_id"]]["traffic"] = one_statistics[
                        "traffic"
                    ]
        # 将字节转换为G / 1073741824
        for k, v in total.items():
            total[k]["traffic"] = round(total[k]["traffic"] / 1073741824, 2)
        return total
