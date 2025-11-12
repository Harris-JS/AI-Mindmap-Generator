# app.py — Structured Mindmap Layout Version
import streamlit as st
import networkx as nx
from pyvis.network import Network
from llm_extract import extract_concepts_with_llm
import random

# --- Streamlit page setup ---
st.set_page_config(page_title="🧠 AI Mindmap Generator", layout="wide")
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
            color: #000000;
        }
        .stTextArea textarea {
            background-color: #ffffff;
            color: #000000;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        .stButton>button {
            background-color: #ffb703;
            color: #000000;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #f48c06;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App Title and Description ---
st.title("🧠 AI-Based Mindmap Generator")
st.markdown(
    "This tool uses **AI (Hugging Face)** to extract the main idea and related sub-ideas, then visualizes them as a clean, centered **mindmap**."
)

# --- Input Text Area ---
text = st.text_area(
    "Enter your text here:",
    height=200,
    placeholder="Example: Artificial Intelligence is transforming industries like healthcare, finance, and education..."
)

# --- Generate Button ---
if st.button("✨ Generate Mindmap"):
    if not text.strip():
        st.warning("⚠️ Please enter some text to generate a mindmap.")
    else:
        with st.spinner("Extracting concepts... please wait ⏳"):
            data = extract_concepts_with_llm(text)

        if not data["nodes"]:
            st.error("❌ No concepts found. Try with a more detailed paragraph.")
        else:
            st.success("✅ Concepts extracted successfully!")

            # --- Create Graph ---
            G = nx.Graph()
            G.add_nodes_from(data["nodes"])
            G.add_edges_from(data["edges"])

            # --- Mindmap Center Logic ---
            main_node = data["nodes"][0]  # assume first concept = main topic
            sub_nodes = data["nodes"][1:] if len(data["nodes"]) > 1 else []

            # --- PyVis Network Setup ---
            net = Network(height="650px", width="100%", bgcolor="#ffffff", font_color="#000000")

            # Define color palette
            center_color = "#ffb703"  # yellow
            idea_color = "#219ebc"    # blue
            sub_color = "#8ecae6"     # light blue

            # Add main topic (center)
            net.add_node(main_node, label=main_node, color=center_color, size=40, shape="circle")

            # Add sub-ideas around the main topic
            for i, node in enumerate(sub_nodes):
                color = random.choice([idea_color, sub_color])
                net.add_node(node, label=node, color=color, size=25, shape="box")
                net.add_edge(main_node, node, color="#023047")

            # Create links between related ideas if edges exist
            for edge in data["edges"]:
                if edge[0] != main_node and edge[1] != main_node:
                    net.add_edge(edge[0], edge[1], color="#8ecae6", width=2)

            # --- Layout Configuration ---
            net.repulsion(
                node_distance=180,
                spring_length=300,
                damping=0.85,
            )

            html_str = net.generate_html()
            st.components.v1.html(html_str, height=650, scrolling=True)

# --- Footer ---
st.markdown("---")
st.caption("🧠 Built by **Harris Selvaraj J** | Designed with Python, Streamlit, and Hugging Face 🚀")
