#Requires AutoHotkey v2.0
#SingleInstance Force

#HotIf WinActive("Open Project ahk_class #32770 ahk_exe CODESYS.exe") || WinActive("打开工程 ahk_class #32770 ahk_exe CODESYS.exe")

; 1. 拦截 Button1 的鼠标点击
$LButton:: {
    MouseGetPos ,, , &mCtrl
    if (mCtrl == "Button1") {
        if TryTriggerDropDown()
            return
    }
    ; 正常点击逻辑
    Click "Down"
    KeyWait "LButton"
    Click "Up"
}

; 2. 拦截 Enter 按键
$Enter::
$NumpadEnter:: {
    ; 如果触发成功（Edit1不为空），则直接返回；否则发送原生 Enter
    if !TryTriggerDropDown() {
        Send "{Enter}"
    }
}

#HotIf

; --- 核心跳转逻辑函数 ---
TryTriggerDropDown() {
    try {
        ; 检查 Edit1 是否有内容
        if (ControlGetText("Edit1", "A") != "") {
            ; 获取 Button1 的位置信息
            ControlGetPos &bx, &by, &bw, &bh, "Button1", "A"
            
            ; 计算下拉三角区位置：右侧边缘往里移动少许像素
            targetX := bx + bw - bh // 4
            targetY := by + (bh // 2)
            
            ; 执行点击
            Click targetX, targetY, 2
            return true
        }
    }
    return false
}