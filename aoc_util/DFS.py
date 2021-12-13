def find_all_paths(cave, source, target, history, visit_small_caves_once):
    path_count = 0  # Start with no path options

    # If a lowercase node is already double-visited, turn that parameter off for the rest of this path
    if not visit_small_caves_once and max(history.count(x) for x in history if x.islower()) == 2:
        visit_small_caves_once = True

    # Find possible next nodes to visit
    if visit_small_caves_once:
        next_nodes = [n for n in cave[source] if n.isupper() or n not in history]  # Don't double-visit lowercase nodes
    else:
        next_nodes = [n for n in cave[source] if n != 'start']  # Can double-visit lowercase nodes

    # Keep going down each path option
    for node in next_nodes:
        if node == target:
            path_count += 1
        else:
            # Find paths from next node to end
            path_count += find_all_paths(cave, node, 'end', history + [node], visit_small_caves_once)

    return path_count
