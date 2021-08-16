# AI lab4

## Project Grade: 90%
#######(A slightly better implementation of LDS could be used).
In the first part, we implemented a solution for solving the MultiKnapsack problem.
We use the Limited Depth Search algorithm (LDS) with two heuristics:
- Branch and Bound.
- LP-relaxation.

The second part is solving the Capacitated Vehicle Routing Problem (CVRP) using two methods:
- Method1: Devide the cities into groups for each vehicle using the MultiKnapsack algorithm in part1 and then optimizing the internal route (TSP) using the Tabu search.
- Method2: using the NSGA algorithm with a multi-objective function. 
##
A thorough report was conducted and can be found in the 'documents' folder.