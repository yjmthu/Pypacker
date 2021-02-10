# -*- coding: utf-8 -*-
# @Date    : 2021-02-06 23:34:01
# @Author  : Megix Wiley (yjmthu@gmail.com)
# @Link    : https://github.com/Wiley2046
# @Version : $Id$

from PyQt5.QtCore import QThread, pyqtSignal
import os, shutil, subprocess


class QmyTread(QThread):

    finish = pyqtSignal(bool)

    def __init__(self,  parent=None):
        super(QmyTread, self).__init__(parent)
        self.command = ''
        self.junkDirs = []
        self.junkFile = ''
        self.Mode = ''
        self.MoveTo = ''
        self.MainPath = ''
        self.MainName = ''
        self.FileMode = ''
    
    def run(self):
        try:
            self.Remove_Dirs()
            #os.system(self.command)
            subprocess.run(self.command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
            
            if self.Mode == 'build':
                if self.MoveTo != '':
                    if os.path.exists(self.MoveTo):
                        pass
                    else:
                        os.makedirs(self.MoveTo)
                    exeFile = os.listdir(self.junkDirs[0])
                    for i in exeFile:
                        if self.FileMode == 'File':
                            name = self.rename(self.MoveTo, i)
                            if name != i:
                                os.rename(self.junkDirs[0]+'\\'+i, self.junkDirs[0]+'/'+name)
                        elif self.FileMode == 'Folder':
                            if os.path.exists(self.MoveTo+'\\'+self.MainName):
                                shutil.rmtree(self.MoveTo+'\\'+self.MainName)
                            name = i
                        From = self.junkDirs[0] + '\\' + name
                        shutil.move(From, self.MoveTo)
                    self.Remove_Dirs()

            self.finish.emit(True)
        except:
            self.finish.emit(False)
    
    def rename(self, Path, Name, i=0):
        if i == 0:
            Named = Name
        else:
            Named = Name[:-4] + '({}).exe'.format(str(i))
        if os.path.exists(Path+'\\'+Named):
            i += 1
            return self.rename(Path, Name, i)
        else:
            return Named
    
    def Remove_Dirs(self):
        if self.junkDirs == [] or self.junkFile == '':
            self.junkDirs = [self.MainPath + '\\' + i for i in ['dist', 'build', '__pycache__']]
            self.junkFile = self.MainPath + '\\' + self.MainName + '.spec'
        if self.Mode == 'build':
            for Path in self.junkDirs:
                if os.path.exists(Path):
                    shutil.rmtree(Path)
            if os.path.exists(self.junkFile):
                os.remove(self.junkFile)
        for File in os.listdir(self.MainPath):
            Path = self.MainPath + '\\' + File
            if os.path.splitext(Path)[1].lower() == '.pyo':
                os.remove(Path)
