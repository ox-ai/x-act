



from fuzzywuzzy import fuzz
from typing import List, Dict

def string_search(promt: str, data_list: List[str]) -> Dict[str, List]:
    """
    Performs exact and fuzzy string search against a list of strings and ranks
    the results based on relevance.

    Args:
        promt (str): The promt string.
        data_list (List[str]): List of strings to search against.

    Returns:
        Dict[str, List]: A dictionary containing indices, matched data, and scores.
    """
    results = []

    for i, data_str in enumerate(data_list):
        if promt == data_str:  
            score = 100  # Exact match gets highest score
        else:
            score = max(
                fuzz.ratio(promt, data_str),
                fuzz.partial_ratio(promt, data_str),
                fuzz.token_sort_ratio(promt, data_str),
                fuzz.token_set_ratio(promt, data_str)
            )

        results.append((i, data_str, score))

    # Sort results by score (descending)
    results.sort(key=lambda x: x[2], reverse=True)

    # Single loop to construct return dictionary
    res = {"idx": [], "data": [], "score": []}
    for i, d, sc in results:
        res["idx"].append(i)
        res["data"].append(d)
        res["score"].append(sc / 100)

    return res