import errno
import os
import threading
import subprocess


class SamtoolsRun():
    def __init__(self, id):
        self.inputFileID = id

    def writeToPipe(self, fn):
        with open(self.inputFileID, 'rb') as fi:
            fifo = open(fn, 'wb')
            # FIXME read & write like a stream, not whole file
            # this would depend on the type of filestore
            fifo.write(fi.read())

    def run(self,):
        fn = 'tmp'
        os.mkfifo(fn)

        th = threading.Thread(target=self.writeToPipe, args=(fn,))
        th.start()

        fi = open(fn, 'rb')

        with open('ERR2122556-fifo-sam.bam', 'wb') as fo:
            parameters = ['samtools', 'view', '-@', '10', '-b', '-S', '-']
            subprocess.run(parameters, stdin=fi, stdout=fo)

            th.join()


if __name__=="__main__":
    inFile = os.path.abspath("/media/mike/D/vu/chr19/ERR2122556.sam")
    sr = SamtoolsRun(inFile)
    sr.run()

