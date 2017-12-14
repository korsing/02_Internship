category = {
            "Akamai" :                         [".globalredir.akadns.net", ".akadns.net", ".edgekey.net", ".edgesuite.net", ".akamaiedge.net", ".akamai.net"],
            "Level3" :                         [".nstatic.net", ".footprint.net"],
            "Microsoft" :                      [".azurewebsites.net", ".cloudapp.net", ".msecnd.net"],
            "Amazon" :                         [".elb.amazonaws.com", ".amazonaws.com", ".cloudfront.net"],
            "Wix" :                            [".wixdns.net", ".wix.com"],
            "OkServer Internet Solution Inc" : [".okserver.cn", "okserver.net"],
            "CDNETWORKS" :                     [".gccdn.net", ".cdnetworks.net", ".cdngc.net", ".cdngs.net", ".speedcdn.net", ".cdngl.net", ".cdnga.net"],
            "Limelight Networks" :             [".llnwd.net", ".lldns.net"],
            "Verizon - EdgeCast" :             [".v0cdn.net", ".edgecastcdn.net", ".cedexis.net", ".mucdn.net"],
            "Fastly" :                         [".fastly.net"],
            "CloudFlare" :                     [".cloudflare.net"],
            "Highwinds" :                      [".hwcdn.net"],
            "CDN77(onApp)" :                   [".cdn77.org"],
            "ChinaCache" :                     [".lxsvc.cn", ".ccgslb.com", ".ccna.c3cdn.net"],
            "Yahoo" :                          [".yahoo"],
            "Google" :                         [".google.com", ".doubleclick.net", ".firebaseapp.com"],
            "Mirror Image" :                   [".instacontent.net"],
            "Cachefly" :                       [".cachefly.net"],
            "Coral Cache" :                    [".nyucd.net"],
            "MaxCDN" :                         [".netdna-cdn.com"],
            "NHN Corp." :                      [".navercdn.com", ".nheos.com"],
            "GS Neotek":                       [".gscdn.net", ".gscdn.com"],
            "LG" :                             [".xcdn.com", ".cdn.cloudn.co.kr"],
            "KT" :                             [".ktics.co.kr"],
            "Hyosung" :                        [".hscdn.com"],
            "Penta Security Systems" :         [".cbricdns.com"],
            "NCIA Sheild Service" :            [".nciashield.org"],
            "Redhat" :                         [".rhcloud.com"],
            "G-Core Labs S.A." :               [".core.pw"],
            "SQUARESPACE" :                    [".squarespace.com"],
            "KINX" :                           [".kinxcdn.com"],
            "Whois Web" :                      [".whoisweb.net"]
           }

cdn_vendor = list(category.keys())

for i in range(len(cdn_vendor)):
    print(category.get(cdn_vendor[i]))
    print(cdn_vendor[i])