import os
import time
from multiprocessing import Process
from mail import EmailSender

class FileObserver:
    def __init__(self, interval, count_threshold, observe_dir, instr, screen_shot):
        self.interval = interval*60
        self.count_threshold = count_threshold
        self.dir = observe_dir
        self.instr = instr
        self.screen_shot = screen_shot
        self.email_sender = None
        self.process = None

        self.previous_file_count = None
        self.counter = 0

    def count_files(self):
        #Counts the number of files in the specified directory.
        return sum(os.path.isfile(os.path.join(self.dir, name)) for name in os.listdir(self.dir))

    def observe(self):
        #Observes the directory for changes in file count.
        print(f'Observer process started with PID {os.getpid()}.')
        while True:
            current_file_count = self.count_files()
            print(f'Total files: {current_file_count}')

            if current_file_count != self.previous_file_count:
                self.counter = 0
            else:
                self.counter += 1

            if self.counter >= self.count_threshold:
                print('No new files found. Exiting observer process.')
                self.email_sender.run(self.screen_shot)
                break

            print(f'Observer process is running with PID {os.getpid()}.')
            self.previous_file_count = current_file_count
            time.sleep(self.interval)

    def start(self):
        self.email_sender = EmailSender(dir=self.dir, instr=self.instr)
        self.process = Process(target=self.observe)
        print(f'Main process started with PID {os.getpid()}.')
        print('Starting observer process.')
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            print('Observer process terminated.')
            self.process = None
        else:
            print('Observer process is not running.')

