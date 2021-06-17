cwlVersion: v1.1
class: CommandLineTool
label: Align FASTQs with BWA - split second

requirements:
  DockerRequirement:
    dockerPull: curii/bwa-samtools
  ShellCommandRequirement: {}

hints:
  arv:RuntimeConstraints:
    keep_cache: 1024
    outputDirType: keep_output_dir
  ResourceRequirement:
    ramMin: 10000
    coresMin: 10
    outdirMin: 10000
  SoftwareRequirement:
    packages:
      BWA:
        specs: [ "https://identifiers.org/rrid/RRID:SCR_010910" ]
        version: [ "0.7.17" ]
      Samtools:
        specs: [ "https://identifiers.org/rrid/RRID:SCR_002105" ]
        version: [ "1.10" ]

inputs:
  reference:
    type: File
    format: edam:format_2573 # SAM
    streamable: true
    label: Alignments in SAM format
  sample:
    type: string
    label: Sample Name

stdout: $(inputs.sample).bam

outputs:
  bam:
    type: File
    format: edam:format_2572 # BAM
    label: Alignments in BAM format
    outputBinding:
      glob: "*bam"

arguments:
  - samtools
  - view
  - -@
  - $(runtime.cores)
  - -b
  - -S
  - $(inputs.reference)

s:codeRepository: https://github.com/arvados/arvados-tutorial
s:license: https://www.gnu.org/licenses/agpl-3.0.en.html

$namespaces:
 s: https://schema.org/
 edam: http://edamontology.org/
 arv: "http://arvados.org/cwl#"
 cwltool: "http://commonwl.org/cwltool#"

#$schemas:
# - https://schema.org/version/latest/schema.rdf
# - http://edamontology.org/EDAM_1.18.owl
