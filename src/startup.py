import valclient, time, traceback, psutil, os, ctypes

from .utilities.processes import Processes
from .utilities.filepath import Filepath
from .utilities.logging import Logger
from .utilities.rcs import Riot_Client_Services
from .utilities.killable_thread import Thread
from .utilities.updater import Updater
from .utilities.logging import Logger
from .presence.presence import Presence
from win10toast_click import ToastNotifier


class Startup:
    def __init__(self):
        if not Processes.is_program_already_running():
            Logger.create_logger()
            self.client = None
            self.region = self.check_region()
                
            try:
                self.presence = Presence()
            except Exception:
                traceback.print_exc()
                ctypes.windll.user32.MessageBoxW(0, u"Discord not detected. Starting VALORANT without presence.\nOpen your Discord and start the program again.\n\nPress OK to launch VALORANT and exit.", u"Error (VALORANT-RPC)", 16)
                if not Processes.are_processes_running():
                    self.start_game()
                    os._exit(1)
            
            self.run()
            
        else:
            if ctypes.windll.user32.MessageBoxW(0, f"Seems like the RPC program is already running. Would you like to exit all instances?", "Already running! (VALORANT-RPC)", 4 | 0x30) == 6:
                Processes.terminate_all_processes()
            else:
                os._exit(0)
            
    def run(self):
        self.presence.update_presence("startup")
        # ? Part of my automatic updater I planned to release, check utilities/updater.py
        #if Updater.is_admin():
        #    version, download_url = Updater.get_download_url()
        #    Updater.update_program(download_url, version)
        #else:
        #    Updater.check_for_new_version(self.config)
        
        Updater.check_for_new_version("balls")
        if not Processes.are_processes_running():
            self.start_game()
        self.setup_client()
        ToastNotifier().show_toast(
            title = "Now running!",
            msg = "Your status is now being enhanced.\nRun the program again to exit.",
            icon_path = Filepath.get_path('favicon.ico'),
            threaded = True
        )
        if self.client.fetch_presence() is None:
            self.wait_for_presence()
        self.dispatch_presence()
        self.presence_thread.stop()

        
        
    def setup_client(self):
        try:
            self.client = valclient.Client(region = self.region)
            self.client.activate()
            self.presence.client = self.client
        except Exception as e:
            Logger.debug("setup_client: " + str(e))
            
    
    def wait_for_presence(self):
        presence_timeout = 60
        presence_timer = 0
        print()
        while self.client.fetch_presence() is None:
            presence_timer += 1
            if presence_timer >= presence_timeout:
                ctypes.windll.user32.MessageBoxW(0, f"Presence Timeout.\nMake sure you are not playing any other game that might be overriding your Discord status, and launch the program again.\n\nPress OK to exit.", u"Error (VALORANT-RPC)", 16)
                os._exit(1)
            time.sleep(1)
            
    
    def dispatch_presence(self):
        self.presence_thread = Thread(target = self.presence.init_loop(), daemon = True)
        self.presence_thread.start()
    
    
    def check_region(self):
        if not Processes.are_processes_running():
            self.start_game()
                    
        client = valclient.Client(region = "eu")
        client.activate()
        sessions = client.riotclient_session_fetch_sessions()
        for _, session in sessions.items():
            if session["productId"] == "valorant":
                launch_args = session["launchConfiguration"]["arguments"]
                for arg in launch_args:
                    if "-ares-deployment" in arg:
                        region = arg.replace("-ares-deployment=", "")
                        return region
                        
                        
    def start_game(self):
        path = Riot_Client_Services.get_rcs_path()
        launch_timeout = 60
        launch_timer = 0
        
        psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Processes.are_processes_running():
            launch_timer += 1
            if launch_timer >= launch_timeout:
                ctypes.windll.user32.MessageBoxW(0, u"VALORANT launch timeout.\nIs VALORANT running? Restart the program\n\nPress OK to exit", u"Error (VALORANT-RPC)", 16)
                os._exit(1)
            time.sleep(1)
            