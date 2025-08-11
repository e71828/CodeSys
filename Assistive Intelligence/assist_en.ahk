#Include %A_ScriptDir%\calc_passwd.ahk

#HotIf WinActive("ahk_exe CODESYS.exe")
=::Send '{U+003A}='
!=::Send '='
PgUp::
{
    global seq
    if seq > 1 and seq < steps.Length + 1 {
        seq -= 1
        assist()
    }

}
PgDn::
{
    global seq
    if seq >= 0 and seq < steps.Length {
        seq += 1
        assist()
    }
}
Pause::
{
    global seq
    static presses := 0
    if presses > 0 ; SetTimer 已经启动, 所以我们记录键击.
    {
        presses += 1
        return
    }
    ; 否则, 这是新开始系列中的首次按下. 把次数设为 1 并启动计时器
    presses := 1
    SetTimer AfterMS, -400 ; 毫秒内等待更多的键击

    AfterMS()  ; 这是一个嵌套函数.
    {
        if presses = 1 ; 此键按下了一次.
        {
            ToolTip
        }
        else if presses = 2 ; 此键按下了两次.
        {
            seq := 1
            assist()
        }
        ; 不论触发了上面的哪个动作, 都对 count 进行重置
        ; 为下一个系列的按键做准备:
        presses := 0
    }
}
`::
{
    global details, seq
    static i := 1
    static seq_last := seq
    if seq = 0 {
        return
    }
    i := seq_last == seq ? i : 1
    seq_last := seq
    ket := details.Get(steps[seq], 0)
    if IsObject(ket) {
        search(ket.Get(i))
        i := i != ket.Length ? i + 1 : 1
    } else if IsInteger(ket) {
        ;
    } else {
        search(ket)
    }
}
search(eye)
{
    project_name := WinGetTitle("ahk_exe CODESYS.exe",,"Find"||"Replace")
    if project_name == "CODESYS " {
        ToolTip "No open projects!"
        return
    }
    if WinExist(project_name) {
        Send "^f"
        ToolTip
        if WinWaitActive("Find"||"Replace",,500) {
            ControlSetText(eye, "Edit1")
            KeyWait "Control"
            Send 'd{BS}'
            Sleep 100 ; Wait a bit for sending chars one by one
            WinGetClientPos &X, &Y, &W, &H
            Click W-100, 30
            Sleep 200 ; Wait a bit for Ctrl+F to be processed by CodeSys
            if WinExist("CODESYS",,project_name) {
                Sleep 400
                WinClose ; The specifid text was not found.
            }
            if WinWaitActive("Find"||"Replace") { ; Active the Find window
                MouseMove W-50, H-30, 1
            }
            WinActivate(project_name)
;            A_Clipboard := "
;            (Join`s
;                This text is placed on the clipboard,
;                and will be pasted below by sending Ctrl+V.
;            )"
        }
    }
}
details := Map(
    "吊载 retain 变量：可能重复定义",
    'rope_length_theory_standardization_sub:REAL',
    "吊载 zero_check",
    'zero_check',
    "吊载 real2uint 不可一步完成",
    'REAL_TO_UINT',
    "吊载平移输入变量报文解析",
    ['array_Rx_limiter_292[4].4', 'array_Rx_limiter_292[4].3',],
    "吊载平移输出变量报文字节封包",
    ['array_Tx_18B[8]', 'array_Tx_38C[2]', 'array_Tx_29C[4]',],
    "吊载平移输入变量来自新增报文",
    ['CAN1_RECEIVE_292',],
    "吊载平移输出变量报文新增发送，注意 ton500ms.Q 与 DLC ",

    ['CAN1_TRANSMIT_29C', 'CAN1_TRANSMIT_18B', 'CAN1_TRANSMIT_38C',],
    "防摇摆输入变量报文解析",
    ['array_Rx_limiter_393[7].7', 'array_Rx_limiter_393[8]',],
    "防摇摆输出变量报文字节封包",
    ['array_Tx_3C0[1]', 'array_Tx_4A3[2]', 'array_Tx_4A3[4]', 'array_Tx_4A3[5]',],
    "防摇摆输入变量来自新增报文",
    ['CAN1_RECEIVE_393',],
    "防摇摆输出变量报文新增发送，注意 ton500ms.Q 与 DLC ",
    ['CAN1_TRANSMIT_3C0', 'CAN1_TRANSMIT_4A3',],
)
seq := 0
steps :=
[
    "Welcome!",
    "吊载主体复制：全局变量可能重复定义",
    "吊载 retain 变量：可能重复定义",
    "吊载 zero_check",
    "吊载 real2uint 不可一步完成",
    "吊载调用复制，接口输入常量修改",
    "吊载平移 derrick_sub 修改，两或3个 network",
    "吊载平移 winch_i_sub 修改，3个 network",
    "吊载平移 pump_sub 修改，1个 network",
;    "吊载平移输入检查未定义", ; 一般都在 GVL 中，很可能重复定义
    "吊载平移输入检查未写入", ; 展开多个
    "吊载平移检查重复写入",

    "防摇摆主体复制：全局变量可能重复定义",
    "防摇摆内部常量修改：臂架质量与电流值-回转速度关系",
    "防摇摆调用复制，接口输入常量",
    "防摇摆 slew_sub 修改，2个 network，左右电流互锁，不关心塔臂",
    "防摇摆调用输入检查未写入",
    "防摇摆检查重复写入",

    "吊载平移输入变量报文解析", ; 展开多个
    "吊载平移输出变量报文字节封包", ; 展开多个
    "吊载平移输入变量来自新增报文", ; 展开多个
    "吊载平移输出变量报文新增发送，注意 ton500ms.Q 与 DLC ", ; 展开多个

    "防摇摆输入变量报文解析", ; 展开多个
    "防摇摆输出变量报文字节封包", ; 展开多个
    "防摇摆输入变量来自新增报文", ; 展开多个
    "防摇摆输出变量报文新增发送，注意 ton500ms.Q 与 DLC ", ; 展开多个
]


assist(){
    global seq
    ToolTip steps[seq]
}

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
