from input import BaseUrls,payloads,Recursive,MaxDepth,Verbose,dynamicApproach


#from BFSApproach import BFS_Static   #level wise approach
#from DFSApproach import DFS_Static   #goes depp down in a single path

from static import BFS_Static, DFS_Static
from dynamic import BFS_Dynamic, DFS_Dynamic


if MaxDepth <=3 :
	print("Using the BFS approach for depth is <=3")
	#option for Static or Dynamic
	if dynamicApproach:
		BFS_Dynamic(BaseUrls,payloads,MaxDepth)

	BFS_Static(BaseUrls,payloads,MaxDepth)
	
else:
	print("Using the DFS approach")
	#option for Static or Dynamic
	if dynamicApproach:
		DFS_Dynamic(BaseUrls,payloads,MaxDepth)

	DFS_Static(BaseUrls,payloads,MaxDepth)
	