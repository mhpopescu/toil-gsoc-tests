import errno
import os
import threading
import subprocess
from toil.common import Toil
from toil.job import Job

class SamtoolsRun(Job):
    def __init__(self, id):
        Job.__init__(self, memory="2G", cores=10, disk="10G")
        self.inputFileID = id

    def writeToPipe(self, fn):
        with open(self.inputFileID, 'rt') as fi:
            fifo = open(fn, 'wt')
            fifo.write(fi.read())
            fifo.close()

    def run(self,fileStore):
        fn = 'tmp'
        os.mkfifo(fn)

        th = threading.Thread(target=self.writeToPipe, args=(fn,))
        th.start()

        with open(fn, 'rt') as fi:
            fon = "out.txt"
            with open(fon, 'wt') as fo:
                parameters = ['cat']
                subprocess.run(parameters, stdin=fi, stdout=fo)

                th.join()
                return fileStore.writeGlobalFile(fon)


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:

        fileDirectory = os.path.dirname(os.path.abspath(__file__))

        if not toil.options.restart:
            inputFileID = toil.importFile("file://" + os.path.abspath(os.path.join(fileDirectory, "hello_world.txt")))
            outputFileID = toil.start(SamtoolsRun(inputFileID))
        else:
            outputFileID = toil.restart()

        toil.exportFile(outputFileID, "file://" + os.path.abspath(os.path.join(fileDirectory, "out-fifo-cat-toil.txt")))



