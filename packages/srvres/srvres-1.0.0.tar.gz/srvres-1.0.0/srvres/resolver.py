from dns.resolver import Resolver, NXDOMAIN, NoAnswer
from srvres.utils import sorted_groupby, priority_sort, choice
from srvres.service_ports import service_ports

class SRVResolver:
	class Iterator:
		def __init__(self,grouped_records):
			self.records = grouped_records
		def __next__(self):
			if len(self.records)==0: raise StopIteration
			group = self.records[0]
			while len(group[1])==0:
				self.records.pop(0)
				if len(self.records)==0: raise StopIteration
				group = self.records[0]
			_, records = group # ditch priority value
			weights = [x.weight+1 for x in records]
			record = choice(records,weights)
			records.remove(record)
			return (record.target.to_text().rstrip("."),record.port)
	def __init__(self,service,domain,transport="tcp",resolver=None,port=0):
		if resolver is None: resolver=Resolver()
		self.srv_part = f"_{service}._{transport}"
		if port==0:
			port = service_ports.get(self.srv_part,0)
		self.domain = domain
		self.port = port
		self.resolver = resolver
	@property
	def qname(self):
		return ".".join([self.srv_part,self.domain])
	def __iter__(self):
		try:
			result = self.resolver.query(self.qname,"SRV")
		except (NXDOMAIN, NoAnswer):
			return iter([(self.domain,self.port)])
		grouped_records = []
		for priority, records in sorted_groupby(result,priority_sort):
			grouped_records.append((priority,list(records)))
		return SRVResolver.Iterator(grouped_records)
