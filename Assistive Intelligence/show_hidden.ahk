#Requires AutoHotkey v2.0
#SingleInstance Force

#HotIf WinActive("ahk_class CabinetWClass") || WinActive("ahk_class #32770")
^h::{
    KeyWait "Control" ; 等待按键释放，避免系统当作按下了两次 Ctrl，从而触发 Listary。
    
    reg := "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    hidden := RegRead(reg, "Hidden", 2)

    if (hidden = 2) {
        RegWrite 1, "REG_DWORD", reg, "Hidden"
        RegWrite 1, "REG_DWORD", reg, "ShowSuperHidden"
    } else {
        RegWrite 2, "REG_DWORD", reg, "Hidden"
        RegWrite 0, "REG_DWORD", reg, "ShowSuperHidden"
    }

    ; 刷新 Explorer
    Send "{F5}"
}
#HotIf
