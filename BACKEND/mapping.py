from meteoweb import collectors
import logic

from dotenv import load_dotenv as env
env()

attObj = collectors.Attribute
genObj = logic.getPlaces

ini = collectors.AttributesTable(attObj=attObj, genObj=genObj)
print(ini.map)