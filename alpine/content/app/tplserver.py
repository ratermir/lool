from http.server import HTTPServer
import tplengine, logging, os

log = logging.getLogger("tplserver")
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

config = tplengine.loadConfig("oms-config.yaml")

addr = "0.0.0.0"
port = 8421

if "server" in config:
    svrcfg = config["server"]
    if "port" in svrcfg:
        port = int(svrcfg["port"])
    if "address" in svrcfg:
        addr = svrcfg["address"]

httpd = HTTPServer((addr, port), tplengine.TemplateEngineServer)
log.info("Starting HTTP server listening on port %s", port)
httpd.serve_forever()

