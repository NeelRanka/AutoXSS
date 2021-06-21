from input import BaseUrls,payloads,Recursive,MaxDepth,Verbose,dynamicApproach


#from BFSApproach import BFS_Static   #level wise approach
#from DFSApproach import DFS_Static   #goes depp down in a single path

from static import staticWrapper
from dynamic import dynamicWrapper


if MaxDepth <=3 :
	print("Using the BFS approach for depth is <=3")
	DFS=False

	if dynamicApproach: #flag set by User
		dynamicWrapper(BaseUrls,payloads,MaxDepth,DFS)
	else:
		staticWrapper(BaseUrls,payloads,MaxDepth,DFS)
	
	print("\n\tSCAN COMPLETE")
else:
	print("Using the DFS approach")
	DFS=True

	if dynamicApproach: #flag set by User
		dynamicWrapper(BaseUrls,payloads,MaxDepth,DFS)
	else:
		staticWrapper(BaseUrls, payloads, MaxDepth, DFS)
	
	print("\n\tSCAN COMPLETE")