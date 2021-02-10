import winreg, os, sys, ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def chkReg()->list:
    Return = [False, False]
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\Background\shell\Pypacker')
        Return[0] = True
    except FileNotFoundError:
        Return[0] = False
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations\.py\shell\Pypacker')
        Return[1] = True
    except FileNotFoundError:
        Return[1] = False
    return Return


def addFolder()->None:
    Path = os.path.realpath(sys.argv[0])
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\Background\shell')
    NewKey = winreg.CreateKey(key, "Pypacker")
    winreg.CloseKey(key)
    winreg.SetValue(NewKey, '', winreg.REG_SZ, "通过 Pypacker 打开")
    winreg.SetValueEx(NewKey, 'Icon', 0, winreg.REG_SZ, Path)
    newkey = winreg.CreateKey(NewKey, "command")
    winreg.CloseKey(NewKey)
    winreg.SetValue(newkey, '', winreg.REG_SZ, '\"{}\" \"%V\"'.format(Path))
    winreg.CloseKey(newkey)

    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\shell')
    NewKey = winreg.CreateKey(key, "Pypacker")
    winreg.CloseKey(key)
    winreg.SetValue(NewKey, '', winreg.REG_SZ, "通过 Pypacker 打开")
    winreg.SetValueEx(NewKey, 'Icon', 0, winreg.REG_SZ, Path)
    newkey = winreg.CreateKey(NewKey, "command")
    winreg.CloseKey(NewKey)
    winreg.SetValue(newkey, '', winreg.REG_SZ, '\"{}\" \"%1\"'.format(Path))
    winreg.CloseKey(newkey)


def delFolder():
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\Background\shell\Pypacker')
    winreg.DeleteKey(key, 'command')
    winreg.CloseKey(key)
    key = key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\Background\shell')
    winreg.DeleteKey(key, 'Pypacker')
    winreg.CloseKey(key)

    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\shell\Pypacker')
    winreg.DeleteKey(key, 'command')
    winreg.CloseKey(key)
    key = key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'Directory\shell')
    winreg.DeleteKey(key, 'Pypacker')
    winreg.CloseKey(key)


def addFile():
    Path = os.path.realpath(sys.argv[0])
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations')
    NewKey = winreg.CreateKey(key, ".py")
    winreg.CloseKey(key)
    key = winreg.CreateKey(NewKey, 'shell')
    winreg.CloseKey(NewKey)
    NewKey = winreg.CreateKey(key, 'Pypacker')
    winreg.CloseKey(key)
    winreg.SetValue(NewKey, '', winreg.REG_SZ, "用 Pypacker 打开")
    newkey = winreg.CreateKey(NewKey, "command")
    winreg.CloseKey(NewKey)
    winreg.SetValue(newkey, '', winreg.REG_SZ, '\"{}\" \"%1\"'.format(Path))
    winreg.CloseKey(newkey)


def delFile():
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations\.py\shell\Pypacker')
    winreg.DeleteKey(key, 'command')
    winreg.CloseKey(key)
    key = key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations\.py\shell')
    winreg.DeleteKey(key, 'Pypacker')
    winreg.CloseKey(key)
    key = key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations\.py')
    winreg.DeleteKey(key, 'shell')
    winreg.CloseKey(key)
    key = key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'SystemFileAssociations')
    winreg.DeleteKey(key, '.py')
    winreg.CloseKey(key)


if __name__ == '__main__':
    if is_admin():
        #delFolder()
        #addFolder()
        addFile()
        #delFile()
        input()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
