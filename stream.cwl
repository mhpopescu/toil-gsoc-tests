#!/usr/bin cwl-runner

cwlVersion: v1.2
class: CommandLineTool
baseCommand: cat

stdout: output.txt

inputs:
  input_file:
    type: File
    streamable: true
    inputBinding:
      position: 1

outputs:
  out:
    type: stdout
    streamable: true