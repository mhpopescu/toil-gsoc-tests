import errno
import os
import subprocess
import threading

from toil.common import Toil
from toil.job import Job


class SamtoolsRun(Job):
    def __init__(self, id):
        Job.__init__(self,  memory="12G", cores=10, disk="10G")
        self.inputFileID = id

    def writeToPipe(self, fn, fileStore):
        with fileStore.readGlobalFileStream(self.inputFileID) as fi:
            fifo = open(fn, 'wb')
            # FIXME read & write like a stream
            fifo.write(fi.read())
            fifo.close()


    def run(self, fileStore):
        fin = fileStore.getLocalTempFileName()
        os.mkfifo(fin)

        th = threading.Thread(target=self.writeToPipe, args=(fileStore,))
        th.start()

        with open(fin, 'rb') as fi:
            fon = fileStore.getLocalTempFile()
            with open(fon, 'wb') as fo:
                parameters = ['samtools', 'view', '-@', '10', '-b', '-S']
                subprocess.run(parameters, stdin=fi, stdout=fo)
                th.join()
                return fileStore.writeGlobalFile(fon)


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:
        inFileDirectory = os.path.abspath("/media/mike/D/vu/chr19/")
        outFileDirectory = os.path.dirname(os.path.abspath(__file__))

        if not toil.options.restart:
            inputFileID = toil.importFile("file://" + os.path.abspath(os.path.join(inFileDirectory, "ERR2122556.sam")))
            outputFileID = toil.start(SamtoolsRun(inputFileID))
        else:
            outputFileID = toil.restart()

        toil.exportFile(outputFileID, "file://" + os.path.abspath(os.path.join(outFileDirectory, "ERR2122556-fifo.bam")))
