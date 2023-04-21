"""
@Author  : GUETTE Steven
@Class   : JSONFile
@Version : 1.0.0
@Since   : 2023
"""

import json
from classes.whiteshield import WShield
from classes.file import File


class JSONFile(File):
    def __int__(self, relpath, writeAppend):
        File.__init__(self, relpath, writeAppend)

    # region GETTERS

    def GetContent(self):
        fileContent = list()

        if self.FileExists(self.Filepath):
            with open(self.Filepath, "r") as file:
                for fileLine in file:
                    fileContent.append(json.loads(fileLine))

        return fileContent

    # endregion

    # Region SETTERS

    def SetContent(self, datas):
        toAdd = list()

        if WShield.IsString(datas) or WShield.IsDict(datas):
            toAdd.append(datas)
        elif WShield.IsList(datas):
            toAdd.extend(datas)

        if len(toAdd) > 0:
            self.CreateDir(self.Filepath)

            mode = "w"
            if self.WriteAppend:
                mode = "a"

            with open(self.Filepath, mode) as file:
                for newLine in toAdd:
                    file.write("{}\n".format(json.dumps(newLine)))

            return True
        return False

    # endregion
