# Example command line program wrapper for the Unix tool "sort"
# demonstrating command line flags.
class: CommandLineTool
doc: "Download a file from different cloud environments"
cwlVersion: v1.2


inputs:
  - id: input_file
    type: File
    inputBinding:
      position: 1
    streamable: true

outputs:
  output:
    type: File
    outputBinding:
      glob: output.txt

baseCommand: ["test","-p"]
stdout: output.txt
