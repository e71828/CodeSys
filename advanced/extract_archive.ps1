# 定义常量变量
$codesysExePath = "C:\Program Files\CODESYS 3.5.16.30\CODESYS\Common\CODESYS.exe"
$codesysProfile = "CODESYS V3.5 SP16 Patch 3"
$scriptPath = "C:\Users\13ANH\PycharmProjects\CodeSys\advanced\extract_archive.py"
$currentPath = "$PSScriptRoot"
$project_path = Read-Host "Enter the directory containing .projectarchive files"
# 去掉输入字符串两侧的引号
$project_path = $project_path.Trim('"')
# 如果输入的是文件路径，则获取其上级目录
if ( $project_path ) {
    if (Test-Path $project_path) {
        if (-not (Test-Path $project_path -PathType Container)) {
            # 如果输入的是文件，获取上级目录
            $project_path = Split-Path $project_path
        }
        if (-not (Test-Path $scriptPath)) {
            Write-Host "The file '$scriptPath' not found ."
            Exit
        }
    } else {
        Write-Host "The path '$project_path' is not valid. Exiting script."
        Exit
    }
} else {
    Exit
}
$extract_to_path = Read-Host "Enter the directory to extract .projectarchive files"
# 去掉输入字符串两侧的引号
$extract_to_path = $extract_to_path.Trim('"')
# 如果输入的是文件路径，则获取其上级目录
if ( $extract_to_path ) {
    if (Test-Path $extract_to_path) {
        if (-not (Test-Path $extract_to_path -PathType Container)) {
            # 如果输入的是文件，获取上级目录
            $extract_to_path = Split-Path $extract_to_path
        }
    } else {
        Write-Host "The path '$extract_to_path' is not valid. Exiting script."
        Exit
    }
} else {
    $extract_to_path = $project_path
}

# 获取当前目录下的所有 .project 文件及其子目录中的 .project 文件
$projectFiles = Get-ChildItem -Recurse -Filter "*.projectarchive" -Path $project_path | Where-Object { $_.Name -notmatch "E107" }
Write-Output "$($projectFiles.Count) projects found. Please confirm ..."

if ($projectFiles.Count -gt 0){
    # 构造要执行的 CMD 命令
    $arguments = "--profile='$codesysProfile' --noUI --runscript='$scriptPath' --scriptargs:'$project_path $extract_to_path'"

    # 启动 CODESYS 进程
    Start-Process -NoNewWindow -Wait -FilePath $codesysExePath -ArgumentList $arguments
}
Read-Host -Prompt "Press Enter to exit"