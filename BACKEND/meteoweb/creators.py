__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################

from datetime import datetime
import os
import pandas as pd
#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation and distribution
# import collectors

## Module importation to be developing
from . import collectors
#--------------------------------------------------------------#


########################    Function    ########################

def isredundant(dfObj, pathfolder):
    try:
        filepath = os.listdir(pathfolder)[-1]
    except IndexError as e:
        print(e)
    else:
        oldFile = pd.read_csv(pathfolder + os.sep + filepath, encoding='utf-8')
        for n, row in dfObj.iterrows():
            newRow = list(map(str, list(row)))
            oldRow = list(map(str, list(oldFile.iloc[n])))
            if newRow != oldRow:
                return False
        return True
#--------------------------------------------------------------#


########################    Classes    ########################

class File_24H:

    def __init__(self, placeAtts, format, encoding):
        self.tp = placeAtts["path"]
        self.url = placeAtts["url"]
        self.name = placeAtts["city"]
        self.format = format
        self.filename = None
        self.filepath = None
        self.encod = encoding

    def Filename(self):
        # Current Running Date
        creation = datetime.now().strftime("%d%m%y_%H%M")
        
        # Date name parameters
        self.day = creation.split('_')[0]
        self.time = creation.split('_')[1]
        
        # Full filename generation
        name = self.name + '_C' + creation
        filename = name + '.' + self.format
        self.filename = filename

    def FileDir(self, mainFolderName='24H'):
        self.Filename()
        childfolder = self.tp + os.sep + mainFolderName
        folder = childfolder + os.sep + self.day
        self.filedir = folder

    def FilePath(self):
        self.FileDir()
        filepath = self.filedir + os.sep + self.filename
        self.filepath = filepath

    def NewFile(self, obj=collectors.DailyArray):
        self.FilePath()
        directory = self.filedir
        content = obj(self.url)
        df = content.genArray()
        if not os.path.exists(directory):
            os.makedirs(directory)
            df.to_csv(self.filepath, encoding='utf-8', index=False)
        else:
            if len(os.listdir(directory)) > 0 and not isredundant(df, directory):
                df.to_csv(self.filepath, encoding='utf-8', index=False)


class File_14Days(File_24H):
    
    def __init__(self, placeAtts, format, encoding):
        super().__init__(placeAtts, format, encoding)
    
    def FileDir(self, mainFolderName='14Days'):
        self.Filename()
        folder = self.tp + os.sep + mainFolderName
        self.filedir = folder
    
    def NewFile(self, obj=collectors.ForeteenArray):
        return super().NewFile(obj)



class File_3H(File_24H):

    def __init__(self, placeAtts, format, encoding):
        super().__init__(placeAtts, format, encoding)

    def Filenames(self):
        super().Filename()
        n = int(self.day[:2])
        names = []
        for _ in range(8):
            init = str(n) + '_' + self.filename
            names.append(init)
            n += 1
        self.filenames = names

    def FileDir(self, mainFolderName='3H'):
        super().FileDir(mainFolderName)
        self.Filenames()
        pathcomps = [self.filedir, self.time]
        self.filedir = os.sep.join(pathcomps)

    def FilePaths(self):
        self.FileDir()
        filepaths = []
        for name in self.filenames:
            filepath = self.filedir + os.sep + name
            filepaths.append(filepath)
        self.filepaths = filepaths

    def NewFile(self, obj=collectors.H3Array):
        self.FilePaths()
        directory = self.filedir
        content = obj(self.url)
        dfs = content.genArray()
        for i,df in enumerate(dfs):
            if not os.path.exists(directory):
                os.makedirs(directory)
                df.to_csv(self.filepaths[i], encoding='utf-8', index=False)
            else:
                df.to_csv(self.filepaths[i], encoding='utf-8', index=False)


class File_1H(File_3H):

    def __init__(self, placeAtts, format, encoding):
        super().__init__(placeAtts, format, encoding)

    def FileDir(self, mainFolderName='1H'):
        super().FileDir(mainFolderName)

    def NewFile(self, obj=collectors.H1Array):
        return super().NewFile(obj)


class File_Brief(File_24H):

    def __init__(self, placeAtts, format, encoding='utf-8'):
        super().__init__(placeAtts, format, encoding)

    def Filename(self):
        creation = datetime.now().strftime("%d%m%y_%H%M")
        self.day = creation.split('_')[0]
        self.time = creation.split('_')[1]
        name = 'C' + creation
        filename = name + '.' + self.format
        self.filename = filename

    # def FileDir(self, mainFolderName='Summations'):
    #     self.Filename()
    #     childfolder = self.tp.split(os.sep)
    #     self.filedir = os.sep.join(childfolder[:-1]) + os.sep + mainFolderName
    #     if not os.path.exists(self.filedir):
    #         os.makedirs(self.filedir)
    
    def FormatRecords(self):
        collector = collectors.Brief(self.url)
        for i,url in enumerate(collector.urls):
            if i == 6: last = True
            else: last = False
            meteoData = collector.genArray(url, last)
            meteoData.insert(0, self.name)
            yield meteoData



class File_Brief14(File_Brief):
    
    def __init__(self, placeAtts, format, encoding='utf-8'):
        super().__init__(placeAtts, format, encoding)
    
    def FormatRecords(self):
        dfByPlace = collectors.Brief14(self.url)
        out = dfByPlace.genArray()
        out.insert(0, "Loc", [self.name]*14)
        return out
#--------------------------------------------------------------#



if __name__ == '__main__':
    from dotenv import load_dotenv as env
    env()
    ini = File_Brief14(os.getenv('json'), 'txt')
    print(ini.FormatRecords())
    # import sys
    # print(sys.getsizeof(next(ini.FormatRecords())))
