import sqlite3
import os
from typing import Dict, List, Any

DB_PATH = 'my_research_daily.db'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """初始化数据库并创建 papers 表"""
    conn = get_connection()
    cursor = conn.cursor()
    # 创建 papers 表，包含指定字段。
    # status 默认为 未读
    # importance_level 默认为 1（即1星）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT,
            abstract TEXT,
            url TEXT,
            published_date TEXT,
            status TEXT DEFAULT '未读',
            importance_level INTEGER DEFAULT 1,
            user_notes TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

def save_paper(paper: Dict[str, Any]):
    """插入新抓取的论文，如果 ID 存在则忽略，以避免重复抓取时产生覆盖"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO papers 
        (id, title, authors, abstract, url, published_date, status, importance_level, user_notes)
        VALUES (?, ?, ?, ?, ?, ?, '未读', 1, '')
    ''', (
        paper.get('id'),
        paper.get('title'),
        paper.get('authors'),
        paper.get('abstract'),
        paper.get('url'),
        paper.get('published_date')
    ))
    conn.commit()
    conn.close()

def get_all_papers() -> List[Dict[str, Any]]:
    """获取所有论文（可用于今日查新等全量展示或搜索）"""
    return _fetch_papers("SELECT * FROM papers ORDER BY published_date DESC")

def get_papers_by_status(status: str) -> List[Dict[str, Any]]:
    """根据状态（未读/已读）获取论文列表"""
    query = "SELECT * FROM papers WHERE status = ? ORDER BY published_date DESC"
    return _fetch_papers(query, (status,))

def _fetch_papers(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """通用的查询辅助函数"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # 方便按列名获取数据
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_paper(paper_id: str, status: str, importance_level: int, user_notes: str):
    """更新论文的状态、星级和批注"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE papers 
        SET status = ?, importance_level = ?, user_notes = ? 
        WHERE id = ?
    ''', (status, importance_level, user_notes, paper_id))
    conn.commit()
    conn.close()
