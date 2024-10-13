from sentence_transformers import SentenceTransformer
import faiss
import os
from tqdm import tqdm

class CodebaseEmbeddings:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.file_paths = []
        self.build_index()

    def build_index(self):
        code_snippets = []
        print("Building code embeddings index...")
        for root, _, files in tqdm(list(os.walk('.')), desc="Scanning files"):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    code_snippets.append(content)
                    self.file_paths.append(file_path)

        embeddings = self.model.encode(code_snippets, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        print("Code embeddings index built successfully.")

    def search_relevant_code(self, query, k=5):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        return [self.file_paths[i] for i in indices[0]]
