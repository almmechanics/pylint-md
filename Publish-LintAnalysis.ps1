
param (
[Parameter(Mandatory=$true)]
[string]
[ValidateScript({Test-Path $_ })]
$RootPath,

[Parameter(Mandatory=$true)]
[string]
[ValidateScript({Test-Path $_ })]
$OutputPath
)

$pythonfiles = @((gci $RootPath -filter '*.py' -Recurse).fullname)


$report = @()
$report += @('# Analysis of folder {0}' -f $RootPath)
$report += @('{0} files analysed' -f $pythonfiles.Count)
    
foreach ($file in $pythonfiles)
{
    
    Write-Verbose $file
    $pylintSummary = (pylint ($file) -f json --persistent=n --score=y) | ConvertFrom-Json

    
    $report += @('## {0}' -f ($file| Split-Path -Leaf))
    $report += @('Folder {0}' -f ($file | Split-Path))
    $report += @('### Summary')

    $report += @('|Type|Number')
    $report += @('|-|-|')
    $report += @('|error|{0}' -f (@($pylintSummary | Where-Object {$_.type -eq 'error' })).count)
    $report += @('|warning|{0}' -f (@($pylintSummary | Where-Object {$_.type -eq 'warning' })).count)
    $report += @('|refactor|{0}' -f (@($pylintSummary | Where-Object {$_.type -eq 'refactor' })).count)
    $report += @('|convention|{0}' -f (@($pylintSummary | Where-Object {$_.type -eq 'convention' })).count)
    
    $report += @('### Pylint messages')
    

    if ($pylintSummary.count -gt 0)
    {
        ($pylintSummary | Sort-Object -Property 'line') | ForEach-Object {
            $report += @('* Line: {0} is {1}[{2}] in {3}' -f $_.line, $_.message, $_.('message-id'), $_.path)
        }
    }
    else
    {
        $report += @('No issues found')
    }


    $report += @('---')
}


# export as a report
$markdownfilePath = '{0}\{1}-SummaryReport.md' -f $OutputPath, (Get-Date -Format "yyyyMMddHHmmss") 
$report | Out-File $markdownfilePath -Force