from CacheSystem import CacheSystem
from ResourceRecord import ResourceRecord
from ParseString import parse_string_cachesystem



a = CacheSystem()

rr1 = ResourceRecord("aaa.com", 1, 1, 1000, "1.2.3.4")
RR2 = ResourceRecord("bbb.com", 1, 1, 1000, "4.1.3")
RR3 = ResourceRecord("ccc.com", 1, 1, 1000, "3.1.2")
RR4 = ResourceRecord("ccc.", 1, 1, 1000, "3.1.2")


#a.put(("aaa.com", 1, 1), RR1)
a.put(rr1)
a.put(RR2)
a.put(RR3)
a.put(RR4)

print(a.get("aaa.com", 1, 1).to_string())
print(a.get("bbb.com", 1, 1).to_string())

print(a.to_string())

string = a.to_string()

b = parse_string_cachesystem(string)
print(b.get("bbb.com", 1, 1).to_string())