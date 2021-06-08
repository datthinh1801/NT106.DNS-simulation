import dns.resolver
import dns.zone
#test enter wrong domain name with false rasie exception
domain = "sontruong.asia"
#domain = "a.ns.facebook.com"
print("--- Viet nam server ---")
my_resolver = dns.resolver.Resolver()
# Public IP of Vietnam Internet Network Information Center
my_resolver.nameservers=['203.119.36.106']
#my_resolver.nameservers = ['129.134.30.12']
answer = my_resolver.resolve(domain)
print(answer.response)
print ("--- Google server ---")
my_resolver = dns.resolver.Resolver()
# Public IP of Vietnam Internet Network Information Center
my_resolver.nameservers=['8.8.8.8']
answer = my_resolver.resolve(domain)
print(answer.response)


# import dns.zone
# import dns.query
# import dns.resolver
# import dns.reversename

# #soa_answer = dns.reversename.from_address('8.8.8.8')
# soa_answer = dns.resolver.resolve('dns.google.','SOA')

# print(soa_answer[0].mname)
# print(len(soa_answer))

# master_ans = dns.resolver.resolve(soa_answer[0].mname,'A')
# print(master_ans[0].address)

# zone = dns.zone.from_xfr(dns.query.xfr(master_ans[0].address,'dns.google.'))

# #print(len(z))
# soa_answer = dns.resolver.resolve('dns.google.','SOA')
# print(soa_answer.response)
# master_answer = dns.resolver.resolve(soa_answer[0].mname, 'A')
# print(master_answer[0].address)
# xfr = dns.query.xfr(where=master_answer[0].address, zone='dns.google')
# print()
# z = dns.zone.from_xfr(xfr)
# for n in sorted(z.nodes.keys()):
#     print(z[n].to_text(n))
# soa_answers = dns.resolver.resolve('dnspython.org', 'NS')
# names = soa_answers.chaining_result.__dict__['answer']
# master_answer = dns.resolver.resolve(soa_answer[0].mname, 'NS')

# zone = dns.zone.from_xfr(dns.query.xfr('3.211.54.86','megacorpone.com'))
#
# import dns.zone
#
# zone = dns.zone.from_file(f='zonefile.txt')
#
# print(zone.to_text())
# for (name, ttl, rdata) in zone.iterate_rdatas('MX'):
#     print(name, ttl, rdata)
