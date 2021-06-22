#!/usr/bin cwl-runner

cwlVersion: v1.2
class: CommandLineTool
baseCommand: cat

stdout: $(inputs.output_filename)

inputs:
  input_file:
    type: File
    streamable: true
    inputBinding:
      position: 1
  output_filename:
    type: string?
    default: output.txt

outputs:
  out:
    type: stdout