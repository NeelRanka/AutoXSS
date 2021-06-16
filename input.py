import requests,argparse
from time import sleep

parser = argparse.ArgumentParser(description = "Reflected XSS Scanner Tool",
								 epilog="eg=> ./AutoXSS -U <URL>"
								 )
 
# Adding URL Arguments
URLGroup = parser.add_mutually_exclusive_group(required=True)
URLGroup.add_argument("-U", "--Url", help = "URL to Test On", type=str)
URLGroup.add_argument("-UF", "--URLFile", help="file input for multiple URL")


#adding Payload Args
parser.add_argument("-PF", "--PayloadFile", help = "Paylods File path", type=str)

#adding Completeness/Recursive Arguments
parser.add_argument("-R", "--Recursive", help="to execute ith script Recursively on the Website", action="store_true")
parser.add_argument("-d", "--depth", help="depth of Recursion", type=int)

# Read arguments from command line
args = parser.parse_args()

MaxDepth=3
Recursive=False
BaseUrls=[]
payloads=[]
if args.URLFile:
	try:	
		with open(args.URLFile,"r") as file:
			for line in file:
				BaseUrls.append(line.strip("\n"))
	except FileNotFoundError:
		print("File not found ")
		exit(0)
	except:
		print("some error related to the input URL file occured \n Exiting")
		exit(0)
	#print(BaseUrls)
elif args.Url:
	BaseUrls = args.Url.split()
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
