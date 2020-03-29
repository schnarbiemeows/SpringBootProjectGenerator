import os
import shutil

"""
    utility class
"""
class Utilities:

    """
        utility for creating a directory
    """
    def mkdir(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
            print("making directory : " + path)
        else:
            print(path+ " already exists")

    """
        utility for copying a file
    """
    def cpy(self,srcpath,destpath):
        if not os.path.exists(destpath):
            shutil.copy(srcpath,destpath)
            print("copying file from : " + srcpath + " to : " + destpath)
        else:
            print(destpath+ " already exists")

    """
        small function to capitalize the first letter of the javaname
    """
    def capitalize(self,word):
        letter = word[0].upper()
        restofword = word[1:len(word)]
        totalword = letter + restofword
        return totalword

