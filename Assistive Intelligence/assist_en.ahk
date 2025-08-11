#Include %A_ScriptDir%\calc_passwd.ahk

#HotIf WinActive("ahk_exe CODESYS.exe")
=::Send '{U+003A}='
!=::Send '='

SetTimer AutoPasswrod, 500
AutoPasswrod()
{
    static is_waiting := false
    ; 检查 "Encryption Password" 和 "CODESYS.exe" 窗口是否存在
    if WinExist("Encryption Password ahk_exe CODESYS.exe") and !is_waiting {
        is_waiting := True
        WinWaitActive("Encryption Password")
        MouseMove 150, 29
        text := ControlGetText("Enter the password")

        ; 使用正则表达式提zat6000v863取引号内的内容
        if RegExMatch(text, "'(.*?)'", &match) {
            extracted := match[1]
            Send(naive(extracted))
            MouseMove 251, 201
        }
    }

    ; 在窗口等待手动 "Encryption Password" 点击确认
    if !WinExist("Encryption Password ahk_exe CODESYS.exe") and is_waiting {
        is_waiting := False ; 重置等待状态
    }

    ; 关闭弹出的 "Environment" 信息窗口
    if WinExist("Project Environment ahk_exe CODESYS.exe"){
        WinClose
    }
}
