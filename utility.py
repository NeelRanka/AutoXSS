from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin,urlparse, parse_qsl

session = HTMLSession()

def UrlToDomain(url):
	from tld import get_fld
	domain_name = url
	try:
		domain_name = get_fld(url)
	except:
		pass
	#print('-------------------------------------')
	#print("Domain Name is: "+domain_name)
	return(domain_name)


def isRequestType(link):
	# print(link)
	urlDetails = urlparse(link)
	# print(urlDetails)
	if urlDetails.query != "":
		paramDetails = parse_qsl(urlDetails.query,keep_blank_values=True)
		# print(paramDetails)
		DS = {}
		DS['action'] = urlDetails.path.strip("/")
		DS['method'] = 'get'
		DS['inputs'] = []
		for param in paramDetails:
			DS['inputs'].append( { 'type':"text", 'name':param[0], 'value':param[1] } )
		return(True,DS)
	return(False,None)


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


def fetchFormAndLinksStatic(url):
	#print(url)
	try:
		resp = session.get(url)
	except KeyboardInterrupt:
		exit(0)
	except:
		return(None,None)
	
	formSoup = BeautifulSoup(resp.html.html, "html.parser")
	linkSoup = BeautifulSoup(resp.text, 'html.parser')

	return( parseHTML(formSoup, linkSoup, url) )


def fetchFormAndLinksDynamic(driver, url):
	#print(url)
	try:
		driver.get(url)
		resp = driver.page_source

	except KeyboardInterrupt:
		exit(0)
	except:
		return(None,None)
	
	formSoup = BeautifulSoup(resp, "html.parser")
	linkSoup = BeautifulSoup(resp,'html.parser')

	return( parseHTML(formSoup, linkSoup, url) )




#fetch all the forms from the Given URL If Valid
def parseHTML(formSoup, linkSoup, url):
	urls=[]
	all_forms=[]
	#UrlLength = len(url)
	originalDomain = UrlToDomain(url)
	#print("Original Domain is : ",originalDomain)
	for links in linkSoup.find_all('a'):
		href = links.get('href')
		if href == "" or href == None:
			continue
		href = urljoin(url,UrlToDomain(href))
		#check for internal or external Link before adding to the list
		if originalDomain == UrlToDomain(href) and url != href:
			if isFile(href):
				continue
			#check if it is a link for a GET request??  eg abc.com/search.php?q=searchString   => if yes then parse it accordingly
			flag, value = isRequestType(href)
			if flag == True:
				all_forms.append(value)
				continue
			#if not a file then 
			urls.append(href)    #href is a complete link with domain name, route and extension if present

	forms = formSoup.find_all("form")
	for form in forms:
		form_details = get_form_details(form)
		if form_details!={}:
			all_forms.append(form_details)
	# print("all forms in parseHTML",all_forms)
	return(all_forms, urls)


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


def log(url,success,fail,file):
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
	
	file.write("\n\t\t\t---------------------------------------------------------------\n\n")


def logSummary(file,BaseUrl,totalInjections,successfulInjections,failedInjections,totalInjectionPoints):
	file.write("Domain : "+UrlToDomain(BaseUrl)+"\n")
	file.write("Total Injection Points : "+ str(totalInjectionPoints)+"\n")
	file.write("Total Injections Attempted : "+str(totalInjections)+"\n")
	file.write("Successful Injections : "+str(successfulInjections)+"\n")
	file.write("Failed Injections : "+str(failedInjections)+"\n")
	file.write("\n--------------------------------------------------------------------------------------------------------------------\n\n")

from termcolor import colored
def printGreen(string):
	print(colored(string, 'green'))

def printRed(string):
	print(colored(string, 'red'))