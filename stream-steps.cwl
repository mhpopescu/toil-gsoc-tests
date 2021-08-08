# Example demonstrating files with flag 'streamable'=True
class: Workflow
doc: "Stream a file"
cwlVersion: v1.2

inputs:
  input_file:
    type: File
    streamable: true

outputs:
  output:
    type: File
    streamable: true
    outputSource: cat2/output

steps:
  cat1:
    run:
      class: CommandLineTool
      baseCommand: ["cat"]
      arguments: [$(inputs.f1)]
      outputs:
        output:
          type: stdout
          streamable: true
      inputs:
        f1:
          type: File
          streamable: true
    out: [output]
    in:
      f1:
        source: input_file

  cat2:
    run:
      class: CommandLineTool
      baseCommand: ["cat"]
      arguments: [$(inputs.f2)]
      outputs:
        output:
          type: stdout
      inputs:
        f2: File
      stdout: output.txt
    out: [output]
    in:
      f2:
        source: cat1/output
