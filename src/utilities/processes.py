import psutil, sys, os, ctypes

class Processes:
    
    @staticmethod
    def is_program_already_running():
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
        
        if len([proc for proc in processes if proc == str(os.path.basename(sys.executable))]) > 2:
            return True
        
        return False
    
    @staticmethod
    def are_processes_running(required_processes = ["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
            
        return set(required_processes).issubset(processes)
    
    
    @staticmethod
    def terminate_all_processes():
        current_exe = os.path.basename(sys.executable)
        current_exe_pid = os.getpid()
        for proc in psutil.process_iter():
            if proc.name() == current_exe:
                if not proc.pid == current_exe_pid:
                    proc.terminate()
        os._exit(0)
        
    
    @staticmethod
    def notification_close_program():
        if ctypes.windll.user32.MessageBoxW(0, f"Are you sure you want to exit?", "Are you sure? (VALORANT-RPC)", 4 | 0x20) == 6:
            Processes.terminate_all_processes()
        else:
            return