from utils.ui.icon_system import get_icon, replace_emojis
"""
Project Timeline Utility
Parses git commits and groups them by weeks and action types for timeline visualization
"""
import subprocess
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def get_git_commits(limit: Optional[int] = None) -> List[Dict[str, str]]:
    """
    Get git commits from the repository
    
    Args:
        limit: Maximum number of commits to retrieve (None for all)
    
    Returns:
        List of commit dictionaries with keys: hash, date, message
    """
    try:
        cmd = ['git', 'log', '--all', '--date=short', '--pretty=format:%h|%ad|%s']
        if limit:
            cmd.extend(['-n', str(limit)])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd='.'
        )
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|', 2)
            if len(parts) == 3:
                commits.append({
                    'hash': parts[0],
                    'date': parts[1],
                    'message': parts[2]
                })
        
        return commits
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def categorize_commit(message: str) -> str:
    """
    Categorize commit message by action type
    
    Args:
        message: Commit message
    
    Returns:
        Category name (ADD, FIX, REMOVE, MERGE, DOCS, REFACTOR, OTHER)
    """
    message_upper = message.upper()
    
    if message_upper.startswith('ADD:'):
        return 'ADD'
    elif message_upper.startswith('FIX:'):
        return 'FIX'
    elif message_upper.startswith('REMOVE:'):
        return 'REMOVE'
    elif message_upper.startswith('MERGE') or 'MERGE' in message_upper:
        return 'MERGE'
    elif any(keyword in message_upper for keyword in ['DOC', 'DOCUMENTACION', 'DOCUMENTATION']):
        return 'DOCS'
    elif any(keyword in message_upper for keyword in ['REFACTOR', 'ORGANIZACION', 'ORGANIZATION', 'MODULAR', 'SEPARACION']):
        return 'REFACTOR'
    else:
        return 'OTHER'


def get_week_start(date_str: str) -> str:
    """
    Get the Monday of the week for a given date
    
    Args:
        date_str: Date string in YYYY-MM-DD format
    
    Returns:
        Monday date string in YYYY-MM-DD format
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Get Monday of the week (weekday 0 = Monday)
        days_since_monday = date_obj.weekday()
        monday = date_obj - timedelta(days=days_since_monday)
        return monday.strftime('%Y-%m-%d')
    except (ValueError, AttributeError):
        return date_str


def format_week_label(week_start: str) -> str:
    """
    Format week label for display
    
    Args:
        week_start: Monday date string in YYYY-MM-DD format
    
    Returns:
        Formatted week label (e.g., "Semana del 25 Ago")
    """
    try:
        date_obj = datetime.strptime(week_start, '%Y-%m-%d')
        # Get Sunday of the week
        sunday = date_obj + timedelta(days=6)
        
        month_names = {
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr',
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        }
        
        return f"Semana del {date_obj.day} {month_names[date_obj.month]}"
    except (ValueError, AttributeError):
        return week_start


def group_commits_by_week_and_action(commits: List[Dict[str, str]]) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    """
    Group commits by week and action type
    
    Args:
        commits: List of commit dictionaries
    
    Returns:
        Nested dictionary: {week_start: {action_type: [commits]}}
    """
    grouped = defaultdict(lambda: defaultdict(list))
    
    for commit in commits:
        week_start = get_week_start(commit['date'])
        action_type = categorize_commit(commit['message'])
        grouped[week_start][action_type].append(commit)
    
    # Sort weeks chronologically
    sorted_weeks = sorted(grouped.keys())
    result = {}
    for week in sorted_weeks:
        result[week] = dict(grouped[week])
    
    return result


def get_timeline_summary(grouped_commits: Dict[str, Dict[str, List[Dict[str, str]]]]) -> Dict[str, any]:
    """
    Get summary statistics for the timeline
    
    Args:
        grouped_commits: Grouped commits dictionary
    
    Returns:
        Dictionary with summary statistics
    """
    total_commits = 0
    total_weeks = len(grouped_commits)
    action_counts = defaultdict(int)
    
    for week_data in grouped_commits.values():
        for action_type, commits in week_data.items():
            count = len(commits)
            total_commits += count
            action_counts[action_type] += count
    
    return {
        'total_commits': total_commits,
        'total_weeks': total_weeks,
        'action_counts': dict(action_counts),
        'first_week': min(grouped_commits.keys()) if grouped_commits else None,
        'last_week': max(grouped_commits.keys()) if grouped_commits else None
    }


def get_action_icon(action_type: str) -> str:
    """
    Get emoji icon for action type
    
    Args:
        action_type: Action category
    
    Returns:
        Emoji icon
    """
    icons = {
        'ADD': '➕',
        'FIX': '🔧',
        'REMOVE': '🗑️',
        'MERGE': '🔀',
        'DOCS': '📚',
        'REFACTOR': '♻️',
        'OTHER': '📝'
    }
    return icons.get(action_type, '📝')


def get_action_color(action_type: str) -> str:
    """
    Get color for action type
    
    Args:
        action_type: Action category
    
    Returns:
        Hex color code
    """
    colors = {
        'ADD': '#28a745',
        'FIX': '#ffc107',
        'REMOVE': '#dc3545',
        'MERGE': '#6f42c1',
        'DOCS': '#17a2b8',
        'REFACTOR': '#fd7e14',
        'OTHER': '#6c757d'
    }
    return colors.get(action_type, '#6c757d')

