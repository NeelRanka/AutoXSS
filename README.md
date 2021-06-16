# AutoXSS
Automated Tool for Detecting Reflected XSS

To run,  
  python3 main.py [options]  
  
  options:  
    -U <URL> : Url to scan for (with the protocol http/https)  
    -UF <File Path> : URL file path for multiple URLS sequentially  
    -R  :to specify a recursive approach  
    -d <number> to specify depth of recursion (default 3)  
    -PF <File Path> : payload file  
