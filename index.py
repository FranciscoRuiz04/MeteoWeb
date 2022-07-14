import gps2df
from datetime import datetime
import os

def toFile(path, mainurl, format='txt'):
    content = gps2df.run(mainurl)
    name = datetime.now().strftime("%b-%d-%Y-%H_%M")
    file = path + os.sep + name + '.' + format
    content.to_csv(file, encoding='utf-8', index=False)

# if __name__=='__main__':
toFile(os.getenv('mypath'), os.getenv('starturl'))