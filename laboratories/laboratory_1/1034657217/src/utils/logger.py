from patterns.singleton import Singleton
import datetime

class Logger(Singleton):
    
    def startLog(self):
        self.log_file = "notification_log.txt"
        with open(self.log_file, "a") as f:
            f.write(f"---- Log started at {datetime.datetime.now()} ----\n")
        
    
    def log(self,message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file,"a") as f:
            f.write(log_entry)
        print(log_entry.strip())