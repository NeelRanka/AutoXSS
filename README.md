# AutoXSS
Automated Tool for Detecting Reflected XSS

Features:
	Provides Recursive scaning of a Web Application with a customizable Depth
	Containes a file having some Well-Known Payloads to check with

Requirments : Pip Modules
    bs4
    requests_html
    urllib.parse
    requests
    argparse
    time
    
    
Usage:
	#Make the Python Script Executable
	chmod +x AutoXSS
	
	#execute the Script
		#Help section
		./AutoXSS -h
		
		#Naive Scanning
		./AutoXSS -U <URL>
		
		#Recursive Scanning (Default depth is 3)
		./AutoXSS -U <URL> -R
		
		#Recursive Scanning with Custom Depth
		./AutoXSS -U <URL> -R -d <depth>
    
