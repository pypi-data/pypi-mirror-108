from urllib.request import urlopen
from os.path import expanduser
from csv import reader as csv_reader
import json
IANA_SERVICE_NAME_PORT_REGISTRY = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"
ADDITIONAL_SERVICE_REGISTRY = "https://khuxkm.tilde.team/additional_service_ports.csv"
CACHED_DB_PATHS = ["~/.local/share/service_ports.json"]

service_ports = {}
loaded = False
for path in CACHED_DB_PATHS:
	path = expanduser(path)
	try:
		with open(path) as f: service_ports=json.load(f)
		loaded=True
	except:
		pass

# wrapper to decode lines, since csv complains if you give it bytes and not strings
class DecodeIterator:
	def __init__(self,f):
		self.lines = [l.decode() for l in f]
	def __iter__(self):
		return iter(self.lines)

if not loaded:
	# load the official service name and port registry
	reader = csv_reader(DecodeIterator(urlopen(IANA_SERVICE_NAME_PORT_REGISTRY)))
	_ = next(reader) # skip header
	for row in reader:
		# only handle cases where protocol, transport, and port are defined
		# this avoids the unassigned blocks, or cases where a service has no port/vice versa
		if not (row[0] and row[1] and row[2]): continue
		key = f"_{row[0]}._{row[2]}"
		try:
			port = int(row[1])
		except:
			port = int(row[1].split("-")[0])
		service_ports[key]=port
	try:
		# attempt to load the custom additional service registry, which includes services not registered with the IANA that are nonetheless widely used
		reader = csv_reader(DecodeIterator(urlopen(ADDITIONAL_SERVICE_REGISTRY)))
		for row in reader:
			# only handle cases where protocol, transport, and port are defined
			# they always should be, but just in case
			if not (row[0] and row[1] and row[2]): continue
			key = f"_{row[0]}._{row[2]}"
			try:
				port = int(row[1])
			except:
				port = int(row[1].split("-")[0])
			service_ports[key]=port
	except: pass
	with open(expanduser(CACHED_DB_PATHS[0]),"w") as f:
		json.dump(service_ports,f)
