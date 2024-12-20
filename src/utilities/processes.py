import psutil

class Processes:
    
    @staticmethod
    def is_program_already_running():
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
        
        if len([proc for proc in processes if proc == "VALORANT-RPC.exe"]) > 2:
            return True
        
        return False
    
    @staticmethod
    def are_processes_running(required_processes = ["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
            
        return set(required_processes).issubset(processes)