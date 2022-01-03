import requests,argparse
from utility import UrlToDomain
from time import sleep

parser = argparse.ArgumentParser(description = "Reflected XSS Scanner Tool",
								 epilog="eg=> ./AutoXSS [options]"
								 )
 
# Adding URL Arguments
URLGroup = parser.add_mutually_exclusive_group(required=True)
URLGroup.add_argument("-U", "--Url", help = "URL/Domain to Test On", type=str)
URLGroup.add_argument("-UF", "--URLFile", help="file input for multiple URL/Domain")


#adding Payload Args
parser.add_argument("-PF", "--PayloadFile", help = "Paylods File path", type=str)

# Adding headers
parser.add_argument("-H", "--header", help = "Adding custom Headers", type=str, nargs='+')

#adding Completeness/Recursive Arguments
parser.add_argument("-R", "--Recursive", help="to execute ith script Recursively on the Website", action="store_true")
parser.add_argument("-d", "--depth", help="depth of Recursion", type=int)
parser.add_argument("-v", "--Verbose", help="to show Verbose Output", action="store_true")
parser.add_argument("--dynamic", help="to use the Dynamic approach for testing Dynamic Web Pages", action="store_true")

# Read arguments from command line
args = parser.parse_args()

MaxDepth=3
Recursive=False
Verbose=False
dynamicApproach=False

BaseUrls=[]
payloads=[]

if args.URLFile:
	try:	
		with open(args.URLFile,"r") as file:
			for line in file:
				if line != "\n" and line != "":
					#print(" '"+line.strip("\n")+"'")
					BaseUrls.append("http://"+UrlToDomain(line.strip("\n")))
	except FileNotFoundError:
		print("File not found ")
		exit(0)
	except:
		print("some error related to the input URL file occured \n Exiting")
		exit(0)
	#print(BaseUrls)
elif args.Url:
	if args.Url == UrlToDomain(args.Url):
		Url = "http://"+args.Url
	BaseUrls = Url.split()
	#print(BaseUrls)
else:
	print("No Args Passwd for URL")
	print("Use -h flag for detailed Help ")
	exit(0)



if args.PayloadFile:
	try:
		with open(args.PayloadFile,"r") as file:
			for line in file:
				payloads.append(line.strip("\n"))

	except FileNotFoundError:
		print("No Such File Found")
		print("QUITTING!!")
		exit(0)
	except:
		print("some error occured")
		exit(0)


if args.Recursive:
	print("Recursive Approach")
	Recursive = True
	if args.depth:
		MaxDepth = args.depth
		print("Max Recursion Depth = ",MaxDepth)
else:
	print("**Recursive Flag not Set**")
	print("Thus only scanning the provided URL excluding the Internal Links")



if args.Verbose:
	Verbose = True



if args.dynamic:
	dynamicApproach=True
#input Argument Parsing
#---------------------------------------------------------------------------------------

#defining the Payloads if not entered by the user
if payloads == []:
	print("\n**NO PAYLOAD FILE SPECIFIED**,\nUsing Default Payloads")
	#sleep(1)
	payloads=[
		'<script>alert(1);</script>',
		'<script>alert(document.cookie);</script>',
	]

headers = {}
if args.header:
	try:
		for i in args.header:
			# print(i)
			headers[i.split(":")[0]] = i.split(":")[1].strip()
	except:
		pass
	print("headers set => ",headers)
