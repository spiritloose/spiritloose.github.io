^s::
SetTitleMatchMode, 2
WinGet, FF,, Mozilla Firefox
ControlSend,, {F5}, ahk_id %FF%
Return
