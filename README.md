'grid.py' reads geographic info from 'grid_clean.xlsx'. Given starting and distination points, the script computes the least cost route by Dijkstra's algorithm.
Travelling costs use parameters from Langmuir (1984). The best route is marked by 'mark ==1' in the output file 'grid_result.csv'.

Environment: Python3.7  pandas 1.2.4

Reference:

Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

Langmuir, Eric. Mountaincraft and leadership: a handbook for mountaineers and hillwalking leaders in the British Isles. Edinburgh: Scottish Sports Council, 1984.
