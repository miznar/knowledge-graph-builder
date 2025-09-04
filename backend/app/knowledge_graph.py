from pyvis.network import Network
import os
import spacy
from nltk.corpus import stopwords
from .ingest import chunk_text, extract_text_from_pdf

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

# Define colors for entity types
ENTITY_COLORS = {
    "PERSON": "green",
    "ORG": "blue",
    "GPE": "purple",   # Countries, cities, etc.
    "LOC": "orange",   # Locations
    "DATE": "red",
    "DEFAULT": "gray"
}

def build_knowledge_graph(pdf_path, output_file="graph.html"):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.force_atlas_2based()  # Better layout
    net.repulsion(node_distance=200, central_gravity=0.2)

    edges = set()   # Store edges to avoid duplicates
    nodes = set()   # Track nodes

    for chunk in chunks:
        doc = nlp(chunk)

        # Extract named entities
        entities = [(ent.text.strip(), ent.label_) for ent in doc.ents if ent.text.strip()]

        # Fallback: use keywords (filtered tokens, first 5 only)
        keywords = [
            (token.text.strip(), "KEYWORD")
            for token in doc
            if token.is_alpha and token.text.lower() not in stop_words
        ][:5]

        candidates = entities + keywords

        # Add nodes + edges
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                src, src_type = candidates[i]
                dst, dst_type = candidates[j]

                if src != dst and (src, dst) not in edges and (dst, src) not in edges:
                    # Node color + tooltip
                    src_color = ENTITY_COLORS.get(src_type, ENTITY_COLORS["DEFAULT"])
                    dst_color = ENTITY_COLORS.get(dst_type, ENTITY_COLORS["DEFAULT"])

                    if src not in nodes:
                        net.add_node(
                            src,
                            label=src,
                            title=f"Entity: {src}<br>Type: {src_type}<br>Source: PDF chunk",
                            color=src_color
                        )
                        nodes.add(src)

                    if dst not in nodes:
                        net.add_node(
                            dst,
                            label=dst,
                            title=f"Entity: {dst}<br>Type: {dst_type}<br>Source: PDF chunk",
                            color=dst_color
                        )
                        nodes.add(dst)

                    net.add_edge(src, dst, title="Co-occurrence in text")
                    edges.add((src, dst))

    # Save HTML file inside app/static/graphs/
    os.makedirs("app/static/graphs", exist_ok=True)
    output_path = os.path.join("app/static/graphs", output_file)
    net.save_graph(output_path)

    return output_path
