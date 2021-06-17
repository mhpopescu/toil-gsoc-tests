import os

from toil.common import Toil
from toil.job import Job
from toil.lib.docker import apiDockerCall


# working_dir = Job.fileStore.getLocalTempDir()
align = Job.wrapJobFn(apiDockerCall,
                      image='curii/bwa-samtools',
                      working_dir=os.getcwd(),
                      entrypoint=['/bin/bash', '-c'],
                      parameters=['ls', '-lah'])
                      # parameters=['samtools', 'view', '-@', '10', '-b', '-S', '-', '>', ])

if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    options.clean = "always"

    with Toil(options) as toil:
       print(toil.start(align))
