import numpy as np
from sentence_transformers import SentenceTransformer, util


class BibleIndex:
    def __init__(self, testament: str = "all") -> None:
        self.model = SentenceTransformer(
            "sentence-transformers/msmarco-bert-base-dot-v5"
        )

        match testament:
            case "all" | "old" | "new":
                self.testament = testament
            case _:
                print("error:")

        self.load_emb()
        self.load_text()

    def load_emb(self) -> None:
        self.emb = np.load(f"data/embeddings/{self.testament}_esv_embeddings.npy")

    def load_text(self) -> None:
        text_path = f"data/text/{self.testament}_testament_esv.txt"

        with open(text_path, "r") as f:
            self.text = f.readlines()[1:]

    def query(self, query: str = "", top_n: int = 10):
        query_emb = self.model.encode(query)
        scores = util.dot_score(query_emb, self.emb)[0].cpu().tolist()

        # Combine docs & scores
        doc_score_pairs = list(zip(self.text, scores))

        # Sort by decreasing score
        doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

        # Output passages & scores
        print("Query:", query)
        results = []
        for doc, score in doc_score_pairs[:top_n]:
            text_split = doc.split(",")
            results.append(
                {
                    "src": f"{text_split[0]} {text_split[1]}:{text_split[2]}",
                    "text": ",".join(text_split[3:])
                    .replace("\xa0", "")
                    .replace("\n", ""),
                    "score": score,
                }
            )
        return results
