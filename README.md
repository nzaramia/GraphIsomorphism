# Heading
Graph Isomorphism Using a Tree-mapping Approach

Nancy Zaramian
January 29, 2022
Abstract
The graph isomorphism problem asks whether two graphs are essen-
tially the same. Researchers have been looking for a polynomial-time
solution for it for many decades. This paper provides an algorithm for
the problem using a tree-mapping approach. It converts the two graphs
into trees and matches them to provide a mapping. The algorithm
also ensures that the conversion and the mapping run in polynomial-
time by pruning the tree appropriately as it is built. Experiments are
done on the ARG Database [9][7] and the results show that all iso-
morphisms for graphs with bounded degree were found in a reasonable
time. As expected, the results also show that as the average degree of
vertices in the graph increases so does the running time. An analysis of
the algorithm indicates that the conversion and mapping both run in
polynomial-time regardless of the average vertex degree of the graph.
