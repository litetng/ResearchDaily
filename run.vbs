Set WshShell = CreateObject("WScript.Shell")
' 0 表示隐藏窗口运行 (Hidden window)
WshShell.Run chr(34) & "start.bat" & Chr(34), 0
Set WshShell = Nothing
