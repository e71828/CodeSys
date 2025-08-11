; 使用正则表达式提zat6000v863取引号内的内容
naive(extracted){
    if InStr(extracted, "ZAT7000V8_5040D_V") {
        passwd := "ZAT7000V863"
    } else if InStr(extracted, "Z125_CR720S") {
        passwd := "ZAT8000V863"
    } else {
        passwd := SubStr(extracted, 1, InStr(extracted, "_") - 1) ; 获取下划线前的部分
    }
    if InStr(passwd, '.') {
        passwd := SubStr(passwd, 1, InStr(passwd, ".") - 1)
    }
    return StrLower(passwd)
}