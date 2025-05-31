from patterns.singleton import Singleton
import datetime

class Logger(Singleton):
    """
    Logger class for notifications
    implements singleton 
    """
    
    def startLog(self):
        """
        Creates the logfile and/or writes a timestamp
        """
        self.log_file = "notification_log.txt"
        with open(self.log_file, "a") as f:
            f.write(f"---- Log started at {datetime.datetime.now()} ----\n")
        
    
    def log(self,message):
        """
        Writes a log into the file, and to the console
        in a specific time format
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file,"a") as f:
            f.write(log_entry)
        print(log_entry.strip())