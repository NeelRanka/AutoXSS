from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import deque
from urllib.parse import urljoin
from utility import *
from input import payloads,Recursive,MaxDepth
import requests

visited={}
currentDomainLinks = deque([])
driver=None
file=None


def CheckXSS(BaseUrl,depth,DFS):
	global visited,driver
	if depth>=MaxDepth :  #already visited Url or greater than MaxDepth
		print("reached max depth")
		return()

	visited[BaseUrl] = 1

	forms,links = fetchFormAndLinksDynamic(driver, BaseUrl)    #links has a list of websote Links found on that site
	if forms==None and links==None:
		print("Error with the Provided URL (Not Reachable) (TRY changing Protocol http/https ) => ",BaseUrl)
		return()

	all_forms=[]

	for i, form in enumerate(forms, start=1):
		form_details = get_form_details(form)
		all_forms.append(form_details)

		
	#print("------------------Testing URL : ",BaseUrl,"------------------")
	print("\nChecking link ",BaseUrl)
	#input(all_forms)
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
				#print("creating payloads")
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
			log(url,success,fail,file)

			#checks if the Recursive flag is set or not
		if Recursive:
			if DFS:
				for link in links:
					CheckXSS(link,depth+1,DFS)			
			else:
				global currentDomainLinks
				currentDomainLinks.append(  ( links, depth+1 )  ) #modify to append only non visited links


	except KeyboardInterrupt:
		print("\nLet me Log First\nQUITTING!")
		log(url,success,fail,file)
		file.close()
		exit(0)
	except Exception as e:
		print("Out of exception	",e)
		return()



def BFS_Dynamic(BaseUrls,payloads,specifiedDepth):

	global currentDomainLinks, MaxDepth, driver, file
	MaxDepth = specifiedDepth

	for BaseUrl in BaseUrls:
		driver = webdriver.Chrome('./chromedriver') 
		print("\t******",BaseUrl,"*******")
		file = open("./Results/result_"+BaseUrl.replace(".","_").split("/")[-1]+".log","w")
		
		currentDomainLinks = deque([([BaseUrl],0)]) #=> tuple(list_Of_Urls, depth)
		
		counter=0
		while counter < len(currentDomainLinks):
			#print("=>",currentDomainLinks[counter])
			Urls = currentDomainLinks[counter][0] 
			depth = currentDomainLinks[counter][1]
			counter+=1
			
			for Url in Urls:
				if Url not in visited:
					CheckXSS(Url,depth,False)
		
		file.close()
		driver.close()




def DFS_Dynamic(BaseUrls, payloads,specifiedDepth):

	global MaxDepth, driver, file  #just to share the data between functions
	MaxDepth = specifiedDepth
	for BaseUrl in BaseUrls:
		driver = webdriver.Chrome('./chromedriver')
		print("\t******",BaseUrl,"*******")
		file = open("./Results/result_"+BaseUrl.replace(".","_").split("/")[-1]+".log","w")
		CheckXSS(BaseUrl,1,True)
		driver.close()
		file.close()