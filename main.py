from input import BaseUrls,payloads,Recursive,MaxDepth


from BFSApproach import BFS   #level wise approach
from DFSApproach import DFS   #goes depp down in a single path


if MaxDepth <=3 :
	print("Using the BFS approach for depth is <=3")
	BFS(BaseUrls,payloads,MaxDepth)
else:
	print("Using the DFS approach")
	DFS(BaseUrls,payloads,MaxDepth)