from __future__ import annotations

from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    """Indexing pipeline configuration.

    Fields
    ------
    bib_file
        Path to the BibTeX file listing papers to ingest.
    index_name
        Name of the Elasticsearch index to create / populate.
    batch_size
        Number of BibTeX entries processed per batch (also used for ES bulk size).
    acl_concurrency
        Number of asyncio workers for PDF downloading.
    crossref_concurrency
        Number of asyncio workers for Crossref API requests.
    download_retries
        Number of retries for downloading PDFs.
    max_entries
        Optional hard cap on number of BibTeX records to ingest (``None`` = all).
    force_delete_index
        If *true*, drop an existing index with the same name before ingesting.
    es_host
        Elasticsearch HTTP endpoint (single-node setup assumed).
    openai_base_url, embedding_model_name, embedding_batch_size, openai_api_key
        See :pyfile:`src.common.settings` – parameters forwarded to the embedding client.
    pagerank_alpha
        Damping factor for PageRank (probability of following citation links).
    """

    bib_file: Path = Field(..., env="BIB_FILE")
    index_name: str = Field("papers", env="INDEX_NAME")
    batch_size: int = Field(100, env="BATCH_SIZE")
    acl_concurrency: int = Field(10, env="ACL_CONCURRENCY")
    crossref_concurrency: int = Field(10, env="CROSSREF_CONCURRENCY")
    download_retries: int = Field(3, env="DOWNLOAD_RETRIES")
    max_entries: Optional[int] = Field(None, env="MAX_ENTRIES")
    force_delete_index: bool = Field(False, env="FORCE_DELETE_INDEX")
    es_host: str = Field("http://localhost:9200", env="ES_HOST")

    openai_base_url: str = Field("http://localhost:8000/v1", env="OPENAI_BASE_URL")
    embedding_model_name: str = Field(
        "text-embedding-3-small", env="EMBEDDING_MODEL_NAME"
    )
    embedding_batch_size: int = Field(128, env="EMBEDDING_BATCH_SIZE")

    openai_api_key: str = Field("not-needed", env="OPENAI_API_KEY")

    pagerank_alpha: float = Field(0.85, env="PAGERANK_ALPHA")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
