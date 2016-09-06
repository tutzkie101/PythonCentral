import os
hostname = "google.com" #example
response = os.system("ping " + hostname+" -n 10")
#response = os.system("ping 10.7.0.25 -n 10")
#response = os.system("ping 10.7.0.41 -n 10")
#response = os.system("ping lightriver.com -n 10")
#and then check the response...
if response == 0:
  print (hostname, 'is up!')
else:
  print (hostname, 'is down!')
 