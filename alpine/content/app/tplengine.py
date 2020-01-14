import pystache, tempfile, zipfile, uuid, shutil, os
import subprocess, yaml, logging, json, traceback
from pathlib import Path

from http.server import BaseHTTPRequestHandler

# ===================================================

def guessType(iType):
    return {
        "html": "text/html",
        "pdf": "application/pdf"
    }.get(iType)

def loadConfig(cfgFile):
    """Loads configuration from the fle passed to the command. 
    
    Args:
        cfgFile: path to the yaml file with configuration.  
    
    """
    with open(cfgFile, "r") as cfgFile : config = yaml.load(cfgFile, Loader=yaml.FullLoader)
    return config

def formatError(iStatus, code, msg):
    return {
        "status": iStatus,
        "type": "application/json",
        "content": bytearray(json.dumps({
                "returnno": -1,
                "returncode": code,
                "message": msg
            }), "utf-8")
        }


class TemplateEngine:

    log = logging.getLogger("TemplateEngine")
    
    def __init__(self, iConfig):
        
        self.config = iConfig
#        with open("oms-config.yaml", "r") as cfgFile : self.config = yaml.load(cfgFile, Loader=yaml.FullLoader)
    
        self.templateBase = self.config["paths"]["templateBase"]
        self.imageSourcePath = self.config["paths"]["signatures"]
        self.libreofficePath = self.config["paths"]["libreoffice"]
        
        self.tempBaseDir = os.sep.join([str(Path(tempfile.TemporaryDirectory().name).parent), "pytplengine"])
        
        
        try :
            os.mkdir(self.tempBaseDir)
            self.log.info("Template directory '%s' created", self.tempBaseDir);
        except FileExistsError:
            self.log.info("Template directory '%s' already exists", self.tempBaseDir);
        self.log.info("Working directory '%s' created", self.tempBaseDir)
    
    def processTemplate(self, sourceData) :
    
        output = {}
        
        self.log.info("Document generating started")
        templateBaseName = sourceData["templateName"]
        outputType = sourceData["outputType"] if "outputType" in sourceData else "pdf"
    
        firstLang = sourceData["firstLanguage"]
        secLang = ("_" + sourceData["secondLanguage"]) if ("secondLanguage" in sourceData and sourceData["secondLanguage"].strip()) else ""
        
        templateFile = os.sep.join([self.templateBase, templateBaseName, templateBaseName + "_" + firstLang + secLang + ".docx"])
        contentType = guessType(outputType) 
        if not contentType:
            return formatError(422, "UNSUPPORTED_OUTPUT_TYPE", "Output document type '" + outputType + "' is not allowed")
    
        docContentSubdir = "word"
        docFileName = "document.xml"
        mediaSubdir = "word/media"
    
        outputFileName = str(uuid.uuid4()) + ".pdf"
    
        self.log.debug("Template file: '%s'", templateFile)
    
        with tempfile.TemporaryDirectory("", "", self.tempBaseDir) as td_name :
        
            targetDocx = os.sep.join([td_name, os.path.splitext(outputFileName)[0] + ".docx"])
            targetZipDir = os.sep.join([td_name, "doc_content"])
            outputDirectory = td_name
#            profileDir = os.sep.join([td_name, "loprofile"]) 
#            os.mkdir(profileDir)
            profileDir = td_name 

            self.log.debug("Target zip file: '%s'", targetZipDir)
        
            with zipfile.ZipFile(templateFile, "r") as zf : zf.extractall(targetZipDir)
            with open(targetZipDir + "/" + docContentSubdir + "/" + docFileName, "r", encoding="utf-8") as inf : content = inf.read()
        
            result = pystache.render(content, sourceData["documentContent"]["data"])
            with open(targetZipDir + "/" + docContentSubdir + "/" + docFileName, "w+", encoding="utf-8") as outf : outf.write(result)
            
            sigs = sourceData["documentContent"]["signatures"]
            for key in sigs :
                shutil.copy(
                    self.imageSourcePath + "/" + sigs[key] + ".png", 
                    targetZipDir + "/" + mediaSubdir + "/" + self.config["signatures"][key] + ".png"
                )
        
            shutil.make_archive(targetDocx, "zip", targetZipDir)
            os.rename(targetDocx+".zip", targetDocx)

            self.log.debug("Starting conversion of '%s' to type '%s'", targetDocx, outputType)
            spr = subprocess.run([self.libreofficePath, 
                                    "--headless", 
                                    "--convert-to", outputType, 
                                    "--outdir", outputDirectory,
                                    " -env:UserInstallation=\"file://"+profileDir+"\"", 
                                    targetDocx
                                ])
            retcode = spr.returncode 
            if retcode == 0:
                self.log.debug("Conversion finished")
                try:
                    resultFile = os.path.splitext(targetDocx)[0] + "." + outputType
                    self.log.debug("Generated file loading start: '%s'", resultFile)
                    with open(resultFile, "rb") as f: 
                        output["content"] = bytearray(f.read())
                    self.log.debug("Generated file '%s' loaded", resultFile)
                    output["status"] = 200
                    output["type"] = contentType
                except Exception as ex:
                    self.log.error("Cannot load generated document: %s", str(ex))
                    output = formatError(500, "CONVERSION_ERROR", "Cannot convert document: " + str(ex))
            else:
                self.log.error("Conversion exded with error: %s", str(spr.stderr))
                output = formatError(500, "CONVERSION_ERROR", "Cannot convert document: errno=" + str(retcode) + ", " + str(spr.stderr))

        return output 

    def readDataFromFile(self, srcDataFile):
        self.log.info("Loading data file '%s'", srcDataFile)
        with open(srcDataFile) as offile : sourceData = eval(offile.read())
        return sourceData


class TemplateEngineServer(BaseHTTPRequestHandler):

    log = logging.getLogger("TemplateEngineServer")
    processor = TemplateEngine(loadConfig("oms-config.yaml"))

    def send_error(self, code, message=None):
        if code >= 400 and code < 500:
            self.error_message_format = message if message else "Error during request processing"
        BaseHTTPRequestHandler.send_error(self, code, message)

    def do_POST(self):

        post_data = self.rfile.read(int(self.headers["Content-Length"]))
        
        try:
            self.log.debug("Sending response")
            output = self.processor.processTemplate(eval(post_data))

            self.send_response(output["status"])
            self.log.debug("Response status is set: %s", output["status"])

            self.send_header("Content-type", output["type"])
            self.end_headers()
            if "content" in output:
                self.wfile.write(output["content"])
                self.log.debug("Output File Content sent")
        except Exception as ex:
            print(traceback.format_exc())
            errMsg = "Exception during request processing: " + str(ex)
            self.log.error(errMsg)
            self.send_error(600, errMsg)

