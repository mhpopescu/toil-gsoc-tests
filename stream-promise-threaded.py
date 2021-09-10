# Test Toil co-scheduling with 2 jobs that stream the input and output
# Second job receive a promise from the first one
# First job returns after creating the file
# There is no synchronizing yet

import os
import threading

from toil.common import Toil
from toil.fileStores import FileID
from toil.job import Job


def fn1(job, finid):
    def work(job, finid, absPath):
        # time.sleep(10) - this would break it because there is no wait for reading the file
        with job.fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
            with open(absPath, "wt") as fo:
                fo.write(fi.read() + 'World!')

    # absPath = job.fileStore.getLocalTempFile() # this gets deleted ...
    absPath = job.fileStore.jobStore._getUniqueFilePath("stream", cleanup=False)
    fileID = FileID(absPath, 0)
    th = threading.Thread(target=work, args=(job, finid, absPath))
    th.start()
    return fileID

# Not working because fo is closed and the other thread can not write to it
# Need something like "createFileStream"
# ==> Have to open the filestream inside the thread
def fn1_closed(job, finid):
    def work(job, finid, fo):
        with job.fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
            fo.write(fi.read() + 'World!')

    name = "stream"
    with job.fileStore.writeGlobalFileStream(name, encoding='utf-8') as (fo, foutid):
        th = threading.Thread(target=work, args=(job, finid, fo))
        th.start()
    return foutid

def fn2(job, finid, ioFileDirectory):
    with job.fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
        with job.fileStore.writeGlobalFileStream(encoding='utf-8') as (fo, foutid):
            fo.write(fi.read() + 'World!')
            print(foutid)
    job.fileStore.exportFile(foutid, "file://" + os.path.abspath(os.path.join(ioFileDirectory, "out-stream-promise.txt")))
    return foutid


if __name__=="__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    # options = parser.parse_args(args=["./toilWorkflowRun", "--debugWorker"])
    options = parser.parse_args(args=["./toilWorkflowRun", "--debugWorker", "--disableCaching"])

    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:
        ioFileDirectory = os.path.dirname(os.path.abspath(__file__))
        inputFileID = toil.importFile("file://" + os.path.abspath(os.path.join(ioFileDirectory, "hello_world.txt")))

        j1 = Job.wrapJobFn(fn1, inputFileID)
        j2 = Job.wrapJobFn(fn2, j1.rv(), ioFileDirectory)
        j1.addFollowOn(j2)
        toil.start(j1)
