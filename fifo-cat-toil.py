import errno
import os
import threading
import subprocess
from toil.common import Toil
from toil.job import Job

class SamtoolsRun(Job):
    def __init__(self, id):
        Job.__init__(self, memory="2G", cores=10, disk="10G")
        self.inputFileName = id

    def writeToPipe(self, fn, fileStore):
        with open(self.inputFileName, 'rt') as fi:
            fifo = open(fn, 'wt')
            fifo.write(fi.read())
            fifo.close()

    def run(self,fileStore):
        fn = 'tmp'
        os.mkfifo(fn)

        th = threading.Thread(target=self.writeToPipe, args=(fn,fileStore))
        th.start()

        with open(fn, 'rt') as fi:
            fon = "out.txt"
            with open(fon, 'wt') as fo:
                parameters = ['cat']
                subprocess.run(parameters, stdin=fi, stdout=fo)

                th.join()
                return fileStore.writeGlobalFile(fon)


if __name__=="__main__":

    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args(args=["./toilWorkflowRun", "--debugWorker"])

    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:

        fileDirectory = os.path.dirname(os.path.abspath(__file__))

        if not toil.options.restart:
            inputFileName = os.path.abspath(os.path.join(fileDirectory, "hello_world.txt"))
            outputFileID = toil.start(SamtoolsRun(inputFileName))
        else:
            outputFileID = toil.restart()

        toil.exportFile(outputFileID, "file://" + os.path.abspath(os.path.join(fileDirectory, "out-fifo-cat-toil.txt")))



