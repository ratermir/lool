import logging, os, sys, tplengine

log = logging.getLogger("tplcmd")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

if len(sys.argv) < 3:
    log.error("At least 2 arguments are expected: source Json file and output file")
    sys.exit(1)

log.debug("Template converted, saving output")
processor = tplengine.TemplateEngine(tplengine.loadConfig("oms-config.yaml"))
output = processor.processTemplate(processor.readDataFromFile(sys.argv[1]))

log.debug("Template converted, saving output")
with open(sys.argv[2], "w+b") as ofile : ofile.write(output["content"])
log.debug("Output file '%s' saved", sys.argv[2])
