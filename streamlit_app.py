import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from searchAlgos import hospital_graph, locations, gbfs, a_star

st.set_page_config(page_title="Emergency Supply Robot - Search Visualizer", layout="wide")

st.title("Emergency Supply Robot: Informed Search Visualizer")
st.write(
    "Pick a start node, a goal node and a search algorithm (GBFS or A*). "
    "The app finds a path through the hospital corridors, highlights it on the "
    "graph and shows the total path cost."
)

nodes = list(hospital_graph.keys())

start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost = gbfs(start, goal)
    else:
        path, cost = a_star(start, goal)

    if path is None:
        st.error(f"No path found from {start} to {goal}.")

    else:
        # Build the NetworkX graph
        G = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations
        fig, ax = plt.subplots(figsize=(10, 6))

        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2200, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange", node_size=2200, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, node_size=2200, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3,
                               arrows=True, arrowsize=25, node_size=2200, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"), ax=ax)

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)

        # Results below the graph (as the lab requires)
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")