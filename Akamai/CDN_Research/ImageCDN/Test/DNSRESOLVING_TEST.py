import dns.resolver
def cname(domain):
        try:
                while(1):
                        for rdata in dns.resolver.query(domain.strip(), "CNAME"):
                                cDomain = str(rdata)
                                print(cDomain)
                                domain = cDomain[:len(cDomain)-1]
        except:
                for rdata in dns.resolver.query(domain.strip(), "A"):
                        print (rdata.address)

			
