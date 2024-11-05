import subprocess
import shlex


class video():
    def __init__(
            self,
            requested,
            command,
            process
        ):
        self.id = 0
        self.status = False
        self.requested = requested
        self.last = ""
        self.lasts = []
        self.command = command
        self.process = process

        self.getId()

    def active(self):
        self.status = True

    def deactive(self):
        self.staus = False

    def addLine(self):
        self.last = self.process.stdout.readline()


        if len(self.lasts) > 50:
            self.lasts.pop(0)
            
        self.lasts.append(self.process.stdout.readline())

    def getId(self):
        # ps aux | grep gst
        try:
            self.id = self.process.pid
            return True
        except:
            return False