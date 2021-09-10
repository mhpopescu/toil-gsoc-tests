# Test Toil co-scheduling with 2 jobs that stream the input and output
# Second job receive a promise from the first one
# First job returns after creating the file
# There is no synchronizing yet

import os
import threading
import time

from toil.common import Toil
from toil.fileStores import FileID
from toil.job import Job


def fn1(job, finid):
    def work(fileStore, finid, fileId, fileFlagID):
        time.sleep(1) # delay the writing to test that the reader is waiting for us
        with fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
            with fileStore.jobStore.updateFileStream(fileId, encoding='utf-8') as fo:
                fo.write(fi.read() + 'World!')
        fileStore.jobStore.deleteFile(fileFlagID)

    # # These get deleted when the job finishes...
    # absPath = job.fileStore.getLocalTempFile()
    # absPath = job.fileStore.jobStore._getUniqueFilePath("stream", cleanup=False)
    # fileID = FileID(absPath, 0)
    fileId = job.fileStore.jobStore.getEmptyFileStoreID()
    fileFlagID = job.fileStore.jobStore.getEmptyFileStoreID()

    th = threading.Thread(target=work, args=(job.fileStore, finid, fileId, fileFlagID))
    th.start()
    return fileId, fileFlagID

def fn2(job, promise, ioFileDirectory):
    finid, fileFlagID = promise
    while not job.fileStore.jobStore.fileExists(fileFlagID):
        # try again later
        time.sleep(1)

    with job.fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
        with job.fileStore.writeGlobalFileStream(encoding='utf-8') as (fo, foutid):
            print(foutid)
            while job.fileStore.jobStore.fileExists(fileFlagID):
                fo.write(fi.read())
                time.sleep(0.5)
            fo.write('World!')
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
