# Test Toil promise feature with 2 jobs that stream the input and output

import os
from toil.common import Toil
from toil.job import Job


def fn1(job, finid, ioFileDirectory, export=False):
    with job.fileStore.readGlobalFileStream(finid, encoding='utf-8') as fi:
        with job.fileStore.writeGlobalFileStream(encoding='utf-8') as (fo, foutid):
            fo.write(fi.read() + 'World!')
            print(foutid)
    if export:
        job.fileStore.exportFile(foutid, "file://" + os.path.abspath(os.path.join(ioFileDirectory, "out-stream-promise.txt")))

    return foutid

if __name__=="__main__":
    parser = Job.Runner.getDefaultArgumentParser()
    options = parser.parse_args(args=["./toilWorkflowRun", "--debugWorker"])

    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:
        ioFileDirectory = os.path.dirname(os.path.abspath(__file__))
        inputFileID = toil.importFile("file://" + os.path.abspath(os.path.join(ioFileDirectory, "hello_world.txt")))

        j1 = Job.wrapJobFn(fn1, inputFileID, ioFileDirectory)
        j2 = Job.wrapJobFn(fn1, j1.rv(), ioFileDirectory, True)
        j1.addFollowOn(j2)
        toil.start(j1)
