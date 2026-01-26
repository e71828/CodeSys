#Requires AutoHotkey v2.0
#SingleInstance Force

lastLButtonUpTime := 0
#HotIf WinActive("Open Project ahk_class #32770 ahk_exe CODESYS.exe") || WinActive("打开工程 ahk_class #32770 ahk_exe CODESYS.exe")

; 1. 拦截 Button1 的鼠标点击
$LButton:: {
    global lastLButtonUpTime
    MouseGetPos &mX, &mY, , &mCtrl
    if (mCtrl == "Button1") {
        if TryTriggerDropDown(false)
            return
    }
    if (InStr(mCtrl, "DirectUIHWND")) {
        if (A_TickCount - lastLButtonUpTime < 400) {
            ; 获取鼠标当前位置的颜色
            ; 默认返回的是 BGR 格式，例如 0x191919
            currColor := PixelGetColor(mX, mY)
            ; 排除背景色 (191919 和 FFFFFF)
            ; 注意：PixelGetColor 返回的是十六进制字符串，如 "0x191919"
            if (currColor != "0x191919" && currColor != "0xFFFFFF") {
                TryTriggerDropDown(false)
                return
            }
        }
    }
    ; 正常点击逻辑
    Click "Down"
    KeyWait "LButton"
    Click "Up"
    lastLButtonUpTime := A_TickCount ; 记录这一次弹起的精确时间
}

; 2. 拦截 Enter 按键
$Enter::
$NumpadEnter:: {
    TryTriggerDropDown(true)
}

#HotIf

; --- 核心跳转逻辑函数 ---
TryTriggerDropDown(keyboard := false) {
    try {
        MouseGetPos &mX, &mY
        ; 检查 Edit1 是否有内容
        if (ControlGetText("Edit1", "A") != "") {
            ; 获取 Button1 的位置信息
            ControlGetPos &bx, &by, &bw, &bh, "Button1", "A"

            ; 计算下拉三角区位置：右侧边缘往里移动少许像素
            targetX := bx + bw - bh // 4
            targetY := by + (bh // 2)

            ; 执行点击
            Click targetX, targetY, 1

            ; win10 等待弹出下拉菜单窗口
            if WinWait("ahk_class #32768 ahk_exe CODESYS.exe", , 0.25) {
                CoordMode "Mouse", "Screen"
                WinGetPos &nx, &ny, &nw, &nh, "ahk_class #32768"
                ; 点击菜单第二项（中心靠下位置）
                Click (nx + nw // 2), (ny + nh *4 // 5), 1
                CoordMode "Mouse", "Client"
                ; 给一点点缓冲时间让菜单处理指令
                Sleep 200
                ; 检查工程打开选择窗口是否还在
                if !WinExist("ahk_class #32770 ahk_exe CODESYS.exe") {
                    return 1
                } else if WinExist("Open Project ahk_class #32770 ahk_exe CODESYS.exe") || WinExist("打开工程 ahk_class #32770 ahk_exe CODESYS.exe") {
                    MouseMove mX, mY
                    return -1
                } else 
                    return -1
            }
        } else {
            if !keyboard
                Click 2
            else
                Send "{Enter}"
        }
        return 0
    }
}