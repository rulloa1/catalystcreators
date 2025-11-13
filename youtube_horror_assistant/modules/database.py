"""
Database Module for YouTube Horror Assistant
Handles storage and retrieval of content ideas, scripts, and metadata
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class ContentDatabase:
    """SQLite database for storing horror content data"""

    def __init__(self, db_path: str = "data/horror_content.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.initialize_database()

    def initialize_database(self) -> None:
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Channel information table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                keywords TEXT,
                logo_prompt TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Story ideas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS story_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                niche TEXT,
                hook TEXT,
                target_duration INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP
            )
        ''')

        # Scripts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER,
                content TEXT NOT NULL,
                duration INTEGER,
                reference_transcript TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (story_id) REFERENCES story_ideas (id)
            )
        ''')

        # Video metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                titles TEXT,
                description TEXT,
                tags TEXT,
                thumbnail_prompts TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts (id)
            )
        ''')

        # Scenes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                scene_number INTEGER,
                content TEXT,
                image_prompt TEXT,
                animation_prompt TEXT,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts (id)
            )
        ''')

        # Analytics table for tracking performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_type TEXT,
                item_id INTEGER,
                metric_name TEXT,
                metric_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def save_channel(self, name: str, description: str, keywords: List[str], logo_prompt: str) -> int:
        """Save channel information and return channel ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO channels (name, description, keywords, logo_prompt)
            VALUES (?, ?, ?, ?)
        ''', (name, description, json.dumps(keywords), logo_prompt))
        self.conn.commit()
        return cursor.lastrowid

    def save_story_idea(self, title: str, description: str, niche: str, hook: str, target_duration: int) -> int:
        """Save story idea and return idea ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO story_ideas (title, description, niche, hook, target_duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, niche, hook, target_duration))
        self.conn.commit()
        return cursor.lastrowid

    def get_story_ideas(self, status: Optional[str] = None, niche: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Retrieve story ideas with optional filters"""
        cursor = self.conn.cursor()

        query = "SELECT * FROM story_ideas WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if niche:
            query += " AND niche = ?"
            params.append(niche)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def mark_story_used(self, story_id: int) -> None:
        """Mark a story idea as used"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE story_ideas
            SET status = 'used', used_at = ?
            WHERE id = ?
        ''', (datetime.now(), story_id))
        self.conn.commit()

    def save_script(self, story_id: Optional[int], content: str, duration: int, reference_transcript: Optional[str] = None) -> int:
        """Save script and return script ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO scripts (story_id, content, duration, reference_transcript)
            VALUES (?, ?, ?, ?)
        ''', (story_id, content, duration, reference_transcript))
        self.conn.commit()
        return cursor.lastrowid

    def save_video_metadata(self, script_id: int, titles: List[str], description: str, tags: List[str], thumbnail_prompts: List[str]) -> int:
        """Save video metadata and return metadata ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO video_metadata (script_id, titles, description, tags, thumbnail_prompts)
            VALUES (?, ?, ?, ?, ?)
        ''', (script_id, json.dumps(titles), description, json.dumps(tags), json.dumps(thumbnail_prompts)))
        self.conn.commit()
        return cursor.lastrowid

    def save_scenes(self, script_id: int, scenes: List[Dict[str, Any]]) -> None:
        """Save multiple scenes for a script"""
        cursor = self.conn.cursor()

        for scene in scenes:
            cursor.execute('''
                INSERT INTO scenes (script_id, scene_number, content, image_prompt, animation_prompt, duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                script_id,
                scene.get('scene_number'),
                scene.get('content'),
                scene.get('image_prompt'),
                scene.get('animation_prompt'),
                scene.get('duration')
            ))

        self.conn.commit()

    def get_script_with_metadata(self, script_id: int) -> Optional[Dict]:
        """Get complete script information including metadata and scenes"""
        cursor = self.conn.cursor()

        # Get script
        cursor.execute("SELECT * FROM scripts WHERE id = ?", (script_id,))
        script = cursor.fetchone()

        if not script:
            return None

        result = dict(script)

        # Get metadata
        cursor.execute("SELECT * FROM video_metadata WHERE script_id = ?", (script_id,))
        metadata = cursor.fetchone()
        if metadata:
            result['metadata'] = dict(metadata)
            result['metadata']['titles'] = json.loads(metadata['titles'])
            result['metadata']['tags'] = json.loads(metadata['tags'])
            result['metadata']['thumbnail_prompts'] = json.loads(metadata['thumbnail_prompts'])

        # Get scenes
        cursor.execute("SELECT * FROM scenes WHERE script_id = ? ORDER BY scene_number", (script_id,))
        scenes = cursor.fetchall()
        result['scenes'] = [dict(scene) for scene in scenes]

        return result

    def save_analytics(self, item_type: str, item_id: int, metric_name: str, metric_value: str) -> None:
        """Save analytics data"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO analytics (item_type, item_id, metric_name, metric_value)
            VALUES (?, ?, ?, ?)
        ''', (item_type, item_id, metric_name, metric_value))
        self.conn.commit()

    def get_analytics(self, item_type: Optional[str] = None, metric_name: Optional[str] = None) -> List[Dict]:
        """Retrieve analytics data"""
        cursor = self.conn.cursor()

        query = "SELECT * FROM analytics WHERE 1=1"
        params = []

        if item_type:
            query += " AND item_type = ?"
            params.append(item_type)

        if metric_name:
            query += " AND metric_name = ?"
            params.append(metric_name)

        query += " ORDER BY created_at DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
