This repo would contain files that help test implementing streaming for toil-cwl-runner

[bwamem-samtools-view](https://github.com/arvados/arvados-tutorial/blob/master/WGS-processing/cwl/helper/bwamem-samtools-view.cwl) step is split in 2 steps that could use streaming: bwamem and samtools-view. For the second step I created the pure python toil workflow.
