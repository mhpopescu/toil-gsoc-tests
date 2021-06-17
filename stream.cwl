#!/usr/bin cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: cat
requirements:
  InlineJavascriptRequirement: {}

stdout: $(inputs.output_filename)
arguments: ["-A"]

inputs:
  input_file:
    type: File
    streamable: true
    inputBinding:
      position: 1
  output_filename:
    type: string?
    default: count.txt

outputs:
  count:
    type: stdout