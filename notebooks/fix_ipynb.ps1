$path = 'notebooks\analise_resultados.ipynb'
$lines = Get-Content $path
$inSource = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^[ \t]*"source"\s*:\s*\[$') {
        $inSource = $true
        continue
    }
    if ($inSource -and $line.Trim() -match '^\](,)?$') {
        $inSource = $false
        continue
    }
    if ($inSource -and $line.TrimStart().StartsWith('"')) {
        $trimmed = $line.TrimEnd()
        if ($trimmed.EndsWith('",') -or $trimmed.EndsWith('"')) {
            $j = $i + 1
            while ($j -lt $lines.Count -and $lines[$j].Trim() -eq '') { $j++ }
            if ($j -lt $lines.Count -and $lines[$j].Trim() -notmatch '^\](,)?$' -and -not $trimmed.EndsWith('",')) {
                $lines[$i] = $line + ','
            }
        }
    }
}
$lines | Set-Content $path -Encoding UTF8
