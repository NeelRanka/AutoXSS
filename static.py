from collections import deque
from urllib.parse import urljoin
from utility import *
from input import payloads,Recursive,MaxDepth,Verbose
import requests

visited={}
currentDomainLinks = deque([])
file = None
totalInjections=0
totalInjectionPoints=0
successfulInjections=0
failedInjections=0


def CheckXSS(BaseUrl,depth,DFS):
	global visited,file,totalInjectionCount
	if depth>=MaxDepth :  #already visited Url or greater than MaxDepth
		#print("reached max depth")
		return()

	visited[BaseUrl] = 1

	forms,links = fetchFormAndLinksStatic(BaseUrl)    #links has a list of websote Links found on that site
	if forms==None and links==None:
		print("Error with the Provided URL (Not Reachable) (TRY changing Protocol http/https ) => ",BaseUrl)
		return()

	all_forms=[]

	for i, form in enumerate(forms, start=1):
		form_details = get_form_details(form)
		if form_details!={}:
			all_forms.append(form_details)

		
	#print("------------------Testing URL : ",BaseUrl,"------------------")
	if Verbose:
		print("\nChecking link ",BaseUrl, "with forms : ")
		for form in all_forms:
			if "action" in form:
				print("\t",form["action"])
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

			print("\n==> ",url)
			global totalInjections,successfulInjections,failedInjections,totalInjectionPoints
			totalInjectionPoints+=1
			success=[]
			fail=[]
			for payload in payloads:
				#print("creating payloads")
				data = create_data(inputs, payload)

				#create Data for the Form/Query string
				totalInjections+=1
				if form['method'] == 'get':
					resp = requests.get(url, params=data)
				elif form['method'] == 'post':
					resp = requests.post(url, data=data)


				if payload in resp.text:
					printGreen("\t"+url+"\t[+] Success with payload "+ payload)
					successfulInjections+=1
					success.append(payload)
				else:
					printRed("\t "+url+" \tFailure" + payload)
					failedInjections+=1
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
		logSummary(file,BaseUrl,totalInjections,successfulInjections,failedInjections,totalInjectionPoints)
		file.close()
		exit(0)
	except Exception as e:
		print("Out of exception	",e)
		return()


def BFS_Static(BaseUrl):
	global currentDomainLinks
	
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


def DFS_Static(BaseUrl):
	CheckXSS(BaseUrl,1,True)
	

def staticWrapper(BaseUrls, payloads, specifiedDepth, DFS):
	global MaxDepth,file,totalInjections,totalInjectionPoints,successfulInjections,failedInjections
	MaxDepth = specifiedDepth
	for BaseUrl in BaseUrls:
		print("\t******",BaseUrl,"*******")
		file = open("./Results/result_"+BaseUrl.replace(".","_").split("/")[-1]+".log","w")
		
		try:
			if DFS:
				DFS_Static(BaseUrl)
			else:
				BFS_Static(BaseUrl)
		except KeyboardInterrupt:
			print("\nLet me Log First\nQUITTING!")
			log(url,success,fail,file)
			logSummary(file,BaseUrl,totalInjections,successfulInjections,failedInjections,totalInjectionPoints)
			file.close()
		except Exception as e:
			print("Some error occured ",e)
			exit(0)

		logSummary(file,BaseUrl,totalInjections,successfulInjections,failedInjections,totalInjectionPoints)
		
		if totalInjectionPoints == 0 or totalInjections == 0:
			print("Sorry, Nothing Found ")

		totalInjections=0
		totalInjectionPoints=0
		successfulInjections=0
		failedInjections=0

		print("Logging Complete")
		file.close()
