import deploymentlib
from pathlib import Path

nexusrepositoryurl = "http://172.18.0.3:8081/repository/micro-integrator/MI-MongoDBSample/MI-MongoDBSample-CAR/1.0.0/MI-MongoDBSample-CAR-1.0.0.zip"
nexusurlpath = Path(nexusrepositoryurl)
artifactname = nexusurlpath.name

deploymentlib.nexusdownload(nexusrepositoryurl)
deploymentlib.devdeployment(artifactname)



