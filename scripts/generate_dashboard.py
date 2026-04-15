#!/usr/bin/env python3
"""
Generate GitHub traffic dashboard with graphs and statistics.

This script:
1. Loads historical traffic data from history.json
2. Generates graphs for different time intervals (daily, weekly, bi-weekly, cumulative)
3. Calculates statistics for 30 days, 90 days, and lifetime
4. Updates README.md with statistics and embedded graph images

Error codes: GD001-008
"""

# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS FOR YOUR NEEDS
# ============================================================================

# File Paths Configuration
# These paths are relative to the repository root directory
HISTORY_FILE_PATH = "history.json"           # Path to historical traffic data
README_FILE_PATH = "README.md"               # Path to README file to update
GRAPHS_DIRECTORY = "graphs"                  # Directory for storing graph images

# Graph Configuration
# Graph dimensions and quality settings
GRAPH_DPI = 100                              # Dots per inch for graph quality
GRAPH_FIGSIZE_DAILY = (12, 6)                # Dimensions for daily graphs (width, height)
GRAPH_FIGSIZE_WEEKLY = (14, 6)               # Dimensions for weekly graphs
GRAPH_FIGSIZE_BIWEEKLY = (16, 6)             # Dimensions for bi-weekly graphs
GRAPH_FIGSIZE_CUMULATIVE = (14, 6)           # Dimensions for cumulative graphs

# Time Period Configuration
# Number of days for different time periods
DAILY_GRAPH_DAYS = 30                        # Days to show in daily graphs
WEEKLY_GRAPH_WEEKS = 12                     # Weeks to show in weekly graphs (3 months)
BIWEEKLY_GRAPH_PERIODS = 26                 # Bi-weekly periods to show (1 year)

# Statistics Periods
# Days for calculating statistics
STATS_PERIOD_SHORT_TERM = 30               # Short-term statistics period (default: 30 days)
STATS_PERIOD_MEDIUM_TERM = 90               # Medium-term statistics period (default: 90 days)

# Graph Style Configuration
# Color schemes for graphs
CLONES_COLOR = "#2196F3"                    # Blue for clones
VIEWS_COLOR = "#4CAF50"                     # Green for views
GRID_COLOR = "#E0E0E0"                      # Light gray for grid lines
TEXT_COLOR = "#333333"                      # Dark gray for text

# Repository Display Configuration
# How repository names are displayed in graphs and README
# Set to True to show full "owner/repo" name, False to show only repo name
SHOW_FULL_REPO_NAME = False                  # If False, shows only repository name

# README Generation Configuration
# Settings for README.md generation
README_HEADER_LEVEL = 1                      # Markdown header level for repository names (1-6)
INCLUDE_CUMULATIVE_GRAPHS = True            # Whether to include cumulative graphs
INCLUDE_SEPARATE_CUMULATIVE = True          # Whether to include separate clones/views cumulative graphs

# ============================================================================
# END OF CONFIGURATION SECTION
# The following settings typically do not need modification
# ============================================================================

# Standard library imports
import json  # For JSON file operations
import sys   # For system exit and error handling
import os    # For file system operations

# Date and time handling
from datetime import datetime, timedelta  # For date calculations

# Type hints for better code documentation
from typing import Dict, List, Any, Tuple  # For type annotations

# Plotting libraries
import matplotlib.pyplot as plt  # For creating graphs
import matplotlib.dates as mdates  # For date formatting in graphs


def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Load a JSON file from disk with comprehensive error handling.
    
    Args:
        filepath: Path to the JSON file to load
        
    Returns:
        Dictionary containing the parsed JSON data
        
    Raises:
        SystemExit: If file not found (GD001), invalid JSON (GD002), or other error (GD003)
    """
    try:
        # Open and read the JSON file
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # ERROR_CODE: GD001 - File not found
        print(f"ERROR_CODE: GD001 - File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        # ERROR_CODE: GD002 - Invalid JSON format
        print(f"ERROR_CODE: GD002 - Invalid JSON in {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # ERROR_CODE: GD003 - General load error
        print(f"ERROR_CODE: GD003 - Error loading {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def save_file(content: str, filepath: str) -> None:
    """
    Save content to a file with error handling.
    
    Args:
        content: String content to write to the file
        filepath: Path where the file should be saved
        
    Raises:
        SystemExit: If file cannot be saved (GD004)
    """
    try:
        # Open the file in write mode and save the content
        with open(filepath, 'w') as f:
            f.write(content)
    except Exception as e:
        # ERROR_CODE: GD004 - File save error
        print(f"ERROR_CODE: GD004 - Error saving to {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def prepare_graphs_directory() -> None:
    """
    Create the graphs directory if it doesn't exist.
    
    This ensures the directory for storing graph images exists before
    attempting to save any graphs.
    
    Raises:
        SystemExit: If directory cannot be created (GD005)
    """
    try:
        # Create directory if it doesn't exist, don't error if it does
        # Uses GRAPHS_DIRECTORY configuration parameter
        os.makedirs(GRAPHS_DIRECTORY, exist_ok=True)
    except Exception as e:
        # ERROR_CODE: GD005 - Directory creation error
        print(f"ERROR_CODE: GD005 - Error creating graphs directory: {e}", file=sys.stderr)
        sys.exit(1)


def calculate_period_stats(daily_data: List[Dict[str, Any]], days: int) -> Dict[str, int]:
    """
    Calculate statistics for a specific time period (e.g., last 30 days, last 90 days).
    
    This function sums up clones and views for all entries within the specified
    number of days from today.
    
    Args:
        daily_data: List of daily data entries with date, clones, and views
        days: Number of days to look back from today
        
    Returns:
        Dictionary with keys: clones_total, clones_unique, views_total, views_unique
    """
    # Return zeros if no data available
    if not daily_data:
        return {
            'clones_total': 0,
            'clones_unique': 0,
            'views_total': 0,
            'views_unique': 0
        }
    
    # Calculate the cutoff date (N days ago)
    cutoff_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # Initialize statistics counters
    stats = {
        'clones_total': 0,
        'clones_unique': 0,
        'views_total': 0,
        'views_unique': 0
    }
    
    # Sum up statistics for entries within the time period
    for entry in daily_data:
        if entry.get('date', '') >= cutoff_date:
            stats['clones_total'] += entry.get('clones_total', 0)
            stats['clones_unique'] += entry.get('clones_unique', 0)
            stats['views_total'] += entry.get('views_total', 0)
            stats['views_unique'] += entry.get('views_unique', 0)
    
    return stats


def calculate_lifetime_stats(daily_data: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Calculate lifetime statistics from all available daily data.
    
    This function sums up all clones and views across the entire
    historical data set.
    
    Args:
        daily_data: List of all daily data entries
        
    Returns:
        Dictionary with keys: clones_total, clones_unique, views_total, views_unique
    """
    # Return zeros if no data available
    if not daily_data:
        return {
            'clones_total': 0,
            'clones_unique': 0,
            'views_total': 0,
            'views_unique': 0
        }
    
    # Initialize statistics counters
    stats = {
        'clones_total': 0,
        'clones_unique': 0,
        'views_total': 0,
        'views_unique': 0
    }
    
    # Sum up statistics for all entries
    for entry in daily_data:
        stats['clones_total'] += entry.get('clones_total', 0)
        stats['clones_unique'] += entry.get('clones_unique', 0)
        stats['views_total'] += entry.get('views_total', 0)
        stats['views_unique'] += entry.get('views_unique', 0)
    
    return stats


def get_daily_data(daily_data: List[Dict[str, Any]], days: int) -> Tuple[List[str], List[int], List[int]]:
    """
    Extract daily data for the last N days.
    
    This function filters daily_data to only include entries within
    the specified number of days from today.
    
    Args:
        daily_data: List of all daily data entries
        days: Number of days to include
        
    Returns:
        Tuple containing:
        - List of date strings
        - List of clone counts
        - List of view counts
    """
    # Return empty lists if no data available
    if not daily_data:
        return [], [], []
    
    # Calculate the cutoff date (N days ago)
    cutoff_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # Initialize lists to hold the filtered data
    dates = []
    clones = []
    views = []
    
    # Filter and extract data within the time period
    for entry in daily_data:
        if entry.get('date', '') >= cutoff_date:
            dates.append(entry.get('date', ''))
            clones.append(entry.get('clones_total', 0))
            views.append(entry.get('views_total', 0))
    
    return dates, clones, views


def get_weekly_data(daily_data: List[Dict[str, Any]], weeks: int) -> Tuple[List[str], List[int], List[int]]:
    """
    Aggregate daily data into weekly intervals for the last N weeks.
    
    This function groups daily data by week and sums up clones and views
    for each week. A week is defined as 7 consecutive days.
    
    Args:
        daily_data: List of all daily data entries
        weeks: Number of weeks to include
        
    Returns:
        Tuple containing:
        - List of week start dates
        - List of weekly clone totals
        - List of weekly view totals
    """
    # Return empty lists if no data available
    if not daily_data:
        return [], [], []
    
    # Get today's date
    today = datetime.utcnow().date()
    weekly_data = []
    
    # Iterate through weeks from oldest to newest
    for w in range(weeks, -1, -1):
        # Calculate week start and end dates
        week_start = today - timedelta(weeks=w * 7)
        week_end = week_start + timedelta(days=6)
        
        # Initialize counters for this week
        week_clones = 0
        week_views = 0
        
        # Sum up data for entries within this week
        for entry in daily_data:
            entry_date = datetime.strptime(entry.get('date', ''), '%Y-%m-%d').date()
            if week_start <= entry_date <= week_end:
                week_clones += entry.get('clones_total', 0)
                week_views += entry.get('views_total', 0)
        
        # Store the aggregated week data
        weekly_data.append({
            'date': week_start.strftime('%Y-%m-%d'),
            'clones': week_clones,
            'views': week_views
        })
    
    # Extract lists from the aggregated data
    dates = [w['date'] for w in weekly_data]
    clones = [w['clones'] for w in weekly_data]
    views = [w['views'] for w in weekly_data]
    
    return dates, clones, views


def get_biweekly_data(daily_data: List[Dict[str, Any]], periods: int) -> Tuple[List[str], List[int], List[int]]:
    """
    Aggregate daily data into bi-weekly (2-week) intervals for the last N periods.
    
    This function groups daily data by 2-week periods and sums up clones and views
    for each period. A period is defined as 14 consecutive days.
    
    Args:
        daily_data: List of all daily data entries
        periods: Number of bi-weekly periods to include
        
    Returns:
        Tuple containing:
        - List of period start dates
        - List of period clone totals
        - List of period view totals
    """
    # Return empty lists if no data available
    if not daily_data:
        return [], [], []
    
    # Get today's date
    today = datetime.utcnow().date()
    biweekly_data = []
    
    # Iterate through periods from oldest to newest
    for p in range(periods, -1, -1):
        # Calculate period start and end dates (14 days)
        period_start = today - timedelta(days=p * 14)
        period_end = period_start + timedelta(days=13)
        
        # Initialize counters for this period
        period_clones = 0
        period_views = 0
        
        # Sum up data for entries within this period
        for entry in daily_data:
            entry_date = datetime.strptime(entry.get('date', ''), '%Y-%m-%d').date()
            if period_start <= entry_date <= period_end:
                period_clones += entry.get('clones_total', 0)
                period_views += entry.get('views_total', 0)
        
        # Store the aggregated period data
        biweekly_data.append({
            'date': period_start.strftime('%Y-%m-%d'),
            'clones': period_clones,
            'views': period_views
        })
    
    # Extract lists from the aggregated data
    dates = [b['date'] for b in biweekly_data]
    clones = [b['clones'] for b in biweekly_data]
    views = [b['views'] for b in biweekly_data]
    
    return dates, clones, views


def get_cumulative_data(daily_data: List[Dict[str, Any]]) -> Tuple[List[str], List[int], List[int]]:
    """
    Calculate cumulative (additive) data over time.
    
    This function calculates running totals of clones and views,
    showing how the total grows over time. Each data point represents
    the sum of all previous days plus the current day.
    
    Args:
        daily_data: List of all daily data entries (should be sorted by date)
        
    Returns:
        Tuple containing:
        - List of dates
        - List of cumulative clone totals
        - List of cumulative view totals
    """
    # Return empty lists if no data available
    if not daily_data:
        return [], [], []
    
    # Initialize lists to hold the cumulative data
    dates = []
    cumulative_clones = []
    cumulative_views = []
    
    # Initialize running totals
    total_clones = 0
    total_views = 0
    
    # Calculate running totals for each day
    for entry in daily_data:
        # Add current day's values to running totals
        total_clones += entry.get('clones_total', 0)
        total_views += entry.get('views_total', 0)
        
        # Store the date and running totals
        dates.append(entry.get('date', ''))
        cumulative_clones.append(total_clones)
        cumulative_views.append(total_views)
    
    return dates, cumulative_clones, cumulative_views


def create_graph(dates: List[str], values: List[int], title: str, ylabel: str, 
                 filename: str, color: str = 'blue', figsize: Tuple[int, int] = None) -> None:
    """
    Create a single-line graph with the given data.
    
    This function creates a line graph showing one metric over time.
    The graph includes markers, grid lines, and properly formatted dates.
    
    Args:
        dates: List of date strings in 'YYYY-MM-DD' format
        values: List of numeric values corresponding to each date
        title: Title for the graph
        ylabel: Label for the y-axis
        filename: Path where the graph image will be saved
        color: Color for the line (default: 'blue')
        figsize: Figure size as (width, height) tuple (uses GRAPH_FIGSIZE_CUMULATIVE if None)
        
    Raises:
        SystemExit: If graph creation fails (GD006)
    """
    try:
        # Check if we have data to plot
        if not dates or not values:
            print(f"WARNING: No data for graph: {title}")
            return
        
        # Use configured figure size if not provided
        if figsize is None:
            figsize = GRAPH_FIGSIZE_CUMULATIVE
        
        # Convert date strings to datetime objects for plotting
        dates_dt = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        # Create a new figure with specified size from configuration
        plt.figure(figsize=figsize)
        
        # Plot the data with markers
        plt.plot(dates_dt, values, marker='o', linewidth=2, markersize=4, color=color)
        
        # Set title and axis labels with configured text color
        plt.title(title, fontsize=14, fontweight='bold', color=TEXT_COLOR)
        plt.xlabel('Date', fontsize=12, color=TEXT_COLOR)
        plt.ylabel(ylabel, fontsize=12, color=TEXT_COLOR)
        
        # Add grid with configured color and transparency
        plt.grid(True, color=GRID_COLOR, alpha=0.3)
        
        # Format x-axis to show dates properly
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure with configured DPI
        plt.savefig(filename, dpi=GRAPH_DPI, bbox_inches='tight')
        
        # Close the figure to free memory
        plt.close()
        
    except Exception as e:
        # ERROR_CODE: GD006 - Graph creation error
        print(f"ERROR_CODE: GD006 - Error creating graph {filename}: {e}", file=sys.stderr)
        sys.exit(1)


def create_multi_line_graph(dates: List[str], clones: List[int], views: List[int], 
                            title: str, filename: str, figsize: Tuple[int, int] = None) -> None:
    """
    Create a multi-line graph showing both clones and views.
    
    This function creates a line graph with two lines: one for clones
    and one for views. Each line has a different color and marker style.
    Includes a legend to distinguish between the two metrics.
    
    Args:
        dates: List of date strings in 'YYYY-MM-DD' format
        clones: List of clone counts corresponding to each date
        views: List of view counts corresponding to each date
        title: Title for the graph
        filename: Path where the graph image will be saved
        figsize: Figure size as (width, height) tuple (uses GRAPH_FIGSIZE_DAILY if None)
        
    Raises:
        SystemExit: If graph creation fails (GD007)
    """
    try:
        # Check if we have data to plot
        if not dates or not clones or not views:
            print(f"WARNING: No data for graph: {title}")
            return
        
        # Use configured figure size if not provided
        if figsize is None:
            figsize = GRAPH_FIGSIZE_DAILY
        
        # Convert date strings to datetime objects for plotting
        dates_dt = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        # Create a new figure with specified size from configuration
        plt.figure(figsize=figsize)
        
        # Plot clones data with configured color and circle markers
        plt.plot(dates_dt, clones, marker='o', linewidth=2, markersize=4, 
                 color=CLONES_COLOR, label='Clones')
        
        # Plot views data with configured color and square markers
        plt.plot(dates_dt, views, marker='s', linewidth=2, markersize=4, 
                 color=VIEWS_COLOR, label='Views')
        
        # Set title and axis labels with configured text color
        plt.title(title, fontsize=14, fontweight='bold', color=TEXT_COLOR)
        plt.xlabel('Date', fontsize=12, color=TEXT_COLOR)
        plt.ylabel('Count', fontsize=12, color=TEXT_COLOR)
        
        # Add legend in upper left corner
        plt.legend(loc='upper left', fontsize=10)
        
        # Add grid with configured color and transparency
        plt.grid(True, color=GRID_COLOR, alpha=0.3)
        
        # Format x-axis to show dates properly
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure with configured DPI
        plt.savefig(filename, dpi=GRAPH_DPI, bbox_inches='tight')
        
        # Close the figure to free memory
        plt.close()
        
    except Exception as e:
        # ERROR_CODE: GD007 - Multi-line graph creation error
        print(f"ERROR_CODE: GD007 - Error creating graph {filename}: {e}", file=sys.stderr)
        sys.exit(1)


def generate_repository_graphs(repo_name: str, daily_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Generate all required graphs for a single repository.
    
    This function creates up to six types of graphs based on configuration:
    1. Daily traffic (configurable days) - shows daily clones and views
    2. Weekly traffic (configurable weeks) - shows weekly aggregates
    3. Bi-weekly traffic (configurable periods) - shows bi-weekly aggregates
    4. Cumulative traffic - shows running totals of both metrics (if INCLUDE_CUMULATIVE_GRAPHS)
    5. Cumulative clones only - separate cumulative graph for clones (if INCLUDE_SEPARATE_CUMULATIVE)
    6. Cumulative views only - separate cumulative graph for views (if INCLUDE_SEPARATE_CUMULATIVE)
    
    Args:
        repo_name: Full repository name (e.g., 'owner/repo')
        daily_data: List of daily data entries for the repository
        
    Returns:
        Dictionary mapping graph type to file path:
        - 'daily_30d': Path to daily graph
        - 'weekly_3m': Path to weekly graph
        - 'biweekly_1y': Path to bi-weekly graph
        - 'cumulative': Path to cumulative graph (if enabled)
        - 'cumulative_clones': Path to cumulative clones graph (if enabled)
        - 'cumulative_views': Path to cumulative views graph (if enabled)
    """
    # Create a safe filename by replacing '/' with '_'
    safe_repo_name = repo_name.replace('/', '_')
    graphs = {}
    
    # 1. Generate daily traffic graph (uses DAILY_GRAPH_DAYS configuration)
    daily_dates, daily_clones, daily_views = get_daily_data(daily_data, DAILY_GRAPH_DAYS)
    
    if daily_dates:
        # Create multi-line graph with clones and views using DAILY_GRAPH_DAYS
        create_multi_line_graph(
            daily_dates, daily_clones, daily_views,
            f'Daily Traffic ({DAILY_GRAPH_DAYS} Days) - {repo_name}',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_daily_{DAILY_GRAPH_DAYS}d.png',
            figsize=GRAPH_FIGSIZE_DAILY
        )
        # Store the graph filename
        graphs['daily'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_daily_{DAILY_GRAPH_DAYS}d.png'
    
    # 2. Generate weekly traffic graph (uses WEEKLY_GRAPH_WEEKS configuration)
    weekly_dates, weekly_clones, weekly_views = get_weekly_data(daily_data, WEEKLY_GRAPH_WEEKS)
    
    if weekly_dates:
        # Create multi-line graph with clones and views using WEEKLY_GRAPH_WEEKS
        create_multi_line_graph(
            weekly_dates, weekly_clones, weekly_views,
            f'Weekly Traffic ({WEEKLY_GRAPH_WEEKS} Weeks) - {repo_name}',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_weekly_{WEEKLY_GRAPH_WEEKS}m.png',
            figsize=GRAPH_FIGSIZE_WEEKLY
        )
        # Store the graph filename
        graphs['weekly'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_weekly_{WEEKLY_GRAPH_WEEKS}m.png'
    
    # 3. Generate bi-weekly traffic graph (uses BIWEEKLY_GRAPH_PERIODS configuration)
    biweekly_dates, biweekly_clones, biweekly_views = get_biweekly_data(daily_data, BIWEEKLY_GRAPH_PERIODS)
    
    if biweekly_dates:
        # Create multi-line graph with clones and views using BIWEEKLY_GRAPH_PERIODS
        create_multi_line_graph(
            biweekly_dates, biweekly_clones, biweekly_views,
            f'Bi-Weekly Traffic ({BIWEEKLY_GRAPH_PERIODS} Periods) - {repo_name}',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_biweekly_{BIWEEKLY_GRAPH_PERIODS}y.png',
            figsize=GRAPH_FIGSIZE_BIWEEKLY
        )
        # Store the graph filename
        graphs['biweekly'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_biweekly_{BIWEEKLY_GRAPH_PERIODS}y.png'
    
    # 4. Generate cumulative (additive) traffic graph (if INCLUDE_CUMULATIVE_GRAPHS enabled)
    cumulative_dates, cumulative_clones, cumulative_views = get_cumulative_data(daily_data)
    
    if cumulative_dates and INCLUDE_CUMULATIVE_GRAPHS:
        # Create multi-line graph with cumulative clones and views
        create_multi_line_graph(
            cumulative_dates, cumulative_clones, cumulative_views,
            f'Cumulative Traffic (Lifetime) - {repo_name}',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative.png',
            figsize=GRAPH_FIGSIZE_CUMULATIVE
        )
        # Store the graph filename
        graphs['cumulative'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative.png'
    
    # 5. Generate cumulative clones only graph (if INCLUDE_SEPARATE_CUMULATIVE enabled)
    if cumulative_dates and INCLUDE_SEPARATE_CUMULATIVE:
        create_graph(
            cumulative_dates, cumulative_clones,
            f'Cumulative Clones (Lifetime) - {repo_name}',
            'Total Clones',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative_clones.png',
            color=CLONES_COLOR,
            figsize=GRAPH_FIGSIZE_CUMULATIVE
        )
        # Store the graph filename
        graphs['cumulative_clones'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative_clones.png'
    
    # 6. Generate cumulative views only graph (if INCLUDE_SEPARATE_CUMULATIVE enabled)
    if cumulative_dates and INCLUDE_SEPARATE_CUMULATIVE:
        create_graph(
            cumulative_dates, cumulative_views,
            f'Cumulative Views (Lifetime) - {repo_name}',
            'Total Views',
            f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative_views.png',
            color=VIEWS_COLOR,
            figsize=GRAPH_FIGSIZE_CUMULATIVE
        )
        # Store the graph filename
        graphs['cumulative_views'] = f'{GRAPHS_DIRECTORY}/{safe_repo_name}_cumulative_views.png'
    
    # Return dictionary of all generated graphs
    return graphs


def calculate_referrer_stats(referrers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate referrer statistics from referrers data.
    
    This function processes referrer data to provide:
    - Total unique referrers
    - Referrers by count (sorted)
    - Total views from referrers
    - Total unique visitors from referrers
    
    Args:
        referrers_data: List of referrer entries from GitHub API
        
    Returns:
        Dictionary with referrer statistics including:
        - total_unique_referrers: Count of unique referrer sources
        - referrers_by_count: List of referrers sorted by total views
        - total_referrer_views: Sum of all views from referrers
        - total_referrer_uniques: Sum of all unique visitors from referrers
    """
    if not referrers_data:
        return {
            'total_unique_referrers': 0,
            'referrers_by_count': [],
            'total_referrer_views': 0,
            'total_referrer_uniques': 0
        }
    
    # Sort referrers by count (descending)
    referrers_sorted = sorted(referrers_data, key=lambda x: x.get('count', 0), reverse=True)
    
    # Calculate totals
    total_views = sum(r.get('count', 0) for r in referrers_data)
    total_uniques = sum(r.get('uniques', 0) for r in referrers_data)
    
    return {
        'total_unique_referrers': len(referrers_data),
        'referrers_by_count': referrers_sorted,
        'total_referrer_views': total_views,
        'total_referrer_uniques': total_uniques
    }


def calculate_repeat_vs_new_stats(daily_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """
    Calculate repeat visitors vs new visitors statistics.
    
    This function calculates:
    - Total views vs unique visitors for different time periods
    - Repeat visitors = Total views - Unique visitors
    - Shows engagement level and returning user behavior
    
    Args:
        daily_data: List of daily data entries
        
    Returns:
        Dictionary with statistics for different periods:
        - short_term: Last STATS_PERIOD_SHORT_TERM days
        - medium_term: Last STATS_PERIOD_MEDIUM_TERM days
        - lifetime: All available data
        Each period contains:
        - total_views: Total views in period
        - unique_visitors: Unique visitors in period
        - repeat_visitors: Repeat visitors (total - unique)
        - repeat_percentage: Percentage of repeat visitors
    """
    # Calculate for different periods
    stats_short = calculate_period_stats(daily_data, STATS_PERIOD_SHORT_TERM)
    stats_medium = calculate_period_stats(daily_data, STATS_PERIOD_MEDIUM_TERM)
    stats_lifetime = calculate_lifetime_stats(daily_data)
    
    def calculate_repeat_stats(stats: Dict[str, int]) -> Dict[str, Any]:
        """Calculate repeat visitor statistics from period stats."""
        total_views = stats.get('views_total', 0)
        unique_visitors = stats.get('views_unique', 0)
        repeat_visitors = total_views - unique_visitors
        
        # Calculate percentage (avoid division by zero)
        repeat_percentage = 0
        if total_views > 0:
            repeat_percentage = round((repeat_visitors / total_views) * 100, 1)
        
        return {
            'total_views': total_views,
            'unique_visitors': unique_visitors,
            'repeat_visitors': repeat_visitors,
            'repeat_percentage': repeat_percentage
        }
    
    return {
        'short_term': calculate_repeat_stats(stats_short),
        'medium_term': calculate_repeat_stats(stats_medium),
        'lifetime': calculate_repeat_stats(stats_lifetime)
    }


def calculate_repeat_vs_new_clones_stats(daily_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """
    Calculate repeat clones vs new clones statistics.

    This function calculates:
    - Total clones vs unique clones for different time periods
    - Repeat clones = Total clones - Unique clones
    - Shows repository adoption level and returning user behavior

    Args:
        daily_data: List of daily data entries

    Returns:
        Dictionary with statistics for different periods:
        - short_term: Last STATS_PERIOD_SHORT_TERM days
        - medium_term: Last STATS_PERIOD_MEDIUM_TERM days
        - lifetime: All available data
        Each period contains:
        - total_clones: Total clones in period
        - unique_clones: Unique clones in period
        - repeat_clones: Repeat clones (total - unique)
        - repeat_percentage: Percentage of repeat clones
    """
    # Calculate for different periods
    stats_short = calculate_period_stats(daily_data, STATS_PERIOD_SHORT_TERM)
    stats_medium = calculate_period_stats(daily_data, STATS_PERIOD_MEDIUM_TERM)
    stats_lifetime = calculate_lifetime_stats(daily_data)

    def calculate_repeat_clones_stats(stats: Dict[str, int]) -> Dict[str, Any]:
        """Calculate repeat clone statistics from period stats."""
        total_clones = stats.get('clones_total', 0)
        unique_clones = stats.get('clones_unique', 0)
        repeat_clones = total_clones - unique_clones

        # Calculate percentage (avoid division by zero)
        repeat_percentage = 0
        if total_clones > 0:
            repeat_percentage = round((repeat_clones / total_clones) * 100, 1)

        return {
            'total_clones': total_clones,
            'unique_clones': unique_clones,
            'repeat_clones': repeat_clones,
            'repeat_percentage': repeat_percentage
        }

    return {
        'short_term': calculate_repeat_clones_stats(stats_short),
        'medium_term': calculate_repeat_clones_stats(stats_medium),
        'lifetime': calculate_repeat_clones_stats(stats_lifetime)
    }


def generate_readme(history_data: Dict[str, Any]) -> None:
    """
    Generate the README.md file with statistics and embedded graphs.
    
    This function creates a comprehensive README.md that includes:
    - Dashboard title and description
    - Clickable index for quick navigation
    - Last updated timestamp
    - Per-repository sections with:
      - Clone statistics in table format (configurable periods)
      - Repeat vs New clone statistics
      - View statistics in table format (configurable periods)
      - Referrer statistics (total unique referrers, top referrers)
      - Repeat vs New visitor statistics
      - All generated graphs with descriptive titles and explanations
      - All generated graphs embedded as images
    
    Args:
        history_data: Dictionary containing the complete history data with
                      metadata and repositories sections
    """
    # Reference to user guide
    md = "See full Reference and Usage Guide at:\n"
    md += "https://soul-traveller.github.io/github-traffic-dashboard/\n\n"

    # Start with dashboard title and description
    md += "# \U0001f4ca GitHub Traffic Dashboard\n\n"
    md += "This dashboard tracks historical traffic data (clones and views) for GitHub repositories.\n\n"
    
    # Add last updated timestamp if available
    if 'metadata' in history_data:
        metadata = history_data['metadata']
        last_updated = metadata.get('last_updated', 'Unknown')
        md += f"**Last Updated:** {last_updated}\n\n"
    
    # Get all repositories from the history data
    repositories = history_data.get('repositories', {})
    
    # Generate clickable index for repositories
    if repositories:
        md += "## \U0001f4cb Table of Contents\n\n"
        md += "Quick navigation to repository statistics:\n\n"
        for repo_name in sorted(repositories.keys()):
            # Determine display name
            if SHOW_FULL_REPO_NAME:
                display_name = repo_name
            else:
                display_name = repo_name.split('/')[-1]
            # Create anchor link (replace spaces with hyphens, remove special chars)
            anchor = display_name.lower().replace(' ', '-').replace('_', '-')
            md += f"- [{display_name}](#{anchor})\n"
        md += "\n"
    
    # Process each repository
    for repo_name, repo_data in repositories.items():
        # Extract daily data and metadata for this repository
        daily_data = repo_data.get('daily_data', [])
        metadata = repo_data.get('metadata', {})
        referrers = repo_data.get('referrers', [])
        
        # Determine display name based on SHOW_FULL_REPO_NAME configuration
        if SHOW_FULL_REPO_NAME:
            display_name = repo_name
        else:
            # Extract only repository name (after the last '/')
            display_name = repo_name.split('/')[-1]
        
        # Create anchor for this repository
        anchor = display_name.lower().replace(' ', '-').replace('_', '-')
        
        # Add repository section header using configured header level
        header_prefix = '#' * README_HEADER_LEVEL
        md += f"{header_prefix} {display_name}\n\n"
        
        # Calculate statistics for different time periods using configuration
        # Short-term period (configurable via STATS_PERIOD_SHORT_TERM)
        stats_short = calculate_period_stats(daily_data, STATS_PERIOD_SHORT_TERM)
        # Medium-term period (configurable via STATS_PERIOD_MEDIUM_TERM)
        stats_medium = calculate_period_stats(daily_data, STATS_PERIOD_MEDIUM_TERM)
        # Lifetime (all available data)
        stats_lifetime = calculate_lifetime_stats(daily_data)
        
        # Calculate referrer statistics
        referrer_stats = calculate_referrer_stats(referrers)

        # Calculate repeat vs new visitor statistics
        repeat_stats = calculate_repeat_vs_new_stats(daily_data)

        # Calculate repeat vs new clone statistics
        repeat_clones_stats = calculate_repeat_vs_new_clones_stats(daily_data)

        # Add Clones section with emoji
        md += "### \U0001f5c5\ufe0f Clones\n\n"
        md += "*Repository clone statistics showing total and unique clones over different time periods.*\n\n"

        # Create professional table for clones statistics
        md += "| Period | Total | Unique |\n"
        md += "|--------|-------|--------|\n"
        md += f"| Last {STATS_PERIOD_SHORT_TERM} Days | {stats_short['clones_total']} | {stats_short['clones_unique']} |\n"
        md += f"| Last {STATS_PERIOD_MEDIUM_TERM} Days | {stats_medium['clones_total']} | {stats_medium['clones_unique']} |\n"
        md += f"| Lifetime | {stats_lifetime['clones_total']} | {stats_lifetime['clones_unique']} |\n\n"

        # Add Repeat vs New Clones section with emoji
        md += "### \U0001f4c4 Repeat vs New Clones\n\n"
        md += "*Analysis of repository adoption showing repeat clones vs new unique clones.*\n\n"
        md += "*Note: GitHub API does not provide geographical location data for cloners.*\n\n"

        # Create table for repeat vs new clone statistics
        md += "| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |\n"
        md += "|--------|--------------|----------------|----------------|----------|\n"
        md += f"| Last {STATS_PERIOD_SHORT_TERM} Days | {repeat_clones_stats['short_term']['total_clones']} | {repeat_clones_stats['short_term']['unique_clones']} | {repeat_clones_stats['short_term']['repeat_clones']} | {repeat_clones_stats['short_term']['repeat_percentage']}% |\n"
        md += f"| Last {STATS_PERIOD_MEDIUM_TERM} Days | {repeat_clones_stats['medium_term']['total_clones']} | {repeat_clones_stats['medium_term']['unique_clones']} | {repeat_clones_stats['medium_term']['repeat_clones']} | {repeat_clones_stats['medium_term']['repeat_percentage']}% |\n"
        md += f"| Lifetime | {repeat_clones_stats['lifetime']['total_clones']} | {repeat_clones_stats['lifetime']['unique_clones']} | {repeat_clones_stats['lifetime']['repeat_clones']} | {repeat_clones_stats['lifetime']['repeat_percentage']}% |\n\n"

        # Add Views section with emoji
        md += "### \U0001f440 Views\n\n"
        md += "*Repository view statistics showing total and unique views over different time periods.*\n\n"

        # Create professional table for views statistics
        md += "| Period | Total | Unique |\n"
        md += "|--------|-------|--------|\n"
        md += f"| Last {STATS_PERIOD_SHORT_TERM} Days | {stats_short['views_total']} | {stats_short['views_unique']} |\n"
        md += f"| Last {STATS_PERIOD_MEDIUM_TERM} Days | {stats_medium['views_total']} | {stats_medium['views_unique']} |\n"
        md += f"| Lifetime | {stats_lifetime['views_total']} | {stats_lifetime['views_unique']} |\n\n"
        
        # Add Referrers section with emoji
        md += "### \U0001f4de Referrers\n\n"
        md += "*Top referrer sources driving traffic to this repository.*\n\n"
        
        # Create table for referrer statistics
        md += f"**Total Unique Referrers:** {referrer_stats['total_unique_referrers']}\n\n"
        
        if referrer_stats['referrers_by_count']:
            md += "| Referrer | Total Views | Unique Visitors |\n"
            md += "|----------|-------------|----------------|\n"
            for ref in referrer_stats['referrers_by_count'][:10]:  # Show top 10
                referrer_name = ref.get('referrer', 'Unknown')
                count = ref.get('count', 0)
                uniques = ref.get('uniques', 0)
                md += f"| {referrer_name} | {count} | {uniques} |\n"
            md += "\n"
        else:
            md += "*No referrer data available.*\n\n"
        
        # Add Repeat vs New Visitors section with emoji
        md += "### \U0001f465 Repeat vs New Visitors\n\n"
        md += "*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*\n\n"
        md += "*Note: GitHub API does not provide geographical location data for visitors.*\n\n"
        
        # Create table for repeat vs new visitor statistics
        md += "| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |\n"
        md += "|--------|-------------|-----------------|-----------------|----------|\n"
        md += f"| Last {STATS_PERIOD_SHORT_TERM} Days | {repeat_stats['short_term']['total_views']} | {repeat_stats['short_term']['unique_visitors']} | {repeat_stats['short_term']['repeat_visitors']} | {repeat_stats['short_term']['repeat_percentage']}% |\n"
        md += f"| Last {STATS_PERIOD_MEDIUM_TERM} Days | {repeat_stats['medium_term']['total_views']} | {repeat_stats['medium_term']['unique_visitors']} | {repeat_stats['medium_term']['repeat_visitors']} | {repeat_stats['medium_term']['repeat_percentage']}% |\n"
        md += f"| Lifetime | {repeat_stats['lifetime']['total_views']} | {repeat_stats['lifetime']['unique_visitors']} | {repeat_stats['lifetime']['repeat_visitors']} | {repeat_stats['lifetime']['repeat_percentage']}% |\n\n"
        
        # Generate all graphs for this repository
        print(f"Generating graphs for {repo_name}...")
        graphs = generate_repository_graphs(repo_name, daily_data)
        
        # Add Graphs section with emoji
        md += "### \U0001f4c8 Traffic Graphs\n\n"
        md += "*Visual representations of traffic trends over different time periods.*\n\n"
        
        # Embed Daily Traffic graph if available
        if 'daily' in graphs:
            md += f"#### Daily Traffic ({DAILY_GRAPH_DAYS} Days)\n\n"
            md += f"*Shows daily clones and views trends for the last {DAILY_GRAPH_DAYS} days. Useful for identifying short-term patterns and recent activity spikes.*\n\n"
            md += f"![Daily {DAILY_GRAPH_DAYS} Days]({graphs['daily']})\n\n"
        
        # Embed Weekly Traffic graph if available
        if 'weekly' in graphs:
            md += f"#### Weekly Traffic ({WEEKLY_GRAPH_WEEKS} Weeks)\n\n"
            md += f"*Shows weekly aggregated clones and views for the last {WEEKLY_GRAPH_WEEKS} weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*\n\n"
            md += f"![Weekly {WEEKLY_GRAPH_WEEKS} Weeks]({graphs['weekly']})\n\n"
        
        # Embed Bi-Weekly Traffic graph if available
        if 'biweekly' in graphs:
            md += f"#### Bi-Weekly Traffic ({BIWEEKLY_GRAPH_PERIODS} Periods)\n\n"
            md += f"*Shows bi-weekly aggregated clones and views for the last {BIWEEKLY_GRAPH_PERIODS} periods (~1 year). Useful for identifying long-term trends and yearly patterns.*\n\n"
            md += f"![Bi-Weekly {BIWEEKLY_GRAPH_PERIODS} Periods]({graphs['biweekly']})\n\n"
        
        # Embed Cumulative Traffic graph if available and enabled
        if 'cumulative' in graphs and INCLUDE_CUMULATIVE_GRAPHS:
            md += "#### Cumulative Traffic (Lifetime)\n\n"
            md += "*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*\n\n"
            md += f"![Cumulative]({graphs['cumulative']})\n\n"
        
        # Embed separate cumulative graphs if available and enabled
        if 'cumulative_clones' in graphs and 'cumulative_views' in graphs and INCLUDE_SEPARATE_CUMULATIVE:
            md += "#### Separate Cumulative Graphs\n\n"
            md += "*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*\n\n"
            md += f"**Cumulative Clones:**\n\n"
            md += f"![Cumulative Clones]({graphs['cumulative_clones']})\n\n"
            md += f"**Cumulative Views:**\n\n"
            md += f"![Cumulative Views]({graphs['cumulative_views']})\n\n"
        
        # Add horizontal separator between repositories
        md += "---\n\n"
    
    # Add footer with automation note
    md += "*This dashboard is automatically updated daily using GitHub Actions.*\n"
    
    # Save the generated README.md using configured path
    save_file(md, README_FILE_PATH)


def main():
    """
    Main function to generate the GitHub traffic dashboard.
    
    This function orchestrates the entire dashboard generation process:
    1. Loads historical data from configured HISTORY_FILE_PATH
    2. Validates the data structure
    3. Prepares the graphs directory using GRAPHS_DIRECTORY
    4. Generates all graphs and statistics using configuration
    5. Updates README.md using configured README_FILE_PATH
    
    Raises:
        SystemExit: If any step fails (various error codes)
    """
    # Print start message
    print("Starting dashboard generation...")
    
    # Load the history data from configured HISTORY_FILE_PATH
    print(f"Loading {HISTORY_FILE_PATH}...")
    history_data = load_json_file(HISTORY_FILE_PATH)
    
    # Validate that the history data has the required structure
    # ERROR_CODE: GD008 - Missing repositories key
    if 'repositories' not in history_data:
        print("ERROR_CODE: GD008 - history.json missing 'repositories' key", file=sys.stderr)
        sys.exit(1)
    
    # Ensure the graphs directory exists using GRAPHS_DIRECTORY
    prepare_graphs_directory()
    
    # Generate README.md with all statistics and embedded graphs
    print(f"Generating {README_FILE_PATH} with graphs...")
    generate_readme(history_data)
    
    # Print completion message
    print("Dashboard generation completed successfully")


# Entry point: Run main() if this script is executed directly
if __name__ == '__main__':
    main()
