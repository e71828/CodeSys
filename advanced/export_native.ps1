# 定义常量变量
$codesysExePath = "C:\Program Files\CODESYS 3.5.16.30\CODESYS\Common\CODESYS.exe"
$codesysProfile = "CODESYS V3.5 SP16 Patch 3"
$scriptPath = "$PSScriptRoot\export_native.py"
$python3script_Path = "$PSScriptRoot\seek3.py"
$project_path = Read-Host "Enter the directory containing .project files"
# 去掉输入字符串两侧的引号
$project_path = $project_path.Trim('"')
# 如果输入的是文件路径，则获取其上级目录
if ($project_path)
{
    if (Test-Path $project_path)
    {
        if (-not (Test-Path $project_path -PathType Container))
        {
            # 如果输入的是文件，获取上级目录
            $project_path = Split-Path $project_path
        }
        if (-not (Test-Path $scriptPath))
        {
            Write-Host "The file '$scriptPath' not found ."
            Exit
        }
    }
    else
    {
        Write-Host "The path '$project_path' is not valid. Exiting script."
        Exit
    }
}
else
{
    Exit
}
$extract_to_path = Read-Host "Enter the directory to save .export files"
# 去掉输入字符串两侧的引号
$extract_to_path = $extract_to_path.Trim('"')
# 如果输入的是文件路径，则获取其上级目录
if ($extract_to_path)
{
    if (Test-Path $extract_to_path)
    {
        if (-not (Test-Path $extract_to_path -PathType Container))
        {
            # 如果输入的是文件，获取上级目录
            $extract_to_path = Split-Path $extract_to_path
        }
    }
    else
    {
        Write-Host "The path '$extract_to_path' is not valid. Exiting script."
        Exit
    }
}
else
{
    $extract_to_path = $project_path
}

# 获取当前目录下的所有 .project 文件及其子目录中的 .project 文件
$projectFiles = Get-ChildItem -Recurse -Filter "*.project" -Path $project_path | Where-Object { $_.Name -notmatch "E107" }
Write-Output "$( $projectFiles.Count ) projects found. Please confirm ..."

if ($projectFiles.Count -gt 0)
{
    # 构造要执行的 CMD 命令
    $arguments = "--profile='$codesysProfile' --noUI --runscript='$scriptPath' --scriptargs:'$project_path $extract_to_path'"

    # 启动 CODESYS 进程
    Start-Process -NoNewWindow -Wait -FilePath $codesysExePath -ArgumentList $arguments

    # 查找 python.exe 的路径
    $python = Get-Command "python.exe" -ErrorAction SilentlyContinue
    if ($python)
    {
        # 获取 Python 版本
        $version = & $python.Path --version 2>&1
        # 如果找到 python3，使用它运行脚本
        if ($version -like "Python 3*")
        {
            Start-Process -NoNewWindow -Wait -FilePath $python.Path -ArgumentList "$python3script_Path", "$extract_to_path"
        }
        else
        {
            Write-Host "Python3 needed."
        }
    }
    else
    {
        Write-Host "Python3 needed."
    }
}
Read-Host -Prompt "Press Enter to exit"