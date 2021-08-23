import requests
import os
import shutil
import time
from pathlib import Path
from zipfile import ZipFile
import configparser
import xml.etree.ElementTree as ET


def nexusdownload(url):
    print('Download Starting...')
    #Nexus URL to download the Package
    nexusurlpath = Path(url)
    artifactname = nexusurlpath.name
    #Creating temp folder if not present else if temp folder is present deleting all the files/folder present in it
    if not os.path.exists('temp'):
       os.makedirs('temp')
    else:
       shutil.rmtree('./temp/')
       os.makedirs('temp')
       #for f in os.listdir('temp'):
       #  os.remove(os.path.join('temp', f))   

    downloadpath = "./temp/"+nexusurlpath.name

    req = requests.get(url, stream=True)
    with open(downloadpath,'wb') as output_file:
        for chunk in req.iter_content(chunk_size=1025):
            if chunk:
                output_file.write(chunk)

    print('Download Completed!!!')         

def devdeployment(packagename):
    packagefoldername = packagename.split(".zip")[0]
    extractedpath = "./temp/"+packagefoldername
    zipfilepath = "./temp/"+packagename
    print('Changing Package Extension from ZIP to CAR!!!') 
    os.rename(zipfilepath,zipfilepath.replace("zip","car"))


def unzipnexuspackage(packagename):
    packagefoldername = packagename.split(".zip")[0]
    extractedpath = "./temp/"+packagefoldername
    zipfilepath = "./temp/"+packagename
    print('Unzipping the package: '+ packagename)
    # opening the zip file in READ mode
    with ZipFile(zipfilepath, 'r') as zip:
        # printing all the contents of the zip file
        #zip.printdir()
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall(extractedpath)
        print('Zip File Extracted! and deleting the src zip file')
        zip.close()
        time.sleep(2)
        os.remove(zipfilepath)



def configupdate(packagename,env):
    packagefoldername = packagename.split(".zip")[0]
    extractedpath = "./temp/"+packagefoldername
    zipfilepath = "./temp/"+packagename 
    #Reading configuration paramters
    configfile = env+".ini"
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(configfile)

    for section_name in config.sections():
        artifact = config[section_name]['artifact']
        version = config[section_name]['version']
        path=extractedpath+"/"+artifact+"_"+version+"/"+artifact+"-"+version+".xml"
        print("updating config of "+ section_name + "...")

        tree = ET.parse(path)
        root = tree.getroot()
        ET.register_namespace("", "http://ws.apache.org/ns/synapse")
        ns = {"":"http://ws.apache.org/ns/synapse","xmlns":"http://ws.apache.org/ns/synapse"}
    
        options = config.options(section_name)
        options.remove("artifact")
        options.remove("version")
        for keyvalues in options:
            element = ".//xmlns:"+keyvalues
            tag = root.find(element,ns)
            tag.text = config[section_name][keyvalues]
        tree.write(path,xml_declaration=True, method='xml', encoding="utf8")
        print(section_name + "config update is done")



    
