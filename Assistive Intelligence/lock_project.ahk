#Requires AutoHotkey v2.0

period := -1
SetTimer lock_codesys_projects, period
lock_codesys_projects()
{
    if WinExist("ahk_exe CODESYS.exe") and (WinGetTitle("ahk_exe CODESYS.exe",,"Find") != "CODESYS "){
        MsgBox "One project is being editing? Please close the file and try angain!"
        SetTimer , 0  ; 即此处计时器关闭自己.
        return
    }
    if (period < -1){
        currentDateTime := FormatTime(A_Now, 'MM/dd/yyyy HH:mm')
        FileAppend " " currentDateTime " :~ 开始设置文件只读;`n", A_ScriptDir "\ReadOnly.log"
    }
    
    
    SelectedFolder := A_Desktop "\Codesys"
    if !(FileExist(SelectedFolder) ~= "[D]"){
        SelectedFolder := DirSelect("::{60632754-C523-4B62-B45C-4172DA012619}", 0)  ; User Accounts.
        if SelectedFolder = ""
            return
    }
    count := 0
    Loop Files, SelectedFolder "\*.project", "R"
    {
        LongPath := A_LoopFilePath
        if (InStr(A_LoopFileDir, "\old")
            || InStr(A_LoopFileDir, "\.stversions")
            || InStr(A_LoopFileDir, "\.git"))
            continue
        if A_LoopFileAttrib ~= "[HRS]"  ; 跳过任何具有 H(隐藏), R(只读) 或 S(系统). 请参阅 ~= 运算符.
            continue  ; 跳过这个文件并继续下一个文件.
        if !InStr(A_LoopFileAttrib, "R"){
            FileSetAttrib "+R", A_LoopFilePath, "F"
            FileAppend "Set " LongPath " as Read-Only.`n", A_ScriptDir "\ReadOnly.log"
            count := count + 1
        }
    }
    if (period < -1){
        currentDateTime := FormatTime(A_Now, 'MM/dd/yyyy HH:mm')
        FileAppend " " currentDateTime " :~ 本次循环执行共有 " count " 个文件被改变了属性。`n", A_ScriptDir "\ReadOnly.log"
    }
}