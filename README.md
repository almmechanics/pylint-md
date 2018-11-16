# pylint-md

Generate markdown reports from pylint analysis

## Powershell implementation

Example usage

    .\Publish-LintAnalysis.ps1" -RootPath C:\dev\github\geekcomputers\Python -OutputPath C:\temp

## Python implementation

Example usage

    pylint_md.py -l c:\dev\github\pylint-md -o c:\temp\t1.md

# Build Status

|Azure DevOps|Circle CI|
|-|-|
|[![Build status](https://almmechanics.visualstudio.com/python/_apis/build/status/pylint_md-CI)](https://almmechanics.visualstudio.com/python/_build/latest?definitionId=-1)|[![CircleCI](https://circleci.com/gh/almmechanics/pylint-md.svg?style=svg)](https://circleci.com/gh/almmechanics/pylint-md)|