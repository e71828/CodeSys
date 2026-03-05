/*
    AutoHotkey Proxy Manager (V2 Version)
    Author: Yasin Asasi (V2 Conversion by Copilot)
    GitHub: https://github.com/e71828/AutoHotkey-Proxy-Manager
    Version: 2.x
    Description: A Windows utility to manage proxy settings via a GUI. Loads proxies from proxies.txt,
                 allows selection and enabling/disabling of proxies, and checks proxy status.
    Usage: Run the script, press Ctrl+Alt+M to open the GUI, select a proxy, and use buttons to manage proxies.
    Notes:
    - Requires AutoHotkey v2.0+.
    - Run as administrator for registry modifications (if you encounter permission errors when setting proxies).
    - Proxies.txt should list proxies in server:port format (e.g., 127.0.0.1:8080), one per line.
    - Automatically creates proxies.txt if missing, with commented instructions.
    - Lines in proxies.txt starting with ; are ignored as comments.
    License: MIT
*/

#Requires AutoHotkey v2.0
#SingleInstance Force
SetWorkingDir A_ScriptDir

global ProxyArray := []
global SelectedProxy := ""

; GUI Creation
ProxyGui := Gui("+AlwaysOnTop", "Proxy Manager")
ProxyList := ProxyGui.Add("ListBox", "x10 y10 w195 h120 vProxyList")
btnSet := ProxyGui.Add("Button", "x210 y10 w100 h25", "Set Proxy")
btnDisable := ProxyGui.Add("Button", "x210 y40 w100 h25", "Disable Proxy")
btnCheck := ProxyGui.Add("Button", "x210 y70 w100 h25", "Check Proxy")
btnOpenFile := ProxyGui.Add("Button", "x210 y100 w100 h25", "Open Proxies File")
ProxyStatus := ProxyGui.Add("Text", "x10 y135 w300 h50 vProxyStatus", "Proxy Status: Not checked")

btnSet.OnEvent("Click", SetProxy)
btnDisable.OnEvent("Click", DisableProxy)
btnCheck.OnEvent("Click", CheckProxy)
btnOpenFile.OnEvent("Click", OpenProxiesFile)
ProxyList.OnEvent("Change", SelectProxy)
ProxyGui.OnEvent("Close", (*) => ProxyGui.Hide())

LoadProxies() {
    global ProxyArray, ProxyList, ProxyStatus, SelectedProxy
    ProxyArray := []
    if !FileExist("proxies.txt") {
        FileAppend(
            "; Add proxies in the format server:port, one per line`n"
            "; Example:`n"
            "; 127.0.0.1:10808`n"
            "; 192.168.42.129:8080`n", "proxies.txt")
        ProxyStatus.Text := "Created proxies.txt. Add proxies to the file."
    }
    try
        ProxyFile := FileRead("proxies.txt")
    catch {
        MsgBox("Could not read proxies.txt")
        ExitApp()
    }
    for line in StrSplit(ProxyFile, "`n") {
        line := Trim(line)
        if (line != "" && SubStr(line, 1, 1) != ";") {
            ProxyArray.Push(line)
        }
    }
    ProxyList.Delete()
    if ProxyArray.Length
        ProxyList.Add(ProxyArray)
    if (ProxyArray.Length == 0)
        ProxyStatus.Text := "No valid proxies found in proxies.txt"
    else {
        ProxyStatus.Text := "Proxy Status: Loaded " ProxyArray.Length " proxies!"
        ProxyList.Choose(1)
        SelectedProxy := ProxyArray[1] ; Auto Select the first. 
    }

}

SelectProxy(*) {
    global SelectedProxy, ProxyList
    SelectedProxy := ProxyList.Text
}

SetProxy(*) {
    global SelectedProxy, ProxyStatus
    if !SelectedProxy {
        ProxyStatus.Text := "Please select a proxy first"
        return
    }
    if RegExMatch(SelectedProxy, "(.+):(\d+)", &m) {
        ProxyServer := m[1]
        ProxyPort := m[2]
        RegWrite(1, "REG_DWORD", "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable")
        RegWrite(ProxyServer ":" ProxyPort, "REG_SZ", "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyServer")
        DllCall("wininet\InternetSetOptionW", "ptr", 0, "uint", 39, "ptr", 0, "uint", 0)
        DllCall("wininet\InternetSetOptionW", "ptr", 0, "uint", 37, "ptr", 0, "uint", 0)
        ProxyStatus.Text := "Proxy set to: " SelectedProxy
    } else {
        ProxyStatus.Text := "Format error"
    }
}

DisableProxy(*) {
    global ProxyStatus
    RegWrite(0, "REG_DWORD", "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable")
    DllCall("wininet\InternetSetOptionW", "ptr", 0, "uint", 39, "ptr", 0, "uint", 0)
    DllCall("wininet\InternetSetOptionW", "ptr", 0, "uint", 37, "ptr", 0, "uint", 0)
    ProxyStatus.Text := "Proxy disabled"
}

CheckProxy(*) {
    global ProxyStatus
    ProxyEnable := RegRead("HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable")
    if (ProxyEnable = 1) {
        ProxyServer := RegRead("HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyServer")
        ProxyStatus.Text := "Proxy enabled: " ProxyServer
    } else {
        ProxyStatus.Text := "No proxy enabled"
    }
}

OpenProxiesFile(*) {
    Run(A_ScriptDir "\proxies.txt")
}

; Hotkey to open GUI and load proxies (Ctrl + Alt + M)
#HotIf A_ComputerName != "vitasoy"
^!m::{
    LoadProxies()
    ProxyGui.Show("w320 h160")
}
#Hotif