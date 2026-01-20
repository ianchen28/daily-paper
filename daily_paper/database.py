"""Database module for storing papers, analyses, and reports.

Uses PostgreSQL with pgvector for scalable RAG-ready storage.
Fallback to SQLite for local development.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from .paper_fetcher import Paper

# Try to import PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import Json
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

# Try to import SQLite (always available)
import sqlite3

logger = logging.getLogger(__name__)


class Database:
    """Database manager supporting PostgreSQL (with pgvector) and SQLite.

    Automatically uses PostgreSQL if DATABASE_URL is set, otherwise falls back to SQLite.

    Schema includes:
    - papers: Basic paper metadata
    - analyses: LLM analysis results with optional embeddings
    - reports: Daily report summaries
    - paper_chunks: PDF content chunks for fine-grained retrieval (future)
    """

    def __init__(self, db_url: Optional[str] = None):
        """Initialize database connection.

        Args:
            db_url: Database URL. If None, uses DATABASE_URL env var or SQLite fallback.
                   PostgreSQL: postgresql://user:pass@host:port/dbname
                   SQLite: daily_paper.db
        """
        self.db_url = db_url or os.getenv("DATABASE_URL", "daily_paper.db")
        self.use_postgres = self.db_url.startswith("postgresql://")

        if self.use_postgres:
            if not POSTGRES_AVAILABLE:
                raise ImportError(
                    "PostgreSQL support requires psycopg2. "
                    "Install with: pip install psycopg2-binary"
                )
            self.conn = psycopg2.connect(self.db_url)
            logger.info("Connected to PostgreSQL database")
        else:
            self.conn = sqlite3.connect(self.db_url)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"Connected to SQLite database: {self.db_url}")

        self._init_tables()

    def _init_tables(self) -> None:
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        if self.use_postgres:
            # Enable pgvector extension
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # Papers table (PostgreSQL)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id SERIAL PRIMARY KEY,
                    paper_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT,
                    summary TEXT,
                    authors JSONB,
                    organization TEXT,
                    published_at TIMESTAMP,
                    upvotes INTEGER DEFAULT 0,
                    github_repo TEXT,
                    github_stars INTEGER DEFAULT 0,
                    num_comments INTEGER DEFAULT 0,
                    keywords JSONB,
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for common queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_published_at
                ON papers(published_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_created_at
                ON papers(created_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_keywords
                ON papers USING GIN (keywords)
            """)

            # Analyses table with vector support
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id SERIAL PRIMARY KEY,
                    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
                    analysis_html TEXT NOT NULL,
                    analysis_text TEXT,
                    model_name TEXT,
                    embedding vector(1536),
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(paper_id, analyzed_at)
                )
            """)

            # Create vector index for similarity search
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analyses_embedding
                ON analyses USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)

            # Reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id SERIAL PRIMARY KEY,
                    date DATE UNIQUE NOT NULL,
                    html_content TEXT NOT NULL,
                    paper_count INTEGER DEFAULT 0,
                    web_page_path TEXT,
                    email_sent BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                )
            """)

            # Paper chunks table for fine-grained retrieval
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paper_chunks (
                    id SERIAL PRIMARY KEY,
                    paper_id TEXT NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    chunk_type TEXT,
                    content TEXT NOT NULL,
                    embedding vector(1536),
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(paper_id, chunk_index)
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_paper_chunks_embedding
                ON paper_chunks USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)

        else:
            # SQLite fallback (simplified schema)
            # Papers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT,
                    summary TEXT,
                    authors TEXT,
                    organization TEXT,
                    published_at TEXT,
                    upvotes INTEGER DEFAULT 0,
                    github_repo TEXT,
                    github_stars INTEGER DEFAULT 0,
                    num_comments INTEGER DEFAULT 0,
                    keywords TEXT,
                    raw_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create FTS5 virtual table for full-text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
                    paper_id, title, summary, keywords,
                    content='papers',
                    content_rowid='id'
                )
            """)

            # Analyses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT NOT NULL,
                    analysis_html TEXT NOT NULL,
                    analysis_text TEXT,
                    model_name TEXT,
                    embedding BLOB,
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
                )
            """)

            # Reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE NOT NULL,
                    html_content TEXT NOT NULL,
                    paper_count INTEGER DEFAULT 0,
                    web_page_path TEXT,
                    email_sent BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)

        self.conn.commit()

    def save_paper(self, paper: Paper) -> None:
        """Save or update a paper in database.

        Args:
            paper: Paper object to save
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("""
                INSERT INTO papers (
                    paper_id, title, link, summary, authors, organization,
                    published_at, upvotes, github_repo, github_stars,
                    num_comments, keywords, raw_data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (paper_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    upvotes = EXCLUDED.upvotes,
                    github_stars = EXCLUDED.github_stars,
                    num_comments = EXCLUDED.num_comments,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                paper.paper_id,
                paper.title,
                paper.link,
                paper.summary,
                Json(paper.authors),
                paper.organization,
                paper.published_at,
                paper.upvotes,
                paper.github_repo,
                paper.github_stars,
                paper.num_comments,
                Json(paper.ai_keywords),
                Json(paper.raw_data)
            ))
        else:
            cursor.execute("""
                INSERT OR REPLACE INTO papers (
                    paper_id, title, link, summary, authors, organization,
                    published_at, upvotes, github_repo, github_stars,
                    num_comments, keywords, raw_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.paper_id,
                paper.title,
                paper.link,
                paper.summary,
                json.dumps(paper.authors),
                paper.organization,
                paper.published_at,
                paper.upvotes,
                paper.github_repo,
                paper.github_stars,
                paper.num_comments,
                json.dumps(paper.ai_keywords),
                json.dumps(paper.raw_data)
            ))

            # Update FTS index
            cursor.execute("""
                INSERT OR REPLACE INTO papers_fts(rowid, paper_id, title, summary, keywords)
                SELECT id, paper_id, title, summary, keywords FROM papers WHERE paper_id = ?
            """, (paper.paper_id,))

        self.conn.commit()

    def save_analysis(
        self,
        paper_id: str,
        analysis_html: str,
        model_name: str,
        analysis_text: Optional[str] = None,
        embedding: Optional[List[float]] = None
    ) -> None:
        """Save paper analysis result with optional embedding.

        Args:
            paper_id: Paper ID
            analysis_html: LLM generated HTML analysis
            model_name: Model used for analysis
            analysis_text: Plain text version of analysis (for embedding)
            embedding: Text embedding vector (1536 dimensions)
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("""
                INSERT INTO analyses (paper_id, analysis_html, analysis_text, model_name, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                paper_id,
                analysis_html,
                analysis_text,
                model_name,
                embedding  # pgvector handles list -> vector conversion
            ))
        else:
            # Store embedding as JSON in SQLite
            embedding_blob = json.dumps(embedding) if embedding else None
            cursor.execute("""
                INSERT INTO analyses (paper_id, analysis_html, analysis_text, model_name, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, (paper_id, analysis_html, analysis_text, model_name, embedding_blob))

        self.conn.commit()

    def save_report(
        self,
        date: str,
        html_content: str,
        paper_count: int,
        web_page_path: Optional[str] = None,
        email_sent: bool = False,
        metadata: Optional[Dict] = None
    ) -> None:
        """Save daily report.

        Args:
            date: Report date (YYYY-MM-DD)
            html_content: Full report HTML
            paper_count: Number of papers in report
            web_page_path: Path to generated web page
            email_sent: Whether email was sent successfully
            metadata: Additional metadata
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("""
                INSERT INTO reports (date, html_content, paper_count, web_page_path, email_sent, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO UPDATE SET
                    html_content = EXCLUDED.html_content,
                    paper_count = EXCLUDED.paper_count,
                    web_page_path = EXCLUDED.web_page_path,
                    email_sent = EXCLUDED.email_sent,
                    metadata = EXCLUDED.metadata
            """, (date, html_content, paper_count, web_page_path, email_sent, Json(metadata or {})))
        else:
            cursor.execute("""
                INSERT OR REPLACE INTO reports (date, html_content, paper_count, web_page_path, email_sent, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date, html_content, paper_count, web_page_path, email_sent, json.dumps(metadata or {})))

        self.conn.commit()

    def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        min_similarity: float = 0.7
    ) -> List[Dict]:
        """Search papers by semantic similarity.

        Args:
            query_embedding: Query text embedding vector
            limit: Maximum number of results
            min_similarity: Minimum cosine similarity threshold

        Returns:
            List of paper dicts with similarity scores
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("""
                SELECT
                    p.*,
                    a.analysis_html,
                    a.model_name,
                    1 - (a.embedding <=> %s::vector) as similarity
                FROM papers p
                JOIN analyses a ON p.paper_id = a.paper_id
                WHERE a.embedding IS NOT NULL
                    AND 1 - (a.embedding <=> %s::vector) >= %s
                ORDER BY a.embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, min_similarity, query_embedding, limit))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            # SQLite fallback: load all embeddings and compute similarity in Python
            cursor.execute("""
                SELECT p.*, a.analysis_html, a.model_name, a.embedding
                FROM papers p
                JOIN analyses a ON p.paper_id = a.paper_id
                WHERE a.embedding IS NOT NULL
            """)

            results = []
            import numpy as np
            query_vec = np.array(query_embedding)

            for row in cursor.fetchall():
                embedding = json.loads(row['embedding'])
                doc_vec = np.array(embedding)
                similarity = np.dot(query_vec, doc_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
                )

                if similarity >= min_similarity:
                    result = dict(row)
                    result['similarity'] = float(similarity)
                    results.append(result)

            # Sort by similarity and limit
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]

    def search_papers(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Search papers by keyword in title, summary, or keywords.

        Args:
            keyword: Search keyword
            limit: Maximum number of results

        Returns:
            List of matching paper data dicts
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            search_term = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM papers
                WHERE title ILIKE %s
                   OR summary ILIKE %s
                   OR keywords::text ILIKE %s
                ORDER BY published_at DESC NULLS LAST, created_at DESC
                LIMIT %s
            """, (search_term, search_term, search_term, limit))
        else:
            # Use FTS5 for better full-text search
            cursor.execute("""
                SELECT p.* FROM papers p
                JOIN papers_fts fts ON p.id = fts.rowid
                WHERE papers_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (keyword, limit))

        if self.use_postgres:
            return [dict(row) for row in cursor.fetchall()]
        else:
            return [dict(row) for row in cursor.fetchall()]

    def get_papers_by_date_range(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get papers within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD), defaults to start_date
            limit: Maximum number of results

        Returns:
            List of paper dicts
        """
        if end_date is None:
            end_date = start_date

        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("""
                SELECT p.*, a.analysis_html, a.model_name
                FROM papers p
                LEFT JOIN analyses a ON p.paper_id = a.paper_id
                WHERE DATE(p.created_at) BETWEEN %s AND %s
                ORDER BY p.upvotes DESC, p.created_at DESC
                LIMIT %s
            """, (start_date, end_date, limit))
        else:
            cursor.execute("""
                SELECT p.*, a.analysis_html, a.model_name
                FROM papers p
                LEFT JOIN analyses a ON p.paper_id = a.paper_id
                WHERE DATE(p.created_at) BETWEEN ? AND ?
                ORDER BY p.upvotes DESC, p.created_at DESC
                LIMIT ?
            """, (start_date, end_date, limit))

        if self.use_postgres:
            return [dict(row) for row in cursor.fetchall()]
        else:
            return [dict(row) for row in cursor.fetchall()]

    def get_report(self, date: str) -> Optional[Dict]:
        """Get report by date.

        Args:
            date: Report date (YYYY-MM-DD)

        Returns:
            Report data dict or None if not found
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute("SELECT * FROM reports WHERE date = %s", (date,))
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            cursor.execute("SELECT * FROM reports WHERE date = ?", (date,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_report_dates(self, limit: int = 100) -> List[str]:
        """Get all available report dates.

        Args:
            limit: Maximum number of dates to return

        Returns:
            List of dates in YYYY-MM-DD format, sorted descending
        """
        cursor = self.conn.cursor()

        if self.use_postgres:
            cursor.execute(
                "SELECT date::text FROM reports ORDER BY date DESC LIMIT %s",
                (limit,)
            )
        else:
            cursor.execute(
                "SELECT date FROM reports ORDER BY date DESC LIMIT ?",
                (limit,)
            )

        return [row[0] for row in cursor.fetchall()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics.

        Returns:
            Statistics dict with counts and metrics
        """
        cursor = self.conn.cursor()

        # Total papers
        cursor.execute("SELECT COUNT(*) FROM papers")
        total_papers = cursor.fetchone()[0]

        # Total reports
        cursor.execute("SELECT COUNT(*) FROM reports")
        total_reports = cursor.fetchone()[0]

        # Papers with analysis
        cursor.execute("SELECT COUNT(DISTINCT paper_id) FROM analyses")
        analyzed_papers = cursor.fetchone()[0]

        # Papers with embeddings
        if self.use_postgres:
            cursor.execute("SELECT COUNT(*) FROM analyses WHERE embedding IS NOT NULL")
        else:
            cursor.execute("SELECT COUNT(*) FROM analyses WHERE embedding IS NOT NULL")
        embedded_papers = cursor.fetchone()[0]

        return {
            "total_papers": total_papers,
            "total_reports": total_reports,
            "analyzed_papers": analyzed_papers,
            "embedded_papers": embedded_papers,
            "database_type": "PostgreSQL" if self.use_postgres else "SQLite"
        }

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
