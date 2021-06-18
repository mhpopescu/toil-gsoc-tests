import errno
import os
import threading
import subprocess


class SamtoolsRun():
    def __init__(self, id):
        self.inputFileID = id

    def writeToPipe(self, fn):
        with open(self.inputFileID, 'rt') as fi:
            fifo = open(fn, 'wt')
            fifo.write(fi.read())
            fifo.close()

    def run(self,):
        fn = 'tmp'
        os.mkfifo(fn)

        th = threading.Thread(target=self.writeToPipe, args=(fn,))
        th.start()

        with open(fn, 'rt') as fi:
            with open('out.txt', 'wt') as fo:
                parameters = ['cat']
                subprocess.run(parameters, stdin=fi, stdout=fo)

                th.join()


if __name__=="__main__":
    inFile = os.path.abspath("hello_world.txt")
    sr = SamtoolsRun(inFile)
    sr.run()

