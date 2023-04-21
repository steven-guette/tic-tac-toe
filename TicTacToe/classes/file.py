"""
@Author  : GUETTE Steven
@Class   : File
@Version : 1.0.0
@Since   : 2023
"""

from classes.whiteshield import WShield
import os


class File:
    def __init__(self, relpath, writeAppend):
        self._Filepath = File.RelativeToAbsolute(relpath)

        if WShield.IsBool(writeAppend):
            self._WriteAppend = writeAppend
        else:
            self._WriteAppend = False

    # region METHODS

    def FileExists(self):
        return os.path.exists(self.Filepath)

    def DirExists(self):
        return os.path.exists(self.Filepath)

    def CreateDir(self):
        if not self.DirExists():
            os.makedirs(os.path.dirname(self.Filepath))

    def Remove(self):
        if self.FileExists(self.Filepath):
            os.remove(self.Filepath)

    def FileExists(path):
        return os.path.exists(path)

    FileExists = staticmethod(FileExists)

    def DirExists(path):
        return os.path.exists(os.path.dirname(path))

    DirExists = staticmethod(DirExists)

    def CreateDir(path):
        if not File.DirExists(path):
            os.makedirs(os.path.dirname(path))

    CreateDir = staticmethod(CreateDir)

    def RelativeToAbsolute(path):
        return os.path.abspath(path)

    RelativeToAbsolute = staticmethod(RelativeToAbsolute)

    # endregion

    # region GETTERS

    def GetContent(self):
        fileContent = list()

        if self.FileExists(self.Filepath):
            with open(self.Filepath, "r") as file:
                for fileLine in file:
                    fileContent.append(fileLine)

        return fileContent

    def GetFilepath(self):
        return self._Filepath

    def GetWriteAppend(self):
        return self._WriteAppend

        # endregion

    # region SETTERS

    def SetContent(self, datas):
        toAdd = list()

        if WShield.IsString(datas):
            toAdd.append(datas)
        elif WShield.IsList(datas):
            toAdd.extend(datas)

        if len(toAdd) > 0:
            self.CreateDir()

            mode = "w"
            if self.WriteAppend:
                mode = "a"

            with open(self.Filepath, mode) as file:
                for newLine in toAdd:
                    file.write(f"{newLine}\n")

            return True
        return False

    def SetFilepath(self, filepath):
        if WShield.IsString(filepath):
            self._Filepath = File.RelativeToAbsolute(filepath)

    def SetWriteAppend(self, value):
        if WShield.IsBool(value):
            self._WriteAppend = value

    # endregion

    Filepath = property(GetFilepath, SetFilepath)
    WriteAppend = property(GetWriteAppend, SetWriteAppend)
