# srvres

A somewhat simple-- yet useful-- SRV resolver in around 100 lines of Python code.

## How to use

```python
import srvres, socket

sock = None
for target in srvres.SRVResolver("xmpp-client","xmpp.example.com"):
	sock = socket.socket()
	sock.settimeout(5)
	try:
		sock.connect(target)
		break
	except socket.timeout: pass
if sock is None:
	# the service is unavailable
else:
	# the service is available and connected to
```

## Explanation

The magic occurs in the `srvres.SRVResolver` object. When you iterate over a SRVResolver object, it makes the DNS query for the SRV record for the specified service. If it gets an answer, it returns a `srvres.SRVResolver.Iterator` object, which handles priority and weighting. If it doesn't get an answer, it falls back to the given domain and a known port (if a port is known). If a port is not known, the default response will include a port of 0. This can be changed by supplying a `port` argument to the `srvres.SRVResolver` constructor like so:

```
# "unknownprotocol" listens on port 49151
for target in srvres.SRVResolver("unknownprotocol","example.com",port=49151):
	# now the unknown response will have port 49151 as opposed to 0
```

## What ports are classified as "known"?

When you first import the library, it will download the IANA registry of assigned service names and port numbers, which it ports into a format it can more easily use. It also downloads a separate registry, maintained by me, that includes a handful of other useful ports that aren't defined by the IANA registry.

Basically, if you have an IANA registration for your service name, and it includes a port and transport, you'll be able to use your service name with no issues. If you don't, and your service is a widely used one, ask me and I'll probably add it to my list.
