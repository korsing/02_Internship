import openpyxl
import dns.resolver
import sys

workbook = openpyxl.load_workbook("cat.xlsx")
worksheet = workbook["All"]

def find_Cname(domain):
  try:
    print("!!!", domain)
    for rdata in dns.resolver.query(domain.strip(), 'CNAME'):
      cDomain = str(rdata.target)
      # sys.stdout.write(CYAN)
      print ("CNAME is detected from {0} : {1}, CDN vendor is {2}".format(domain,cDomain,find_Vendor(cDomain)))
      # sys.stdout.write(RESET)
      find_Cname(cDomain[0:len(cDomain)-1])
    except:
      find_ARecord(domain)

def find_ARecord(domain):
	try:
		for rdata in dns.resolver.query(domain, 'A'):
			print("CNAME is not detected from {0}, IP Address is {1}".format(domain,rdata.address))
	except:
		print("Can't find DNS lookup: " + domain)
	finally:
		print("------------------------------------------------------------------------------------------------------------------------")

colC = ws['E']
for cell in colC:
	if (len(str(cell.value))) > 7:
		find_Cname(cell.value)