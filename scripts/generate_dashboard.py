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
        os.makedirs("graphs", exist_ok=True)
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
                 filename: str, color: str = 'blue') -> None:
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
        
    Raises:
        SystemExit: If graph creation fails (GD006)
    """
    try:
        # Check if we have data to plot
        if not dates or not values:
            print(f"WARNING: No data for graph: {title}")
            return
        
        # Convert date strings to datetime objects for plotting
        dates_dt = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        # Create a new figure with specified size
        plt.figure(figsize=(12, 6))
        
        # Plot the data with markers
        plt.plot(dates_dt, values, marker='o', linewidth=2, markersize=4, color=color)
        
        # Set title and axis labels
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        
        # Add grid with transparency
        plt.grid(True, alpha=0.3)
        
        # Format x-axis to show dates properly
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure with high DPI
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        
        # Close the figure to free memory
        plt.close()
        
    except Exception as e:
        # ERROR_CODE: GD006 - Graph creation error
        print(f"ERROR_CODE: GD006 - Error creating graph {filename}: {e}", file=sys.stderr)
        sys.exit(1)


def create_multi_line_graph(dates: List[str], clones: List[int], views: List[int], 
                            title: str, filename: str) -> None:
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
        
    Raises:
        SystemExit: If graph creation fails (GD007)
    """
    try:
        # Check if we have data to plot
        if not dates or not clones or not views:
            print(f"WARNING: No data for graph: {title}")
            return
        
        # Convert date strings to datetime objects for plotting
        dates_dt = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        # Create a new figure with specified size
        plt.figure(figsize=(12, 6))
        
        # Plot clones data with green color and circle markers
        plt.plot(dates_dt, clones, marker='o', linewidth=2, markersize=4, 
                 color='#2ecc71', label='Clones')
        
        # Plot views data with blue color and square markers
        plt.plot(dates_dt, views, marker='s', linewidth=2, markersize=4, 
                 color='#3498db', label='Views')
        
        # Set title and axis labels
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        
        # Add legend in upper left corner
        plt.legend(loc='upper left', fontsize=10)
        
        # Add grid with transparency
        plt.grid(True, alpha=0.3)
        
        # Format x-axis to show dates properly
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure with high DPI
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        
        # Close the figure to free memory
        plt.close()
        
    except Exception as e:
        # ERROR_CODE: GD007 - Multi-line graph creation error
        print(f"ERROR_CODE: GD007 - Error creating graph {filename}: {e}", file=sys.stderr)
        sys.exit(1)


def generate_repository_graphs(repo_name: str, daily_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Generate all required graphs for a single repository.
    
    This function creates six types of graphs:
    1. Daily traffic (30 days) - shows daily clones and views
    2. Weekly traffic (3 months) - shows weekly aggregates
    3. Bi-weekly traffic (1 year) - shows bi-weekly aggregates
    4. Cumulative traffic - shows running totals of both metrics
    5. Cumulative clones only - separate cumulative graph for clones
    6. Cumulative views only - separate cumulative graph for views
    
    Args:
        repo_name: Full repository name (e.g., 'owner/repo')
        daily_data: List of daily data entries for the repository
        
    Returns:
        Dictionary mapping graph type to file path:
        - 'daily_30d': Path to daily 30-day graph
        - 'weekly_3m': Path to weekly 3-month graph
        - 'biweekly_1y': Path to bi-weekly 1-year graph
        - 'cumulative': Path to cumulative graph
        - 'cumulative_clones': Path to cumulative clones graph
        - 'cumulative_views': Path to cumulative views graph
    """
    # Create a safe filename by replacing '/' with '_'
    safe_repo_name = repo_name.replace('/', '_')
    graphs = {}
    
    # 1. Generate daily traffic graph (30 days with daily intervals)
    # This shows the most recent 30 days of traffic data
    daily_dates, daily_clones, daily_views = get_daily_data(daily_data, 30)
    
    if daily_dates:
        # Create multi-line graph with clones and views
        create_multi_line_graph(
            daily_dates, daily_clones, daily_views,
            f'Daily Traffic (30 Days) - {repo_name}',
            f'graphs/{safe_repo_name}_daily_30d.png'
        )
        # Store the graph filename
        graphs['daily_30d'] = f'graphs/{safe_repo_name}_daily_30d.png'
    
    # 2. Generate weekly traffic graph (3 months with weekly intervals)
    # This aggregates data into weeks for the last 3 months (12 weeks)
    weekly_dates, weekly_clones, weekly_views = get_weekly_data(daily_data, 12)
    
    if weekly_dates:
        # Create multi-line graph with clones and views
        create_multi_line_graph(
            weekly_dates, weekly_clones, weekly_views,
            f'Weekly Traffic (3 Months) - {repo_name}',
            f'graphs/{safe_repo_name}_weekly_3m.png'
        )
        # Store the graph filename
        graphs['weekly_3m'] = f'graphs/{safe_repo_name}_weekly_3m.png'
    
    # 3. Generate bi-weekly traffic graph (1 year with bi-weekly intervals)
    # This aggregates data into 2-week periods for the last year (26 periods)
    biweekly_dates, biweekly_clones, biweekly_views = get_biweekly_data(daily_data, 26)
    
    if biweekly_dates:
        # Create multi-line graph with clones and views
        create_multi_line_graph(
            biweekly_dates, biweekly_clones, biweekly_views,
            f'Bi-Weekly Traffic (1 Year) - {repo_name}',
            f'graphs/{safe_repo_name}_biweekly_1y.png'
        )
        # Store the graph filename
        graphs['biweekly_1y'] = f'graphs/{safe_repo_name}_biweekly_1y.png'
    
    # 4. Generate cumulative (additive) traffic graph
    # This shows running totals over the entire lifetime
    cumulative_dates, cumulative_clones, cumulative_views = get_cumulative_data(daily_data)
    
    if cumulative_dates:
        # Create multi-line graph with cumulative clones and views
        create_multi_line_graph(
            cumulative_dates, cumulative_clones, cumulative_views,
            f'Cumulative Traffic (Lifetime) - {repo_name}',
            f'graphs/{safe_repo_name}_cumulative.png'
        )
        # Store the graph filename
        graphs['cumulative'] = f'graphs/{safe_repo_name}_cumulative.png'
    
    # 5. Generate cumulative clones only graph
    # Separate graph showing only cumulative clones over time
    if cumulative_dates:
        create_graph(
            cumulative_dates, cumulative_clones,
            f'Cumulative Clones (Lifetime) - {repo_name}',
            'Total Clones',
            f'graphs/{safe_repo_name}_cumulative_clones.png',
            color='#2ecc71'  # Green color for clones
        )
        # Store the graph filename
        graphs['cumulative_clones'] = f'graphs/{safe_repo_name}_cumulative_clones.png'
    
    # 6. Generate cumulative views only graph
    # Separate graph showing only cumulative views over time
    if cumulative_dates:
        create_graph(
            cumulative_dates, cumulative_views,
            f'Cumulative Views (Lifetime) - {repo_name}',
            'Total Views',
            f'graphs/{safe_repo_name}_cumulative_views.png',
            color='#3498db'  # Blue color for views
        )
        # Store the graph filename
        graphs['cumulative_views'] = f'graphs/{safe_repo_name}_cumulative_views.png'
    
    # Return dictionary of all generated graphs
    return graphs


def generate_readme(history_data: Dict[str, Any]) -> None:
    """
    Generate the README.md file with statistics and embedded graphs.
    
    This function creates a comprehensive README.md that includes:
    - Dashboard title and description
    - Last updated timestamp
    - Per-repository sections with:
      - Clone statistics (30 days, 90 days, lifetime)
      - View statistics (30 days, 90 days, lifetime)
      - All generated graphs embedded as images
    
    Args:
        history_data: Dictionary containing the complete history data with
                      metadata and repositories sections
    """
    # Start with dashboard title and description
    md = "# \U0001f4ca GitHub Traffic Dashboard\n\n"
    md += "This dashboard tracks historical traffic data (clones and views) for GitHub repositories.\n\n"
    
    # Add last updated timestamp if available
    if 'metadata' in history_data:
        metadata = history_data['metadata']
        last_updated = metadata.get('last_updated', 'Unknown')
        md += f"**Last Updated:** {last_updated}\n\n"
    
    # Get all repositories from the history data
    repositories = history_data.get('repositories', {})
    
    # Process each repository
    for repo_name, repo_data in repositories.items():
        # Extract daily data and metadata for this repository
        daily_data = repo_data.get('daily_data', [])
        metadata = repo_data.get('metadata', {})
        
        # Add repository section header
        md += f"## {repo_name}\n\n"
        
        # Calculate statistics for different time periods
        # 30 days (1 month)
        stats_30d = calculate_period_stats(daily_data, 30)
        # 90 days (3 months)
        stats_90d = calculate_period_stats(daily_data, 90)
        # Lifetime (all available data)
        stats_lifetime = calculate_lifetime_stats(daily_data)
        
        # Add Clones section with emoji
        md += "### \U0001f5c5\ufe0f Clones\n\n"
        
        # Last 30 Days statistics
        md += "**Last 30 Days:**\n"
        md += f"- Total: **{stats_30d['clones_total']}**\n"
        md += f"- Unique: **{stats_30d['clones_unique']}**\n\n"
        
        # Last 90 Days (3 Months) statistics
        md += "**Last 90 Days (3 Months):**\n"
        md += f"- Total: **{stats_90d['clones_total']}**\n"
        md += f"- Unique: **{stats_90d['clones_unique']}**\n\n"
        
        # Lifetime statistics
        md += "**Lifetime:**\n"
        md += f"- Total: **{stats_lifetime['clones_total']}**\n"
        md += f"- Unique: **{stats_lifetime['clones_unique']}**\n\n"
        
        # Add Views section with emoji
        md += "### \U0001f440 Views\n\n"
        
        # Last 30 Days statistics
        md += "**Last 30 Days:**\n"
        md += f"- Total: **{stats_30d['views_total']}**\n"
        md += f"- Unique: **{stats_30d['views_unique']}**\n\n"
        
        # Last 90 Days (3 Months) statistics
        md += "**Last 90 Days (3 Months):**\n"
        md += f"- Total: **{stats_90d['views_total']}**\n"
        md += f"- Unique: **{stats_90d['views_unique']}**\n\n"
        
        # Lifetime statistics
        md += "**Lifetime:**\n"
        md += f"- Total: **{stats_lifetime['views_total']}**\n"
        md += f"- Unique: **{stats_lifetime['views_unique']}**\n\n"
        
        # Generate all graphs for this repository
        print(f"Generating graphs for {repo_name}...")
        graphs = generate_repository_graphs(repo_name, daily_data)
        
        # Add Graphs section with emoji
        md += "### \U0001f4c8 Graphs\n\n"
        
        # Embed Daily Traffic graph if available
        if 'daily_30d' in graphs:
            md += f"**Daily Traffic (30 Days):**\n\n"
            md += f"![Daily 30 Days]({graphs['daily_30d']})\n\n"
        
        # Embed Weekly Traffic graph if available
        if 'weekly_3m' in graphs:
            md += f"**Weekly Traffic (3 Months):**\n\n"
            md += f"![Weekly 3 Months]({graphs['weekly_3m']})\n\n"
        
        # Embed Bi-Weekly Traffic graph if available
        if 'biweekly_1y' in graphs:
            md += f"**Bi-Weekly Traffic (1 Year):**\n\n"
            md += f"![Bi-Weekly 1 Year]({graphs['biweekly_1y']})\n\n"
        
        # Embed Cumulative Traffic graph if available
        if 'cumulative' in graphs:
            md += f"**Cumulative Traffic (Lifetime):**\n\n"
            md += f"![Cumulative]({graphs['cumulative']})\n\n"
        
        # Embed separate cumulative graphs if available
        if 'cumulative_clones' in graphs and 'cumulative_views' in graphs:
            md += "**Separate Cumulative Graphs:**\n\n"
            md += f"![Cumulative Clones]({graphs['cumulative_clones']})\n\n"
            md += f"![Cumulative Views]({graphs['cumulative_views']})\n\n"
        
        # Add horizontal separator between repositories
        md += "---\n\n"
    
    # Add footer with automation note
    md += "*This dashboard is automatically updated daily using GitHub Actions.*\n"
    
    # Save the generated README.md
    save_file(md, "README.md")


def main():
    """
    Main function to generate the GitHub traffic dashboard.
    
    This function orchestrates the entire dashboard generation process:
    1. Loads historical data from history.json
    2. Validates the data structure
    3. Prepares the graphs directory
    4. Generates all graphs and statistics
    5. Updates README.md with the new content
    
    Raises:
        SystemExit: If any step fails (various error codes)
    """
    # Print start message
    print("Starting dashboard generation...")
    
    # Load the history data from history.json
    print("Loading history.json...")
    history_data = load_json_file("history.json")
    
    # Validate that the history data has the required structure
    # ERROR_CODE: GD008 - Missing repositories key
    if 'repositories' not in history_data:
        print("ERROR_CODE: GD008 - history.json missing 'repositories' key", file=sys.stderr)
        sys.exit(1)
    
    # Ensure the graphs directory exists
    prepare_graphs_directory()
    
    # Generate README.md with all statistics and embedded graphs
    print("Generating README.md with graphs...")
    generate_readme(history_data)
    
    # Print completion message
    print("Dashboard generation completed successfully")


# Entry point: Run main() if this script is executed directly
if __name__ == '__main__':
    main()
