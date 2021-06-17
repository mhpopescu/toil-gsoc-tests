import os
import subprocess
from toil.common import Toil
from toil.job import Job


class SamtoolsRun(Job):
    def __init__(self, id):
        Job.__init__(self,  memory="12G", cores=10, disk="10G")
        self.inputFileID = id

    def run(self, fileStore):
        with fileStore.readGlobalFileStream(self.inputFileID) as fi:
            with fileStore.writeGlobalFileStream() as (fo, outputFileID):
                parameters = ['samtools', 'view', '-@', '10', '-b', '-S', '-']
                fo.write(subprocess.check_output(parameters, input=fi.read()))
                return outputFileID


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

        toil.exportFile(outputFileID, "file://" + os.path.abspath(os.path.join(outFileDirectory, "ERR2122556.bam")))
