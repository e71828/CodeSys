sync_cmd:='"c:\Program Files\git\bin\sh.exe" -c "rsync -av --delete --exclude=.st* --exclude=.git* --exclude=*.ini --exclude=*.opt --exclude=*.compileinfo --exclude=*.bootinfo_guids --exclude=*.bootinfo --exclude=*.~u --exclude=*.precompilecache ~/Desktop/Codesys/ ~/OneDrive/13ANH/PycharmProjects/CodeSys/程序-e71828/"'
SetTimer sync_1drv, -1
sync_1drv()
{
    RunWait(sync_cmd,,'hide')
    SetTimer , 5*60000  ; 即此处计时器设置周期，如果此前 return，则不会循环执行.
}