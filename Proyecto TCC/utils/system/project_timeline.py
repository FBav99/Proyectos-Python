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


def create_gantt_chart_data(grouped_commits: Dict[str, Dict[str, List[Dict[str, str]]]]) -> List[Dict]:
    """
    Create data for Gantt chart visualization
    
    Args:
        grouped_commits: Grouped commits dictionary
    
    Returns:
        List of dictionaries with Gantt chart data
    """
    gantt_data = []
    
    # Sort weeks chronologically
    sorted_weeks = sorted(grouped_commits.keys())
    
    for week_start in sorted_weeks:
        week_data = grouped_commits[week_start]
        
        # Get Monday (start) and Sunday (end) of the week
        try:
            monday = datetime.strptime(week_start, '%Y-%m-%d')
            sunday = monday + timedelta(days=6)
        except (ValueError, AttributeError):
            continue
        
        # Create a bar for each action type in this week
        for action_type, commits in week_data.items():
            if not commits:
                continue
            
            # Count commits for this action type in this week
            commit_count = len(commits)
            
            # Create task label with icon and count
            icon = get_action_icon(action_type)
            task_label = f"{icon} {action_type} ({commit_count})"
            
            gantt_data.append({
                'Task': task_label,
                'Start': monday,
                'Finish': sunday,
                'Action': action_type,
                'Commits': commit_count,
                'Color': get_action_color(action_type)
            })
    
    return gantt_data


def create_gantt_chart_plotly(grouped_commits: Dict[str, Dict[str, List[Dict[str, str]]]]):
    """
    Create a Gantt chart using Plotly
    
    Args:
        grouped_commits: Grouped commits dictionary
    
    Returns:
        Plotly figure object
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None
    
    # Get Gantt chart data
    gantt_data = create_gantt_chart_data(grouped_commits)
    
    if not gantt_data:
        return None
    
    # Create unique tasks by combining week and action type
    tasks_dict = {}
    
    for item in gantt_data:
        # Create unique task key: Action + Week
        week_label = item['Start'].strftime('%Y-%m-%d')
        task_key = f"{item['Action']}_{week_label}"
        
        if task_key not in tasks_dict:
            # Create task label
            icon = get_action_icon(item['Action'])
            week_start_str = item['Start'].strftime('%d/%m')
            week_end_str = item['Finish'].strftime('%d/%m')
            task_label = f"{icon} {item['Action']} - {week_start_str} a {week_end_str}"
            
            tasks_dict[task_key] = {
                'Task': task_label,
                'Start': item['Start'],
                'Finish': item['Finish'],
                'Action': item['Action'],
                'Commits': item['Commits'],
                'Color': item['Color']
            }
        else:
            # Merge commit counts
            tasks_dict[task_key]['Commits'] += item['Commits']
    
    # Convert to list and sort by start date, then action type
    tasks_list = list(tasks_dict.values())
    tasks_list.sort(key=lambda x: (x['Start'], x['Action']))
    
    # Create figure with timeline-style bars
    fig = go.Figure()
    
    # Add a trace for each action type to enable grouping in legend
    action_types = sorted(set(task['Action'] for task in tasks_list))
    
    for action_type in action_types:
        # Filter tasks for this action type
        action_tasks = [t for t in tasks_list if t['Action'] == action_type]
        
        if not action_tasks:
            continue
        
        # Create arrays for this action type
        task_names = [t['Task'] for t in action_tasks]
        starts = [t['Start'] for t in action_tasks]
        finishes = [t['Finish'] for t in action_tasks]
        commits = [t['Commits'] for t in action_tasks]
        colors = [t['Color'] for t in action_tasks]
        
        # For Gantt charts, we'll use dates directly
        # Calculate the difference (duration) as timedelta objects
        # Plotly bar charts can handle datetime objects for base
        
        # Create individual traces for each task to properly handle dates
        for i, task in enumerate(action_tasks):
            start = task['Start']
            finish = task['Finish']
            duration_days = (finish - start).days + 1
            
            # Add a bar for each task
            fig.add_trace(go.Bar(
                name=get_action_icon(action_type) + ' ' + action_type if i == 0 else '',  # Only show in legend once
                x=[duration_days],
                y=[task['Task']],
                base=[start],
                orientation='h',
                marker=dict(
                    color=task['Color'],
                    line=dict(color='white', width=1)
                ),
                text=[f"{task['Commits']} commits"],
                textposition='inside',
                textfont=dict(color='white', size=9),
                hovertemplate='<b>%{y}</b><br>' +
                             f'Inicio: {start.strftime("%d/%m/%Y")}<br>' +
                             f'Fin: {finish.strftime("%d/%m/%Y")}<br>' +
                             f'Commits: {task["Commits"]}<br>' +
                             '<extra></extra>',
                showlegend=(i == 0)  # Only show in legend for first task of this type
            ))
    
    # Update layout for Gantt chart
    fig.update_layout(
        title=dict(
            text='📊 Gráfico de Gantt - Progreso del Proyecto',
            x=0.5,
            font=dict(size=18)
        ),
        xaxis=dict(
            title='Fecha',
            type='date',
            showgrid=True,
            gridcolor='lightgray',
            side='top'
        ),
        yaxis=dict(
            title='Actividades por Semana',
            showgrid=True,
            gridcolor='lightgray',
            autorange='reversed',
            tickfont=dict(size=10)
        ),
        height=max(600, len(tasks_list) * 50),
        template='plotly_white',
        hovermode='closest',
        margin=dict(l=250, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig

