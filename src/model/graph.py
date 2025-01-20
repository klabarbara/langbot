import json
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_graph(input_file="data/translation/translated_content.json"):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        headers = content.get("headers", [])
        paragraphs = content.get("paragraphs", [])

        # creates directed multigraph
        # ie: nodes can have multiple edges between them
        # this allows two nodes to have 'explains' and 'related_to' edges
        G = nx.MultiDiGraph() 

        # add headers and paragraphs as nodes
        for header in headers:
            G.add_node(header, type="header")
        for paragraph in paragraphs:
            G.add_node(paragraph, type="paragraph")

        # add "explains" edges
        for header, paragraph in zip(headers, paragraphs):
            G.add_edge(paragraph, header, relationship="explains")

        # compute "related_to" edges using text similarity
        if headers or paragraphs:
            all_texts = headers + paragraphs
            vectorizer = TfidfVectorizer().fit_transform(all_texts)
            similarity_matrix = cosine_similarity(vectorizer)

            for i, text_a in enumerate(all_texts):
                for j, text_b in enumerate(all_texts):
                    if i != j and similarity_matrix[i, j] > 0.3:
                        # adds a "related_to" edge regardless of existing edges
                        G.add_edge(text_a, text_b, relationship="related_to")

        print("Graph created successfully.")
        return G
    except Exception as e:
        print(f"Error creating graph: {e}")
        return None
