# -*- coding: utf-8 -*-
# @Date    : 2021-02-06 23:34:01
# @Author  : Megix Wiley (yjmthu@gmail.com)
# @Link    : https://github.com/Wiley2046
# @Version : 3.5

from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox,QLabel, QActionGroup,
QLineEdit, QInputDialog, QColorDialog, qApp)
from PyQt5.QtCore import QCoreApplication, QDir, pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
import sys, os, json, webbrowser, ctypes
import RegSet

from ui_mainwindow import Ui_MainWindow
from cmdThread import QmyTread


class Qmywindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pyPath = ''
        self.pyName = ''
        self.icoPath = ''
        self.icoName = ''
        self.specName = ''
        self.MoveTo = ''
        self.PassWord = 'Pypacker'
        self.SettingName = 'Settings.json'
        self.ColorW = [240, 240, 240, 255]
        self.ColorT = [0, 0, 0, 255]
        self.argv = sys.argv
        self.stayPath = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.linePath.setReadOnly(True)
        self.ui.pBtnOpen.setEnabled(False)
        self.ui.linePath.setFocusPolicy(Qt.NoFocus)
        self.ui.pBtnOK.setShortcut(Qt.Key_Return)

        self.BarLable = QLabel('注意：在使用本程序之前，请确认已经配置好Python的环境变量'
        '以及安装pyinstaller。')
        self.ui.statusBar.addWidget(self.BarLable, stretch=0)

        actGroup = QActionGroup(self)
        actGroup.addAction(self.ui.actDall)
        actGroup.addAction(self.ui.actDbootloader)
        actGroup.addAction(self.ui.actDimports)
        actGroup.addAction(self.ui.actDnoarchive)
        actGroup.setExclusive(True)
        try:
            self.LoadSettings()
        except KeyError:
            pass

        if not os.path.exists(self.stayPath+'\\Temporary.json'):
            if self.ui.actRigthMenu.isChecked():
                if len(self.argv) == 2:
                    Path = self.argv[1]
                    if os.path.isfile(Path):
                        if os.path.splitext(Path)[1].lower() == '.py':
                            self.pyName = Path.split('\\')[-1]
                            self.ui.linePath.setText(Path)
                        else:
                            self.pyName = ''
                            self.ui.linePath.clear()
                        self.pyPath = os.path.dirname(Path)
                    else:
                        self.pyPath = Path
                        self.pyName = ''
                        self.ui.linePath.clear()
                else:
                    self.pyPath = os.getcwd()
                    self.pyName = ''
                    self.ui.linePath.clear()
                self.ui.pBtnOpen.setEnabled(True)
        
        if self.pyPath != "":
            if os.path.exists(self.pyPath):
                self.ui.actCleanPyo.setEnabled(True)
                self.ui.actCleanSpec.setEnabled(True)

        self.Thread = QmyTread()
        self.Thread.finish.connect(self.do_Finish)

    
    @pyqtSlot(bool)
    def on_pBtnChScript_clicked(self):
        #Path = os.path.dirname(os.path.abspath(__file__))
        #Path = os.path.dirname(os.path.realpath(sys.argv[0]))
        filter = "PY文件(*.py)"
        caption = "选择Python主程序文件"
        if self.pyPath == "":
            Path = os.getcwd()
            Path_1 = QFileDialog.getOpenFileName(self, caption=caption, directory=Path,
            filter=filter,options=QFileDialog.ShowDirsOnly)
        else:
            Path_1 = QFileDialog.getOpenFileName(self, caption=caption, directory=self.pyPath,
            filter=filter, options=QFileDialog.ShowDirsOnly)
        if Path_1[0] != "":
            self.pyPath = Path_1[0].replace('/', '\\')
            self.ui.linePath.setText(self.pyPath)
            self.pyName = self.pyPath.split('\\')[-1]
            self.pyPath = os.path.dirname(self.pyPath)
            if self.specName == '':
                self.setSpecLable()
            self.ui.pBtnOpen.setEnabled(True)
            self.ui.actCleanSpec.setEnabled(True)

    @pyqtSlot(bool)
    def on_pBtnChico_clicked(self):
        filter = "ico文件(*.ico)"
        caption = "选择图标文件"
        if self.pyPath != '':
            self.icoPath = QFileDialog.getOpenFileName(self, caption=caption, directory=self.pyPath,
            filter=filter, options=QFileDialog.ShowDirsOnly)
        else:
            #Path = os.path.dirname(os.path.abspath(__file__))
            self.icoPath = QFileDialog.getOpenFileName(self, caption=caption, directory=self.stayPath,
            filter=filter, options=QFileDialog.ShowDirsOnly)
        if self.icoPath[0] != '':
            self.icoPath = self.icoPath[0].replace('/', '\\')
            self.ui.Labico.setText(self.icoPath)
            self.icoName = self.icoPath.split('\\')[-1]
            self.icoPath = os.path.dirname(self.icoPath)
        else:
            self.ui.chkSetIcon.setChecked(False)
            self.ui.pBtnChico.setEnabled(False)

    
    @pyqtSlot(bool)
    def on_chkSetIcon_clicked(self, bool):
        self.ui.pBtnChico.setEnabled(bool)
        if not bool:
            self.ui.Labico.setText('未设置')
    
    @pyqtSlot(bool)
    def on_pBtnOpen_clicked(self):
        Path = self.pyPath
        if os.path.exists(Path):
            os.system('start explorer {}'.format(Path))

    @pyqtSlot(bool)
    def on_pBtnOK_clicked(self, bool):
        if self.pyName != '' and self.pyPath != '':
            self.ui.pBtnCancel.setEnabled(False)
            self.ui.pBtnOK.setEnabled(False)
            Cmd = 'cd ' + self.pyPath + ' && pyinstaller'
            content = 'pyinstaller'
            if self.ui.rBtnDebug.isChecked():
                Cmd += ' -d ' + self.MakeOutAction()
                content += ' -d ' + self.MakeOutAction()
            if self.ui.rBtnOneFile.isChecked():
                Cmd += ' -F'
                content += ' -F'
            if self.ui.chkConsole.isChecked():
                Cmd += ' -w'
                content += ' -w'
            if self.ui.rBtnNameSet.isChecked():
                Cmd += ' -n ' + self.specName[:-5]
                content += ' -n ' + self.specName[:-5]
            if self.ui.chkSetIcon.isChecked() and self.icoName != '':
                Cmd += ' -i ' + self.icoPath + '\\' + self.icoName
                if self.pyPath == self.icoPath:
                    content += ' -i ' + self.icoName
                else:
                    content += ' -i ' + self.icoPath + '\\' + self.icoName
            if self.ui.actSecret.isChecked() and self.PassWord != '':
                Cmd += ' --key ' + self.PassWord
                content += ' --key ' + self.PassWord
            Cmd += ' ' + self.pyName
            content += ' --clean ' + self.pyName

            self.BarLable.setText('正在执行命令……')
            if self.ui.chkBat.isChecked():
                file = open(self.pyPath+'/'+'PyToExe.bat', 'w', encoding='gbk')
                file.write(content)
                file.close()

            if self.ui.chkSaveSet.isChecked():
                self.DumpSettings()
            if self.ui.actPerfect.isChecked():
                self.Thread.MoveTo = self.MoveTo
                if self.ui.rBtnOneFile.isChecked():
                    self.Thread.FileMode = 'File'
                else:
                    self.Thread.FileMode = 'Folder'
            
            self.Thread.MainPath = self.pyPath
            self.Thread.MainName = self.specName[:-5]
            self.Thread.command = Cmd
            self.Thread.Mode = 'build'
            self.Thread.start()
        else:
            msg_box = QMessageBox.warning(self, "警告", "你需要选择一个Python脚本！")
    
    @pyqtSlot(bool)
    def do_Finish(self, sucess):
        if sucess:
            if self.Thread.Mode == 'build':
                if self.ui.actExit.isChecked():
                    if self.ui.actExitSave.isChecked():
                        self.DumpSettings()
                    self.close()
                else:
                    self.BarLable.setText('编译完成！')
                    if self.ui.actFinishDianlog.isChecked():
                        QMessageBox.information(self, "提示", '编译完成！')
                    self.ui.pBtnCancel.setEnabled(True)
                    self.ui.pBtnOK.setEnabled(True)
            elif self.Thread.Mode == 'install':
                self.BarLable.setText("安装完成！")
                QMessageBox.information(self, "提示", '安装完成！')
            elif self.Thread.Mode == 'uninstall':
                self.BarLable.setText("卸载完成")
                QMessageBox.information(self, "提示", '卸载完成！')
        else:
            self.ui.pBtnCancel.setEnabled(True)
            self.ui.pBtnOK.setEnabled(True)
            self.BarLable.setText("编译出错了！！！")
            QMessageBox.critical(self, "出错", "出现严重错误，请检查相关文件以及编译设置。")
    
    @pyqtSlot(bool)
    def on_actInstaller_triggered(self):
        self.BarLable.setText('正在安装pyinstaller……')
        self.Thread.Mode = 'install'
        self.Thread.command = 'pip install pyinstaller'
        self.Thread.start()
    
    @pyqtSlot(bool)
    def on_rBtnNameSet_clicked(self):
        dlgTitle = "输入文字对话框"
        txtLabel = "请输入spec文件名"
        if self.specName == '':
            defaultInput = self.pyName[:-3]
        else:
            defaultInput = self.specName[:-5]
        echoMode = QLineEdit.Normal
        text, OK = QInputDialog.getText(self, dlgTitle, txtLabel, echoMode, defaultInput)
        if OK:
            if text != '':
                if text.split('.')[-1] == 'spec':
                    self.specName = text.replace(' ', '_')
                else:
                    self.specName = text.replace(" ", '_') + '.spec'
                self.ui.LabSpecName.setText(self.specName+' )')
            else:
                QMessageBox.warning(self, '警告', '没有输入任何文件名！')
                self.ui.rBtnNameDefault.setChecked(True)
                self.setSpecLable()
        else:
            if self.specName != '':
                self.ui.LabSpecName.setText(self.specName+' )')
            else:
                self.ui.rBtnNameDefault.setChecked(True)
                self.setSpecLable()
    
    @pyqtSlot(bool)
    def on_rBtnNameDefault_clicked(self):
        self.specName = ''
        self.setSpecLable()
    
    @pyqtSlot(bool)
    def on_actFileLoad_triggered(self):
        Path = self.stayPath + '\\Settings.json'
        if os.path.exists(Path):
            try:
                self.LoadSettings(True)
            except (json.decoder.JSONDecodeError, KeyError):
                QMessageBox.critical(self, '错误', 'json文件版本过低或内容错误！')
        else:
            QMessageBox.information(self, '提示', '缺失json文件，可通过保存配置或重启软件解决。')

    @pyqtSlot(bool)
    def on_actFileDump_triggered(self):
        self.DumpSettings()
        QMessageBox.information(self, "提示", "设置已保存！")

    @pyqtSlot(bool)
    def on_actCleanSpec_triggered(self):
        '''清除spec文件'''
        n = 0
        if self.pyPath != '':
            files = os.listdir(self.pyPath)
            for i in files:
                Path = self.pyPath + '\\' + i
                if os.path.isfile(Path):
                    if os.path.splitext(Path)[1].lower() == '.spec':
                        os.remove(i)
                        n += 1
        else:
            pass
        QMessageBox.information(self, "提示", "共找到"+str(n)+"个spec文件，并且全部清除完毕！")
    
    @pyqtSlot(bool)
    def on_actCleanPyo_triggered(self):
        '''清除pyo文件。'''
        n = 0
        if self.pyPath != '':
            files = os.listdir(self.pyPath)
            for i in files:
                Path = self.pyPath + '\\' + i
                if os.path.isfile(Path):
                    if os.path.splitext(Path)[1].lower() == '.pyo':
                        os.remove(i)
                        n += 1
        else:
            pass
        QMessageBox.information(self, "提示", "共找到"+str(n)+"个pyo文件，并且全部清除完毕！")

    @pyqtSlot(bool)
    def on_actModules_triggered(self):
        '''安装模块。'''
        dlgTitle = "输入文字对话框"
        txtLable = "请输入模块名称"
        echoMode = QLineEdit.Normal
        text, OK = QInputDialog.getText(self, dlgTitle, txtLable, echoMode)
        if OK:
            if text != '':
                self.BarLable.setText('正在安装'+text+"库……")
                self.Thread.Mode = 'install'
                self.Thread.command = "pip install " + text
                self.Thread.start()

    @pyqtSlot(bool)
    def on_actUModules_triggered(self):
        '''卸载模块。'''
        dlgTitle = "输入文字对话框"
        txtLable = "请输入模块名称"
        echoMode = QLineEdit.Normal
        text, OK = QInputDialog.getText(self, dlgTitle, txtLable, echoMode)
        if OK:
            if text != '':
                self.BarLable.setText('正在卸载'+text+"库……")
                self.Thread.Mode = 'uninstall'
                self.Thread.command = "pip uninstall -y " + text
                self.Thread.start()
    
    @pyqtSlot(bool)
    def on_actPerfect_triggered(self, bool):
        '''Action，编译后清除垃圾文件。'''
        if bool:
            if self.pyPath != '':
                Path = self.pyPath
            else:
                Path = os.getcwd()
            MoveTo = QFileDialog.getExistingDirectory(self, caption='选择目标文件夹',
            directory=Path, options=QFileDialog.ShowDirsOnly)
            if MoveTo != '':
                self.MoveTo = MoveTo.replace('/', '\\')
            else:
                self.ui.actPerfect.setChecked(False)
    
    @pyqtSlot(bool)
    def on_actColorW_triggered(self):
        pal = self.palette()
        iniColor = pal.color(QPalette.Window)
        color = QColorDialog.getColor(iniColor, self, '选择界面颜色')
        if color.getRgb()[:3] != (0, 0, 0):
            self.ColorW = [i for i in color.getRgb()]
            pal.setColor(QPalette.Window, color)
            self.setPalette(pal)
    
    @pyqtSlot(bool)
    def on_actColorT_triggered(self):
        pal = self.palette()
        iniColor = pal.color(QPalette.WindowText)
        color = QColorDialog.getColor(iniColor, self, '选择字体颜色')
        self.ColorT = [i for i in color.getRgb()]
        pal.setColor(QPalette.WindowText, color)
        self.setPalette(pal)

    @pyqtSlot(bool)
    def on_actAlpha_triggered(self):
        '''调节不透明度。'''
        pal = self.palette()
        iniColor = pal.color(QPalette.Window)
        iniAlpha = iniColor.getRgb()[3]
        dlgTitle = "输入不透明度对话框"
        txtLable = "调节窗口不透明度"
        minValue = 0
        maxValue = 255
        stepValue = 5
        inputValue, OK = QInputDialog.getInt(self, dlgTitle, txtLable, iniAlpha, minValue,
        maxValue, stepValue)
        if OK:
            self.ColorW[3] = inputValue
            iniColor.setAlpha(inputValue)
            pal.setColor(QPalette.Window, iniColor)
            self.setPalette(pal)
    
    @pyqtSlot(bool)
    def on_actHelp_triggered(self):
        webbrowser.open('https://github.com/Wiley2046/Pypacker')
    
    @pyqtSlot(bool)
    def on_actCleanJSON_triggered(self):
        FilePath = self.stayPath + '\\Settings.json'
        if os.path.exists(FilePath):
            os.remove(FilePath)
        QMessageBox.information(self, '提示', '清除完毕！')
    
    @pyqtSlot(bool)
    def on_actRestart_triggered(self):
        restart()
    
    @pyqtSlot(bool)
    def on_actChkRightMenu_triggered(self):
        self.ui.actRegFolder.setEnabled(True)
        self.ui.actRegFile.setEnabled(True)
        SET = RegSet.chkReg()
        self.ui.actRegFolder.setChecked(SET[0])
        self.ui.actRegFile.setChecked(SET[1])
    
    @pyqtSlot(bool)
    def on_actRegFile_triggered(self, checked):
        try:
            if checked:
                RegSet.addFile()
            else:
                RegSet.delFile()
        except PermissionError:
            QMessageBox.information(self, "提示", "缺失管理员权限，以管理模式运行本程序。")
            self.ui.actRegFile.setChecked(1-checked)

    @pyqtSlot(bool)
    def on_actRegFolder_triggered(self, checked):
        try:
            if checked:
                RegSet.addFolder()
            else:
                RegSet.delFolder()
        except PermissionError:
            QMessageBox.information(self, "提示", "缺失管理员权限，以管理模式运行本程序。")
            self.ui.actRegFolder.setChecked(1-checked)
    
    @pyqtSlot(bool)
    def on_actRestartAdm_triggered(self):
        self.DumpSettings('Temporary.json')
        restart('B')

    @pyqtSlot(bool)
    def on_actOutput_triggered(self):
        if self.MoveTo != '' and self.ui.actPerfect.isChecked():
            if os.path.exists(self.MoveTo):
                pass
            else:
                os.makedirs(self.MoveTo)
            os.system('start explorer {}'.format(self.MoveTo))
        elif self.pyPath != '':
            if os.path.exists(self.pyPath+'\\dist'):
                os.system('start explorer {}'.format(self.pyPath))
            else:
                QMessageBox.information(self, '提示', '还没有生成输出文件哦~')
        else:
            QMessageBox.information(self, '提示', '没有路径可以打开。')
    
    @pyqtSlot(bool)
    def on_actPassword_triggered(self):
        dlgTitle = "输入文字对话框"
        txtLable = "请输入密码(加密需要提前安装模块tinyaes，否则会导致程序bug)"
        echoMode = QLineEdit.Normal
        text, OK = QInputDialog.getText(self, dlgTitle, txtLable, echoMode, self.PassWord)
        if OK:
            if text != '':
                self.PassWord = text
    
    @pyqtSlot(bool)
    def on_actOpenInstallPath_triggered(self):
        os.system('start explorer {}'.format(self.stayPath))

    def MakeOutAction(self, Mode=''):
        '''检查Debug模式。'''
        if Mode == '':
            if self.ui.actDall.isChecked():
                return 'all'
            elif self.ui.actDimports.isChecked():
                return 'imports'
            elif self.ui.actDbootloader.isChecked():
                return 'bootloader'
            else:
                return 'noarchive'
        elif Mode == 'all':
            self.ui.actDall.setChecked(True)
        elif Mode == 'imports':
            self.ui.actDimports.setChecked(True)
        elif Mode == 'bootloader':
            self.ui.actDimports.setChecked(True)
        else:
            self.ui.actDnoarchive.setChecked(True)


    def setSpecLable(self):
        if self.pyName != '':
            self.ui.LabSpecName.setText(self.pyName[:-3]+'.spec )')
            self.specName = self.pyName[:-3]+'.spec'
        else:
            self.ui.LabSpecName.setText('xxxx.spec )')

    def LoadSettings(self, BOOL=False):
        Path = self.stayPath + '\\Temporary.json'
        if not os.path.exists(Path):
            Path = self.stayPath + '\\Settings.json'
        else:
            BOOL = True
        if os.path.exists(Path):
            File = open(Path, 'r')
            dic = json.load(File)
            if dic['Load'] or BOOL:
                self.ui.actLoad.setChecked(dic['Load'])
                self.pyPath = dic['pyPath']
                self.pyName = dic['pyName']
                self.icoPath = dic['icoPath']
                self.icoName = dic['icoName']
                self.specName = dic['specName']
                self.ui.actRigthMenu.setChecked(dic['RightMenu'])
                self.ui.rBtnNameSet.setChecked(dic['NameSet'])
                self.ui.rBtnDebug.setChecked(dic['Debug'])
                self.ui.rBtnFolder.setChecked(1-dic['OneFile'])                        #Bug大发现
                self.ui.chkConsole.setChecked(dic['Console'])
                self.ui.chkBat.setChecked(dic['Bat'])
                self.ui.chkSetIcon.setChecked(dic['SetIcon'])
                self.ui.actPerfect.setChecked(dic['Perfect'])
                self.ui.actExit.setChecked(dic['Exit'])
                self.ui.actExitSave.setChecked(dic['ExitSave'])
                self.ui.actExitDialog.setChecked(dic['ExitDialog'])
                self.ui.actFinishDianlog.setChecked(dic['FinishDianlog'])
                self.MoveTo = dic['MoveTo']
                self.ColorW = dic['ColorW']
                self.ColorT = dic['ColorT']
                self.ui.actSecret.setChecked(dic['Secret'])
                self.PassWord = dic['PassWord']
                self.SetColor(self.ColorW, 'W')
                self.SetColor(self.ColorT, 'T')
                if self.ui.chkSetIcon.isChecked():
                    if self.icoPath == '':
                        self.ui.chkSetIcon.setChecked(False)
                    elif self.icoName == '':
                        self.ui.chkSetIcon.setChecked(False)
                    elif not os.path.exists(self.icoPath+'/'+self.icoName):
                        self.ui.chkSetIcon.setChecked(False)
                self.ui.chkSaveSet.setChecked(dic['SaveSet'])
                self.ui.pBtnChico.setEnabled(dic['ChicoEnabled'])
                self.ui.pBtnOpen.setEnabled(dic['OpenEnabled'])
                if self.pyName != '':
                    self.ui.linePath.setText(self.pyPath+'\\'+self.pyName)
                if self.specName != '':
                    self.ui.LabSpecName.setText(self.specName+' )')
                else:
                    if self.pyName == '':
                        self.ui.LabSpecName.setText('xxxx.spec )')
                    else:
                        self.ui.LabSpecName.setText(self.pyName[:-3]+'.spec )')
                if self.pyPath != '':
                    self.ui.actCleanSpec.setEnabled(True)
                    self.ui.actCleanPyo.setEnabled(True)
                if dic['icoName'] != '':
                    self.ui.Labico.setText(dic['icoPath']+'/'+dic['icoName'])
                self.MakeOutAction(dic['DebugMode'])
            else:
                self.ui.actLoad.setChecked(False)
            File.close()
        else:
            self.DumpSettings()
        Path = self.stayPath + '\\Temporary.json'
        if os.path.exists(Path):
            os.remove(Path)
        
    
    def DumpSettings(self, Mode="Settings.json"):
        File = open(self.stayPath+"\\"+Mode, "w")
        File = open(self.stayPath+"\\"+Mode, "w")
        dic = dict()
        dic['Load'] = self.ui.actLoad.isChecked()
        dic['pyPath'] = self.pyPath
        dic['pyName'] = self.pyName
        dic['icoPath'] = self.icoPath
        dic['icoName'] = self.icoName
        dic['specName'] = self.specName
        dic['RightMenu'] = self.ui.actRigthMenu.isChecked()
        dic['NameSet'] = self.ui.rBtnNameSet.isChecked()
        dic['Debug'] = self.ui.rBtnDebug.isChecked()
        dic['OneFile'] = self.ui.rBtnOneFile.isChecked()
        dic['Console'] = self.ui.chkConsole.isChecked()
        dic['Bat'] = self.ui.chkBat.isChecked()
        dic['SetIcon'] = self.ui.chkSetIcon.isChecked()
        dic['ChicoEnabled'] = self.ui.pBtnChico.isEnabled()
        dic['OpenEnabled'] = self.ui.pBtnOpen.isEnabled()
        dic['SaveSet'] = self.ui.chkSaveSet.isChecked()
        dic['Perfect'] = self.ui.actPerfect.isChecked()
        dic['MoveTo'] = self.MoveTo
        dic['ColorW'] = self.ColorW
        dic['ColorT'] = self.ColorT
        dic['PassWord'] = self.PassWord
        dic['Secret'] = self.ui.actSecret.isChecked()
        dic['DebugMode'] = self.MakeOutAction()
        dic['Exit'] = self.ui.actExit.isChecked()
        dic['ExitSave'] = self.ui.actExitSave.isChecked()
        dic['ExitDialog'] = self.ui.actExitDialog.isChecked()
        dic['FinishDianlog'] = self.ui.actFinishDianlog.isChecked()
        json.dump(dic, File)
        File.close()
    
    def SetColor(self, colorTuple, Mode='W'):
        color = QColor()
        color.setRed(colorTuple[0])
        color.setGreen(colorTuple[1])
        color.setBlue(colorTuple[2])
        color.setAlpha(colorTuple[3])
        pal = self.palette()
        if Mode == 'W':
            pal.setColor(QPalette.Window, color)
        elif Mode == "T":
            pal.setColor(QPalette.WindowText, color)
        self.setPalette(pal)
    
    def closeEvent(self, event):
        if self.ui.actExitDialog.isChecked():
            reply = QMessageBox.question(self, "警告", "确认退出？")
            if reply == QMessageBox.Yes:
                if self.ui.actExitSave.isChecked():
                    self.DumpSettings()
                event.accept()
            else:
                event.ignore()
        else:
            if self.ui.actExitSave.isChecked():
                self.DumpSettings()
            event.accept()


def restart(Mode='A'):
    if Mode == 'A':
        qApp.exit(9420233)
    else:
        qApp.exit(2339420)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    while True:
        app = QApplication(sys.argv)
        form = Qmywindow()
        form.show()
        exitCode = app.exec_()
        if exitCode == 9420233:
            del form
            del app
        else:
            break
    if exitCode == 2339420:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)