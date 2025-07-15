import os
from typing import List, Dict, Any, Tuple

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding
        self.metadata = []  # Store metadata for each document

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith(".txt"):
                self.load_file()
            elif self.path.endswith(".pdf"):
                self.load_pdf()
            else:
                raise ValueError(
                    "Provided path is neither a valid directory nor a supported file type (.txt or .pdf)."
                )
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a supported file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            content = f.read()
            self.documents.append(content)
            self.metadata.append({
                "source": self.path,
                "type": "txt",
                "page": None
            })

    def load_pdf(self):
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 is required for PDF support. Install with: pip install PyPDF2")
        
        with open(self.path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    self.documents.append(text)
                    self.metadata.append({
                        "source": self.path,
                        "type": "pdf",
                        "page": page_num + 1,
                        "total_pages": len(pdf_reader.pages)
                    })

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".txt"):
                    with open(file_path, "r", encoding=self.encoding) as f:
                        content = f.read()
                        self.documents.append(content)
                        self.metadata.append({
                            "source": file_path,
                            "type": "txt",
                            "page": None
                        })
                elif file.endswith(".pdf") and PDF_AVAILABLE:
                    with open(file_path, "rb") as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            if text.strip():
                                self.documents.append(text)
                                self.metadata.append({
                                    "source": file_path,
                                    "type": "pdf",
                                    "page": page_num + 1,
                                    "total_pages": len(pdf_reader.pages)
                                })

    def load_documents(self):
        self.load()
        return self.documents

    def get_documents_with_metadata(self):
        """Return documents along with their metadata."""
        self.load()
        return list(zip(self.documents, self.metadata))


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks
    
    def split_texts_with_metadata(self, texts_with_metadata: List[Tuple[str, Dict[str, Any]]]) -> List[Tuple[str, Dict[str, Any]]]:
        """Split texts while preserving and updating metadata."""
        chunks_with_metadata = []
        for text, metadata in texts_with_metadata:
            text_chunks = self.split(text)
            for i, chunk in enumerate(text_chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_id"] = i
                chunk_metadata["total_chunks"] = len(text_chunks)
                chunks_with_metadata.append((chunk, chunk_metadata))
        return chunks_with_metadata


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
