# 迪克斯特拉算法： 计算加权图中的最短路径
# graph: 起点start，a,b,终点fin之间的距离
graph = {}
graph["start"] = {}
graph["start"]["a"] = 6
graph["start"]["a"] = 2
graph["a"] = {}
graph["a"]["fin"] = 1
graph["b"] = {}
graph["b"]["a"] = 3
graph["b"]["fin"] = 5
graph["fin"] = {}
# costs: 起点到 a,b,fin的开销
infinity = float("inf")
costs = {}
costs["a"] = 6
costs["b"] = 2
costs["fin"] = infinity
# parents： 存储父节点，记录最短路径
parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["fin"] = None
# processed: 记录处理过的节点，避免重复处理
processed = []


# find_lowest_cost_node(costs): 返回开销最低的点
def find_lowest_cost_node(costs):
    lowest_cost = float("inf")
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


# Dijkstra implement
node = find_lowest_cost_node(costs)
while node is not None:
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys():
        new_cost = cost + neighbors[n]
        if costs[n] > new_cost:
            costs[n] = new_cost
            parents[n] = node
    processed.append(node)
    node = find_lowest_cost_node(costs)

print(processed)
