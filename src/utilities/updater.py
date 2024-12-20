import requests

GITHUB_REPO = "https://api.github.com/repos/KEA12/valorant-rpc/releases/latest"

class Updater:
    
    @staticmethod
    def check_for_new_version(config):
        data = requests.get(GITHUB_REPO)
        print(data)
        if data.status_code == 200:
            latest = data.json()["tag_name"]
            print(latest)
            
Updater.check_for_new_version("penis")
