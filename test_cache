from Cache import Cache
from ResourceRecord import ResourceRecord


a = Cache()

rr1 = ResourceRecord("aaa.com", 1, 1, 1000, "1.2.3.4")
RR2 = ResourceRecord("bbb.com", 1, 1, 1000, "4.1.3")
RR3 = ResourceRecord("ccc.com", 1, 1, 1000, "3.1.2")
RR4 = ResourceRecord("ccc.", 1, 1, 1000, "3.1.2")


#a.put(("aaa.com", 1, 1), RR1)
print(rr1.to_string())
a.put( (rr1._name, rr1._type, rr1._class), rr1 )
a.put(("bbb.com", 1, 1), RR2)
a.put(("ccc.com", 1, 1), RR3)
a.put( ("ccc.",1,1), RR4 )

print(a.get(("aaja.com", 1, 1)))

print(a.get( ("aaa.com", 1, 1) ).to_string())

print( a.get(("ccc.",1,1)).to_string() )


