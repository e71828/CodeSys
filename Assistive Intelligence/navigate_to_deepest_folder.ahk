#Requires AutoHotkey v2.0

#HotIf WinActive("ahk_class CabinetWClass")
Tab::GoDeepestExplorerPath()
#HotIf


GoDeepestExplorerPath(hwnd := 0) {
    path := ExplorerGetPath(hwnd)

    ; 非真实路径（GUID / 空）
    if (!path || RegExMatch(path, "^::\{"))
        return

    deepest := GoDeepestFolder(path)

    if (deepest && deepest != path)
        ExplorerNavigate(deepest)
}


ExplorerNavigate(path) {
    for window in ComObject("Shell.Application").Windows {
        try {
            if (window.hwnd = WinActive("ahk_class CabinetWClass")) {
                ;window.Navigate(path)
                window.Navigate2(path, 0x800)
                return
            }
        }
    }
}


ExplorerGetPath(hwnd := 0) {
    static winTitle := "ahk_class CabinetWClass ahk_exe explorer.exe"

    if (!hwnd) {
        hwnd := WinActive(winTitle)
        if (!hwnd)
            return ""
    }

    for window in ComObject("Shell.Application").Windows {
        try {
            if !window || !window.Document
                continue

            if (window && window.hwnd = hwnd) {
                title := window.Document.Folder.Title
                path  := window.Document.Folder.Self.Path
                
                ; Win11: multiple tabs
                if (InStr(WinGetTitle("A"), title)) {
                    result .= title "  =>  " path "`n"
                    return window.Document.Folder.Self.Path
                }
            }
        }
    }
    return ""
}


GoDeepestFolder(path) {
    loop {
        subDirs := []
        hasFile := false

        Loop Files path "\*", "FD" {
            if (A_LoopFileAttrib ~= "D")
                subDirs.Push(A_LoopFileFullPath)
            else {
                hasFile := true
                break
            }
        }

        ; 有文件 或 子目录不唯一 → 停止
        if (hasFile || subDirs.Length != 1)
            break

        path := subDirs[1]
    }
    return path
}
