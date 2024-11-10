from pathlib import Path
from typing import List, Union, IO, Any

from pypdf import PdfReader
import pymupdf4llm 


from xact.plugin.document.base import Document
from xact.plugin.document.doc.base import Doc
from xact.utils.log import logger

def to_text(pdf_path):
    # creating a pdf reader object
    reader = PdfReader(pdf_path)

    # printing number of pages in pdf file
    text = ""
    for page in reader.pages:
        text += "\n\n\n"+ page.extract_text()
    return text

def to_markdown(pdf_path):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text

class PDF(Doc):
    """Doc for PDF files"""

    def read(self, pdf: Union[str, Path, IO[Any]]) -> List[Document]:
        if not pdf:
            raise ValueError("No pdf provided")


        doc_name = ""
        try:
            if isinstance(pdf, str):
                doc_name = pdf.split("/")[-1].split(".")[0].replace(" ", "_")
            else:
                doc_name = pdf.name.split(".")[0]
        except Exception:
            doc_name = "pdf"

        logger.info(f"Reading: {doc_name}")
        doc_reader = PdfReader(pdf)

        documents = [
            Document(
                name=doc_name,
                id=f"{doc_name}_{page_number}",
                meta_data={"page": page_number},
                content=page.extract_text(),
            )
            for page_number, page in enumerate(doc_reader.pages, start=1)
        ]
        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents
        return documents


class PDFUrl(Doc):
    """Doc for PDF files from URL"""

    def read(self, url: str) -> List[Document]:
        if not url:
            raise ValueError("No url provided")

        from io import BytesIO

        try:
            import httpx
        except ImportError:
            raise ImportError("`httpx` not installed")

        try:
            from pypdf import PdfReader as PdfReader  # noqa: F401
        except ImportError:
            raise ImportError("`pypdf` not installed")

        logger.info(f"Reading: {url}")
        response = httpx.get(url)

        doc_name = url.split("/")[-1].split(".")[0].replace("/", "_").replace(" ", "_")
        doc_reader = PdfReader(BytesIO(response.content))

        documents = [
            Document(
                name=doc_name,
                id=f"{doc_name}_{page_number}",
                meta_data={"page": page_number},
                content=page.extract_text(),
            )
            for page_number, page in enumerate(doc_reader.pages, start=1)
        ]
        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents
        return documents


class PDFImage(Doc):
    """Doc for PDF files with text and images extraction"""

    def read(self, pdf: Union[str, Path, IO[Any]]) -> List[Document]:
        if not pdf:
            raise ValueError("No pdf provided")

        try:
            import rapidocr_onnxruntime as rapidocr
            from pypdf import PdfReader as PdfReader  # noqa: F401
        except ImportError:
            raise ImportError("`pypdf` or `rapidocr_onnxruntime` not installed")

        doc_name = ""
        try:
            if isinstance(pdf, str):
                doc_name = pdf.split("/")[-1].split(".")[0].replace(" ", "_")
            else:
                doc_name = pdf.name.split(".")[0]
        except Exception:
            doc_name = "pdf"

        logger.info(f"Reading: {doc_name}")
        doc_reader = PdfReader(pdf)

        # Initialize RapidOCR
        ocr = rapidocr.RapidOCR()

        documents = []
        for page_number, page in enumerate(doc_reader.pages, start=1):
            page_text = page.extract_text() or ""
            images_text_list: List = []

            for image_object in page.images:
                image_data = image_object.data

                # Perform OCR on the image
                ocr_result, elapse = ocr(image_data)

                # Extract text from OCR result
                if ocr_result:
                    images_text_list += [item[1] for item in ocr_result]

            images_text: str = "\n".join(images_text_list)
            content = page_text + "\n" + images_text

            documents.append(
                Document(
                    name=doc_name,
                    id=f"{doc_name}_{page_number}",
                    meta_data={"page": page_number},
                    content=content,
                )
            )

        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents

        return documents


class PDFUrlImage(Doc):
    """Doc for PDF files from URL with text and images extraction"""

    def read(self, url: str) -> List[Document]:
        if not url:
            raise ValueError("No url provided")

        from io import BytesIO

        try:
            import httpx
            from pypdf import PdfReader as PdfReader
            import rapidocr_onnxruntime as rapidocr
        except ImportError:
            raise ImportError("`httpx`, `pypdf` or `rapidocr_onnxruntime` not installed")

        # Read the PDF from the URL
        logger.info(f"Reading: {url}")
        response = httpx.get(url)

        doc_name = url.split("/")[-1].split(".")[0].replace(" ", "_")
        doc_reader = PdfReader(BytesIO(response.content))

        # Initialize RapidOCR
        ocr = rapidocr.RapidOCR()

        # Process each page of the PDF
        documents = []
        for page_number, page in enumerate(doc_reader.pages, start=1):
            page_text = page.extract_text() or ""
            images_text_list = []

            # Extract and process images
            for image_object in page.images:
                image_data = image_object.data

                # Perform OCR on the image
                ocr_result, elapse = ocr(image_data)

                # Extract text from OCR result
                if ocr_result:
                    images_text_list += [item[1] for item in ocr_result]

            images_text = "\n".join(images_text_list)
            content = page_text + "\n" + images_text

            # Append the document
            documents.append(
                Document(
                    name=doc_name,
                    id=f"{doc_name}_{page_number}",
                    meta_data={"page": page_number},
                    content=content,
                )
            )

        # Optionally chunk documents
        if self.chunk:
            chunked_documents = []
            for document in documents:
                chunked_documents.extend(self.chunk_document(document))
            return chunked_documents

        return documents