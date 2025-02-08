from typing import Optional, Dict, Any, List



from xact.data.data import DataX


class Chunker():

    def __init__(self,chunk_size:int=3000):
        self.chunk_size: int = chunk_size
        self.separators: List[str] = ["\n", "\n\n", "\r", "\r\n", "\n\r", "\t", " ", "  "]



    def clean_text(self, text: str) -> str:
        """Clean the text by replacing multiple newlines with a single newline"""
        import re

        # Replace multiple newlines with a single newline
        cleaned_text = re.sub(r"\n+", "\n", text)
        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)
        # Replace multiple tabs with a single tab
        cleaned_text = re.sub(r"\t+", "\t", cleaned_text)
        # Replace multiple carriage returns with a single carriage return
        cleaned_text = re.sub(r"\r+", "\r", cleaned_text)
        # Replace multiple form feeds with a single form feed
        cleaned_text = re.sub(r"\f+", "\f", cleaned_text)
        # Replace multiple vertical tabs with a single vertical tab
        cleaned_text = re.sub(r"\v+", "\v", cleaned_text)

        return cleaned_text

    def chunk_document(self, datax: DataX) -> List[DataX]:
        """Chunk the datax content into smaller documents"""
        content = datax.content
        cleaned_content = self.clean_text(content)
        content_length = len(cleaned_content)
        chunked_documents: List[DataX] = []
        chunk_number = 1
        chunk_data = datax.to_dict()
        
        start = 0
        while start < content_length:
            end = start + self.chunk_size

            # Ensure we're not splitting a word in half
            if end < content_length:
                while end > start and cleaned_content[end] not in [
                    " ",
                    "\n",
                    "\r",
                    "\t",
                ]:
                    end -= 1

            # If the entire chunk is a word, then just split it at self.chunk_size
            if end == start:
                end = start + self.chunk_size

            # If the end is greater than the content length, then set it to the content length
            if end > content_length:
                end = content_length

            chunk = cleaned_content[start:end]

            chunk_id = None
            if datax.cid:
                chunk_id = f"{datax.cid}_{chunk_number}"
            elif datax.uid:
                chunk_id = f"{datax.uid}_{chunk_number}"
            chunk_datax = DataX.from_dict(chunk_data)
            chunk_datax.cid = chunk_id
            chunk_datax.content = chunk
            chunk_datax.metadata = {"chunk_n": chunk_number, "chunk_size": len(chunk)}

            chunked_documents.append(chunk_datax)
            chunk_number += 1
            start = end
        return chunked_documents
