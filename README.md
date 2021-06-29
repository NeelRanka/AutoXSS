# AutoXSS
Automated Tool for Detecting Reflected XSS

To run,  
  python3 main.py [options]  
  
  options:  
    -U <URL> : Url/Domain to scan for  
    -UF <File Path> : URL/Domain file path for multiple URLs/Domains sequentially  
    -R  :to specify a recursive approach  
    -d <number> to specify depth of recursion (default 3)  
    -PF <File Path> : payload file  
    -v : Verbose output  
    --dynamic : to render dynamic webpages using selenium
