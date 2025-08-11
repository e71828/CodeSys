#Include %A_ScriptDir%\calc_passwd.ahk

#HotIf WinActive("ahk_exe CODESYS.exe")
=::Send '{U+003A}='
!=::Send '='

SetTimer AutoPasswrod, 500
AutoPasswrod()
{
    static is_waiting := false
    ; 检查 "Encryption Password" 和 "CODESYS.exe" 窗口是否存在
    if WinExist("密码 ahk_exe CODESYS.exe") and !is_waiting {
        is_waiting := True
        WinWaitActive("密码")
        MouseMove 150, 29
        text := ControlGetText("输入") ; 输入"ZAT4000VS863-1_5040_V01_d"的密码:

        ; 使用正则表达式提取双引号内的内容
        if RegExMatch(text, '"(.*?)"', &match) {
            extracted := match[1]
            Send(naive(extracted))
            MouseMove 251, 201
        }
    }

    ; 在窗口等待手动 "Encryption Password" 点击确认
    if !WinExist("密码 ahk_exe CODESYS.exe") and is_waiting {
        is_waiting := False ; 重置等待状态
    }

    ; 关闭弹出的 "Environment" 信息窗口
    if WinExist("工程版本信息 ahk_exe CODESYS.exe"){
        WinClose
    }
}
