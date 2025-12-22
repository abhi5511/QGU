import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os

def run_mind_simulation():
    print("🧠 QGU MIND SIMULATION: MEMORY AS FLOW...")
    print("   Testing: Can a fluid network 'learn' a path simply by use?")

    # --- 1. SETUP THE "LIQUID BRAIN" ---
    # Create a random graph of "Neurons"
    num_neurons = 20
    G = nx.erdos_renyi_graph(num_neurons, 0.3, seed=42)
    
    # Assign "Resistance" to each connection (Edge)
    # Initially, all paths are hard (High Resistance)
    for u, v in G.edges():
        G[u][v]['resistance'] = 1.0
        G[u][v]['flow_count'] = 0

    # Layout for visualization
    pos = nx.spring_layout(G, seed=42)

    # --- 2. THE LEARNING PHASE (TRAINING) ---
    # Hum ek specific Input -> Output path ko baar-baar trigger karenge
    start_node = 0
    end_node = num_neurons - 1
    
    print(f"   Training: Sending signals from Node {start_node} to Node {end_node}...")
    
    # QGU LEARNING RULE: "Erosion"
    # Every time flow passes, Resistance decreases (Path gets wider)
    learning_rate = 0.05
    iterations = 50
    
    path_history = []
    
    for i in range(iterations):
        try:
            # Find the path of least resistance (Shortest weighted path)
            # Weight = Resistance
            path = nx.shortest_path(G, source=start_node, target=end_node, weight='resistance')
            path_history.append(path)
            
            # Reinforce the path (Hebb's Law / Flow Erosion)
            for j in range(len(path) - 1):
                u, v = path[j], path[j+1]
                # Reduce resistance (Widen the pipe)
                # Minimum resistance is 0.1 (Cannot be zero)
                G[u][v]['resistance'] = max(0.1, G[u][v]['resistance'] - learning_rate)
                G[u][v]['flow_count'] += 1
                
        except nx.NetworkXNoPath:
            print("   No path found!")
            break

    # --- 3. VISUALIZATION (The Scan) ---
    plt.figure(figsize=(10, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor='#111111')

    # Draw all edges (Faint lines = Unused connections)
    nx.draw_networkx_edges(G, pos, edge_color='#333333', alpha=0.3, width=1)
    
    # Draw "Learned" edges (Thick & Bright = Strong Memory)
    edges = G.edges(data=True)
    
    # Filter only edges that have flow history
    learned_edges = [(u, v) for u, v, d in edges if d['flow_count'] > 0]
    
    # Width depends on how many times flow passed (Memory Strength)
    weights = [d['flow_count'] * 0.8 for u, v, d in edges if d['flow_count'] > 0]
    
    if learned_edges:
        nx.draw_networkx_edges(G, pos, edgelist=learned_edges, width=weights, edge_color='cyan', alpha=0.9)
    
    # Draw Nodes
    node_colors = ['#555555'] * num_neurons
    node_colors[start_node] = '#00ff00' # Input (Green)
    node_colors[end_node] = '#ff00ff'   # Output (Magenta)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300)
    
    # Labels
    plt.title("QGU BRAIN: EMERGENT MEMORY PATHS", color='white', fontsize=14)
    plt.text(0.5, 0.02, "CYAN PATHS = MEMORY (Low Resistance Flow Channels)\nGREY PATHS = FORGOTTEN (High Resistance)", 
             color='white', ha='center', transform=ax.transAxes)
    
    plt.axis('off')
    
    # Save
    if not os.path.exists("figures"): os.makedirs("figures")
    save_path = "figures/qgu_mind_proof.png"
    plt.savefig(save_path, facecolor='#111111')
    print(f"📸 Brain Scan Generated: {save_path}")
    plt.show()

if __name__ == "__main__":
    run_mind_simulation()