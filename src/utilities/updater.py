# !
# !
# !
# !     The commented functions here were gonna be part of my automatic updating feature
# !     that updates the .exe automatically for you without having to manually download it.
# !     However at the moment I'm too lazy to figure out an efficient way to do that,
# !     so I've left the WIP code here
# !
# !
# ! 



import requests, ctypes, webbrowser, os

from ..mapping.reader import Reader

GITHUB_REPO = "https://api.github.com/repos/KEA12/valorant-rpc/releases/latest"
USER_FRIENDLY = "https://github.com/KEA12/valorant-rpc/releases/latest"

class Updater:
    
    @staticmethod
    def get_download_url():
        data = requests.get(GITHUB_REPO)
        if data.status_code == 200:
            json = data.json()
            latest_version = json.get("tag_name")
            return latest_version
        else:
            if ctypes.windll.user32.MessageBoxW(0, f"Failed to check for updates. Status code: {data.status_code}\n\nRetry?", "Warning (VALORANT-RPC)", 5 | 0x30) == 4:
                    Updater.check_for_new_version(GITHUB_REPO)
    
    
    #@staticmethod
    #def is_admin():
    #    try:
    #        return ctypes.windll.shell32.IsUserAnAdmin()
    #    except:
    #        return False
    #    
    #@staticmethod
    #def run_as_admin():
    #    try:
    #        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)
    #        sys.exit(0)
    #    except Exception as e:
    #        ctypes.windll.user32.MessageBoxW(0, f"Failed to run as Admin:\n{e}\n\nYou can try to manually download the latest version.\nPress OK to exit.", u"Error (VALORANT-RPC)", 16)
    #        sys.exit(1)
    #        
    
    @staticmethod
    def check_for_new_version(config):
        current_version = Reader.get_config_value("version")
        latest_version = Updater.get_download_url()
        if latest_version and latest_version != current_version:
            Updater.prompt_update(latest_version)
                
            

    @staticmethod
    def prompt_update(latest_version):
        if ctypes.windll.user32.MessageBoxW(0, f"A new update for VALORANT RPC is available: {latest_version}\n\nWould you like to open the Github page?", "Update Available (VALORANT-RPC)", 4 | 0x20) == 6:
            webbrowser.open(USER_FRIENDLY)
            os._exit(0)
    
    #@staticmethod
    #def update_program(download_url, latest_version):
    #    try:
    #        current_exe = sys.executable
    #        new_exe = current_exe + ".new"
    #        data = requests.get(download_url, stream = True)
    #        if data.status_code == 200:
    #            with open(new_exe, "wb") as f:
    #                for chunk in data.iter_content(chunk_size = 8192):
    #                    if chunk:
    #                        f.write(chunk)
    #                        
    #                        
    #            updater_script = current_exe + "_updater.bat"
    #            with open(updater_script, "w") as f:
    #                f.write(f"""
    #                        @echo off
    #                        timeout /t 2 > nul
    #                        :retry
    #                        tasklist | find /i "{os.path.basename(current_exe)}" > nul
    #                        if not errorlevel 1 (
    #                            timeout /t 1 > nul
    #                            goto retry
    #                        )
    #                        move /y "{new_exe}" "{current_exe}"
    #                        start "" "{current_exe}"
    #                        del "%~f0"
    #                        """)
    #                
    #            
    #            subprocess.Popen(["cmd", "/c", updater_script], close_fds = True)
    #            Config.update_version(latest_version)
    #            ctypes.windll.user32.MessageboxW(0, "Update finished successfully.\n\nPress OK to run the new version.", "Update complete (VALORANT-RPC)", 0x40)
    #            sys.exit(0)
    #            
    #        else:
    #            if ctypes.windll.user32.MessageBoxW(0, f"Failed to fetch newest version. Status code: {data.status_code}\n\nRetry?", "Warning (VALORANT-RPC)", 5 | 0x30) == 4:
    #                Updater.check_for_new_version(download_url)
    #    
    #    except Exception as e:
    #        ctypes.windll.user32.MessageBoxW(0, f"Update failed!\n{e}\n\nYou can try to manually download the latest version.\nPress OK to exit.", u"Error (VALORANT-RPC)", 16)
    #        os._exit(1)