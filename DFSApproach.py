from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import deque
from urllib.parse import urljoin
from utility import *
from input import payloads,Recursive
import requests


visited={}
MaxDepth=0

def DFS(BaseUrls, payloads,specifiedDepth):

	def CheckXSS(BaseUrl,depth):
		global MaxDepth,visited

		if depth>=MaxDepth or BaseUrl in visited :  #already visited Url or greater than MaxDepth
			return()

		visited[BaseUrl] = 1

		forms,links = get_all_forms_and_links(BaseUrl)    #links has a list of websote Links found on that site
		if forms==None and links==None:
			print("Error with the Provided URL (Not Reachable) (TRY changing Protocol http/https ) ")
			return()

		#for i in links:
		#	print(i)

		all_forms=[]

		for i, form in enumerate(forms, start=1):
			form_details = get_form_details(form)
			all_forms.append(form_details)

		print("\nChecking link ",BaseUrl)
		try:
			for form in all_forms:
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
					#print("creating payload")
					data = create_data(inputs, payload)
					#print("created payloads")
					#create Data for the Form/Query string

					if form['method'] == 'get':
						#print("sent get req")
						resp = requests.get(url, params=data)
						#print("received get resp")
					elif form['method'] == 'post':
						#print("sent post req")
						resp = requests.post(url, data=data)
						#print("received post req")

					#print("Payload created")

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
				for link in links:
					CheckXSS(link,depth+1)

		except KeyboardInterrupt:
			print("\nLet me Log First\nQUITTING!")
			log(url,success,fail,file)
			file.close()
			exit(0)
		except:
			print("out due to exception")
			return()


	global MaxDepth
	MaxDepth = specifiedDepth
	for BaseUrl in BaseUrls:
		print("\t******",BaseUrl,"*******")
		file = open("./Results/result_"+BaseUrl.replace(".","_").split("/")[-1]+".log","w")
		CheckXSS(BaseUrl,1)
		file.close()
