import gps2df
from datetime import datetime
import os
import sys

def toFile(path, format, mainurl):
    content = gps2df.run(mainurl)
    name = datetime.now().strftime("%b-%d-%Y-%H_%M")
    file = path + os.sep + name + '.' + format
    content.to_csv(file, encoding='utf-8', index=False)

if __name__=='__main__':
    toFile(sys.argv[1], sys.argv[2], sys.argv[3])