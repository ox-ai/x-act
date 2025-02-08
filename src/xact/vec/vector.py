from typing import List, Optional, Dict
import numpy as np

from xact.config.gen import config
from xact.llm.embed import Embedder



class VectorModel:
    def __init__(self,embed_model:str=config.XACT_LLM_EMBEDDING_MODEL) -> None:
        """
        Initializes the Model class with the default sentence transformer model.
        """
        self.md_name = embed_model
        self.model = Embedder(model=self.md_name)
        

    def generate(self, data:list,model:str=config.XACT_LLM_EMBEDDING_MODEL):
        """
        Encodes the input data into embeddings using the loaded model.

        Args:
            data: The data to be encoded, typically a list of strings.

        Returns:
            A list of embeddings corresponding to the input data.
        """
        embeddings = self.model.generate(data,model=model)
        embd_out = []
        for embed in embeddings.data:
            embd_out.append(embed.embedding)
        return embd_out


    def search(self, query_embed: str|List[int],  data: Optional[List[str]] = [],data_embed: Optional[List[List[int]]] = [], by: Optional[str] = config.SIM_FORMAT,include : Optional[List[str]]=[]) -> Dict[str, List]:
        """
        Searches for the most similar documents to the query based on the specified similarity metric.

        Args:
            query (str): The query string to search for.
            data_embed (list, optional): Precomputed embeddings for the documents. Defaults to an empty list.
            data (list, optional): Raw document data that needs to be encoded. Defaults to an empty list.
            by (Optional[str], optional): The similarity metric to use. Defaults to "dp".
                - "dp" : Dot Product (default)
                - "ed" : Euclidean Distance
                - "cs" : Cosine Similarity
            include (Optional[List[str]],optional): return data format
                - "emdeds" : embeddings of the data


        Returns:
            dict[str, List]: A dictionary containing the indices, similarity scores, document data, and embeddings of the top results.
        """
        # Validate the search method
        if by not in config.SIM_FORMATS:
            raise ValueError(f"Invalid search method '{by}'. Must be one of {config.SIM_FORMATS}.")

        if isinstance(query_embed,str):
            # Generate embeddings for the query
            query_embed = np.array(self.generate([query_embed]))[0]
        elif isinstance(query_embed,list):
            # Generate embeddings for the query
            query_embed = np.array(query_embed)
        



        if len(data_embed) > 0:
            data_embed = np.array(data_embed)
        elif len(data) > 0:
            # Generate embeddings for the documents if raw data is provided
            data_embed = np.array(self.generate(data))
        else:
            return {"idx": [], "sim_score": [], "data": [], "data_embed": []}

        # Vectorized similarity calculations
        if by == "dp":
            sim = np.dot(data_embed, query_embed.T)
        elif by == "cs":
            sim = np.dot(data_embed, query_embed.T) / (np.linalg.norm(data_embed, axis=1) * np.linalg.norm(query_embed))
        elif by == "ed":
            sim = np.linalg.norm(data_embed - query_embed, axis=1)

        # Get top N indices and their similarity scores
        if by == "ed":
            idx = np.argsort(sim)  # For Euclidean distance, lower distance is more similar
        else:
            idx = np.argsort(sim)[::-1]  # For Dot Product and Cosine Similarity, higher is more similar

        idx = idx.tolist()
        sim_score = sim[idx].tolist()

        # Reorder data and embed based on the sorted indices
        data_sorted = []
        if len(data) > 0:
            data_sorted = [data[i] for i in idx]
        data_embed_sorted = []
        if "data_embed" in include:
            data_embed_sorted = [data_embed[i].tolist() for i in idx]

        return {
            "idx": idx,
            "score": sim_score,
            "data": data_sorted,
            "data_embed": data_embed_sorted
        }

    @staticmethod
    def sim( veca, vecb, sim_format: Optional[str] = config.SIM_FORMAT):
        """
        Calculates the similarity between two vectors based on the specified format.

        Args:
            veca: The first vector.
            vecb: The second vector.
            sim_format (Optional[str], optional): The similarity metric to use. Defaults to "dp".
                - "dp" : Dot Product (default)
                - "ed" : Euclidean Distance
                - "cs" : Cosine Similarity

        Returns:
            The similarity value between the two vectors based on the chosen format.
        """
        if sim_format not in config.SIM_FORMATS:
            raise ValueError(
                f"ox-db: sim_format should be one of {config.SIM_FORMATS}, not {sim_format}"
            )

        veca = np.array(veca)
        vecb = np.array(vecb)

        if sim_format == "dp":
            return np.dot(veca, vecb)
        if sim_format == "ed":
            return np.linalg.norm(veca - vecb)
        elif sim_format == "cs":
            return np.dot(veca, vecb) / (np.linalg.norm(veca) * np.linalg.norm(vecb))