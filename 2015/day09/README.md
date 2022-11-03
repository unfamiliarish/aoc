# scribbles and notes

this is the traveling salesman problem
i could write a brute force solution, also apparently called the naive solution

i thought that all cities connected to each other (in hindsight it makes sense that they don't), and that the complexity of brute force would be O(n!)
it's not though, because this is essentially a graph, yes, so you'd instead brute force through all possible paths, branching from each node

ok, no the complexity would probably still be O(n!) or so, because you'd have to try every possible path, from every possible starting node 

i don't remember the solution to the TSP, but i'm not going to look it up, because fighting it for a while first will make it stick more

this is more complex than the shortest path from start node to end node, which can be handled with a hash table (i think)

i'm confused about how to do this without using brute force 

this is np-complete, i looked it up

### potential solution (broken)
steps:
* loop through paths and find the shortest one 
* store path, repeat, always taking the smallest edges connected to the nodes

i went looking fdor examples, and turns out this is sort of it

for a complete graph, set up a matrix of all the connected edges, and then just find the shortest distance between nodes 

steps:
* choose a node
* for all paths from that node, choose the shortest one 
* from the new node, choose the shortest path without visiting an already-visited node
* repeat
* sum

i am curious about whether this works for an incomplete graph

the answer is no, this example does a good illustration of it
https://miro.medium.com/max/665/1*WG9lvtclY3lp2r5LNNZyfQ.png

ok wait
what if
somehow
we start with some node

no wait, i think it remember how this works 
no that's djikstra's, and i don't think that works for TSP

this isn't exactly the traveling salesman problem, because he only has to visit every node exactly once 

he doesn't need to make a full loop 

one of the destinations has no out paths, but that feels odd to use that to restrict the solution to the problem 
like, i could, but also then i would be writing my solution to a specific use case 
but also that is the point of advent of code , find a solution and find it quick 

