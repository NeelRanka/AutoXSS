#!/usr/bin/python3
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import requests,argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#python3 filename.py -U <URL> -F <Filename>

payloads=[]
Recursive = False
MaxDepth = 3
#--------------------------------------------------------------------------------
#Args Parsing
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


BaseUrls=[]
if args.URLFile:
	#print("Url Entered : % s" % args.Url)	
	with open(args.URLFile,"r") as file:
		for line in file:
			BaseUrls.append(line.strip("\n"))
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

session = HTMLSession()

#create a function isFile()
# to check if it is a file or a URL
files = ["pdf","pptx","xlsx","jpg","png","jpeg"]
def isFile(href):
	global files
	if href == None or len(href) == 0:
		return(True)  #ignore as blank

	href = href.split(".")
	extension = href[-1]
	if extension.lower() in files:
		return(True)
	return(False)


#fetch all the forms from the Given URL If Valid
def get_all_forms(url):
	try:
		#resp = session.get(url)
		driver.get(url)
		resp = driver.page_source
	except KeyboardInterrupt:
		exit(0)
	except:
		return(None,None)
	
	formSoup = BeautifulSoup(resp, "html.parser")
	linkSoup = BeautifulSoup(resp,'html.parser')
	urls=[]
	UrlLength = len(url)
	for links in linkSoup.find_all('a'):
		href = links.get('href')
		if href == "" or href == None:
			continue
		href = urljoin(url,href)
		#check for internal or external Link before adding to the list
		#need some better logic for Internal Links
		if url == href[:UrlLength] and url != href:
			if isFile(href):
				continue

			#if not a file then 
			urls.append(href)    #href is a complete link with domain name, route and extension if present

	return(formSoup.find_all("form"),urls)


#Create a Data Structure for storing the Form attributes
def get_form_details(form):   #=>    {action:value,    method:value,   inputs: list[{type:  ,name:  , value:  }]}
	details = {}
	try:
		action = form.attrs.get("action").lower()
		method = form.attrs.get("method", "get").lower()
		inputs = []
		for input_tag in form.find_all("input"):
			input_type = input_tag.attrs.get("type", "text")
			input_name = input_tag.attrs.get("name")
			input_value =input_tag.attrs.get("value", "")
			inputs.append({"type": input_type, "name": input_name, "value": input_value})
		details["action"] = action
		details["method"] = method
		details["inputs"] = inputs
	except:
		pass

	return(details)

#insert the data in the form
def create_data(inputs, payload):
	data = {}
	for input_tag in inputs:
		if input_tag['type'] == 'hidden':
			data[input_tag['name']] = input_tag['value']
		elif input_tag['type'] != 'submit':
			data[input_tag['name']] = payload
	return(data)


def log(url,success,fail):
	file.write("URL : "+url+"\n")
	##create a log file for the success and failures
	if success!=None and len(success)!=0:
		file.write("\tSuccess\n")
		for element in success:
			file.write("\t\t[+] "+element+"\n")

	if fail!=None and len(fail)!=0:
		file.write("\n\n\tFailures\n")
		for element in fail:
			file.write("\t\t"+element+"\n")
	
	file.write("\n------------------------------------------------------------------------------------------------------------------------\n\n\n")



def CheckXSS(BaseUrl,depth):
	global MaxDepth,visited

	if depth>=MaxDepth or BaseUrl in visited :  #already visited Url or greater than MaxDepth
		return()

	visited[BaseUrl] = 1

	forms,links = get_all_forms(BaseUrl)    #links has a list of websote Links found on that site
	if forms==None and links==None:
		print("Error with the Provided URL (Not Reachable) (TRY changing Protocol http/https ) ")
		return()
	#print(len(forms),len(links))
	#for i in links:
	#	print(i)

	all_forms=[]

	for i, form in enumerate(forms, start=1):
		form_details = get_form_details(form)
		all_forms.append(form_details)

	#input("----------------------------------------------------------------------------------------")

	#for form in all_forms:
	#	print(form,end='\n\n')
	#input()
	#print("------------------Testing URL : ",BaseUrl,"------------------")
	print("\nChecking link ",BaseUrl)
	try:
		for form in all_forms:
			#print("Checking forms",form)
			if "action" in form and "method" in form and "inputs" in form:
				action = form['action']    #check if the action has the BaseUrl
				method = form['method']
				inputs = form['inputs']
			else:
				print("form issue")
				print(form)
				#input()
				continue

			#print("==>",BaseUrl,action)
			url = urljoin(BaseUrl, action)
			if url in visited:
				#print("already visited this ",url)
				continue
			else:
				visited[url] = 1

			print("==> ",url)
			success=[]
			fail=[]
			for payload in payloads:
				print("creating payloads")
				data = create_data(inputs, payload)

				#create Data for the Form/Query string

				if form['method'] == 'get':
					resp = requests.get(url, params=data)
				elif form['method'] == 'post':
					resp = requests.post(url, data=data)


				if payload in resp.text:
					print("\t",url,"\t[+] Success with payload ", payload)
					success.append(payload)
				else:
					print("\t",url,"\tFailure")
					fail.append(payload)
					#print(resp.text)

			#append to log file
			log(url,success,fail)

		#checks if the Recursive flag is set or not
		if Recursive:
			for link in links:
				CheckXSS(link,depth+1)

	except KeyboardInterrupt:
		print("\nLet me Log First\nQUITTING!")
		log(url,success,fail)
		file.close()
		exit(0)
	except Exception as e:
		print("Out of exception	",e)
		return()



print("\n\nTHIS IS A TOOL AND IT IS RECOMMENDED TO PERFORM MANUAL TESTING FOR VERIFICATION\n\n")
sleep(2)
visited={}

#BaseUrl = "http://mescoepune.org"    #issue with dynamic website
for BaseUrl in BaseUrls:
	driver = webdriver.Chrome('./chromedriver') 
	print("\t******",BaseUrl,"*******")
	file = open("./Results/result_"+BaseUrl.replace(".","_").split("/")[-1]+".log","w")
	CheckXSS(BaseUrl,1)
	file.close()
	driver.close()


#_________________________________________________________________________________________
#completed the naive approach
#now try to find strings which match the payload and send such a string from the respnse which would couse and XSS vuln 

