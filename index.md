# GitHub Traffic Dashboard - User Guide

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage Guide](#usage-guide)
  - [Daily Operation](#daily-operation)
  - [Manual Trigger](#manual-trigger)
  - [Understanding the Output](#understanding-the-output)
- [Cloning and Reusing](#cloning-and-reusing)
  - [For New Users](#for-new-users)
  - [File Structure](#file-structure)
  - [Files to Keep](#files-to-keep)
  - [Generated Files](#generated-files)
  - [Renaming Your Repository](#renaming-your-repository)
  - [Adapting Configuration](#adapting-configuration)
- [Configuration Details](#configuration-details)
  - [Workflow Configuration](#workflow-configuration)
  - [Python Script Configuration](#python-script-configuration)
  - [Graph Customization](#graph-customization)
- [Features](#features)
  - [Automatic Data Collection](#automatic-data-collection)
  - [Graph Generation](#graph-generation)
  - [Statistics Calculation](#statistics-calculation)
  - [Server Downtime Handling](#server-downtime-handling)
  - [Calendar Edge Cases](#calendar-edge-cases)
- [Error Handling](#error-handling)
  - [Error Codes](#error-codes)
  - [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
  - [Adding Repositories](#adding-repositories)
  - [Updating Configuration](#updating-configuration)
  - [Monitoring](#monitoring)
- [Technical Details](#technical-details)
  - [Data Format](#data-format)
  - [Technical Stack](#technical-stack)
  - [Dependencies](#dependencies)
- [Limitations](#limitations)
- [License and Credits](#license-and-credits)

---

## Overview

The **GitHub Traffic Dashboard** is a production-ready solution for automatically tracking and visualizing GitHub repository traffic statistics (clones and views) over time. It provides:

- **Automatic Data Collection**: Runs daily via GitHub Actions to fetch traffic data from GitHub API
- **Professional Graphs**: Generates 6 types of graphs for each repository (daily, weekly, bi-weekly, cumulative)
- **Detailed Statistics**: Calculates statistics for 30 days, 90 days, and lifetime
- **Robust Error Handling**: Comprehensive error codes and clear error messages
- **Server Downtime Recovery**: Automatically recovers up to 14 days of missed data
- **Calendar Edge Case Handling**: Correctly handles year transitions, leap years, and month boundaries
- **Scalable Architecture**: Easy to add multiple repositories with minimal configuration

### What It Does

1. **Fetches Data**: Daily at 2 AM UTC, the workflow fetches traffic data (clones, views, referrers) from GitHub API
2. **Merges Data**: New data is merged with historical data, with zero-filling for missing dates
3. **Generates Graphs**: Creates professional graphs showing traffic trends over different time periods
4. **Calculates Statistics**: Computes totals and unique counts for 30 days, 90 days, and lifetime
5. **Updates Dashboard**: Automatically updates README.md with statistics and embedded graph images

### Key Benefits

- **Zero Maintenance**: Runs automatically once configured
- **Data Integrity**: Zero-filling ensures no gaps in historical data
- **Recovery**: Automatic recovery from server downtime (up to 14 days)
- **Professional Output**: Clean, publication-ready graphs and statistics
- **Easy to Scale**: Add unlimited repositories with simple configuration
- **Standards-Based**: Compatible with github-repo-stats principles

---

## Quick Start

Get started in 3 simple steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/soul-traveller/github-traffic-dashboard.git
   cd github-traffic-dashboard
   ```

2. **Configure your repositories**
   - Edit `.github/workflows/main.yml`
   - Add your repositories in the `repos` array (lines 156-160)
   - Example: `"your-username/your-repo"`

3. **Set up GitHub secret**
   - Go to repository Settings > Secrets and variables > Actions
   - Create a new secret named `TRAFFIC_ACTION_TOKEN`
   - Generate a Personal Access Token with `repo` scope and paste it

That's it! The workflow will run automatically at 2 AM UTC and start collecting data.

---

## Getting Started

### Prerequisites

Before using the GitHub Traffic Dashboard, ensure you have:

- **GitHub Account**: To create repositories and access GitHub Actions
- **GitHub Personal Access Token**: With `repo` scope permissions
- **Python 3.x**: For running scripts locally (optional, not required for GitHub Actions)
- **Basic Git Knowledge**: For cloning and managing repositories

### Installation

#### Option 1: Clone and Use (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/soul-traveller/github-traffic-dashboard.git
   cd github-traffic-dashboard
   ```

2. Configure your repositories (see [Configuration](#configuration))

3. Set up GitHub secret (see [Quick Start](#quick-start))

4. Push to your GitHub repository:
   ```bash
   git remote set-url origin https://github.com/your-username/your-repo.git
   git add .
   git commit -m "Initial setup"
   git push
   ```

5. Enable GitHub Actions in repository settings

#### Option 2: Fork and Customize

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/github-traffic-dashboard.git
   cd github-traffic-dashboard
   ```

3. Follow steps 2-5 from Option 1

### Configuration

#### Step 1: Configure Repositories in Workflow

Edit `.github/workflows/main.yml` and update the repository list:

```yaml
# Find this section (around line 147-160)
repos=(
  "your-username/repository-1"
  "your-username/repository-2"
  "your-username/repository-3"
)
```

**Important Notes:**
- Each repository must be in format: `"owner/repository-name"`
- You can add as many repositories as needed
- Each repository will get the same professional output
- The workflow automatically handles all configured repositories

#### Step 2: Create GitHub Secret

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token" (classic)
3. Select `repo` scope (this is required)
4. Generate the token and copy it
5. Go to your repository Settings > Secrets and variables > Actions
6. Click "New repository secret"
7. Name: `TRAFFIC_ACTION_TOKEN`
8. Value: Paste your token
9. Click "Add secret"

#### Step 3: Enable GitHub Actions

1. Go to repository Settings > Actions > General
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Click "Save"

#### Step 4: Verify Configuration

1. Go to the Actions tab in your repository
2. Click "GitHub Traffic Dashboard" workflow
3. Click "Run workflow" to test manually
4. Check the workflow logs for any errors

---

## Usage Guide

### Daily Operation

Once configured, the dashboard operates automatically:

- **Schedule**: Runs daily at 2 AM UTC (end of day in most timezones)
- **Process**:
  1. Fetches traffic data from GitHub API (last 14 days)
  2. Merges with existing historical data
  3. Generates graphs for each repository
  4. Calculates statistics
  5. Updates README.md
  6. Commits changes to repository

- **Result**: You'll see updated graphs and statistics in your README.md every day

### Manual Trigger

You can manually trigger the workflow at any time:

1. Go to the Actions tab
2. Select "GitHub Traffic Dashboard" workflow
3. Click "Run workflow" button
4. Select branch (usually `main`)
5. Click "Run workflow"

This is useful for:
- Testing configuration changes
- Immediate updates after adding new repositories
- Troubleshooting issues

### Understanding the Output

#### README.md Structure

Your README.md will contain:

```
# Repository Name

### 🗅️ Clones

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | X | Y |
| Last 90 Days | X | Y |
| Lifetime | X | Y |

### 👀 Views

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | X | Y |
| Last 90 Days | X | Y |
| Lifetime | X | Y |

### 📈 Graphs

![Daily Traffic](graphs/repo_daily_30d.png)
![Weekly Traffic](graphs/repo_weekly_3m.png)
![Bi-Weekly Traffic](graphs/repo_biweekly_1y.png)
![Cumulative Traffic](graphs/repo_cumulative.png)
```

**Note:** Statistics are displayed in professional table format for easy comparison and readability.

#### Graph Types

1. **Daily Traffic (30 Days)**: Shows daily clones and views for the last 30 days
2. **Weekly Traffic (3 Months)**: Shows weekly aggregates for 12 weeks
3. **Bi-Weekly Traffic (1 Year)**: Shows bi-weekly aggregates for 26 periods
4. **Cumulative Traffic**: Shows running totals of both clones and views
5. **Cumulative Clones**: Separate cumulative graph for clones only
6. **Cumulative Views**: Separate cumulative graph for views only

#### Statistics Explained

- **Total**: Sum of all clones/views in the period
- **Unique**: Count of unique users who cloned/viewed
- **Last 30 days**: Short-term trends
- **Last 90 days**: Medium-term trends
- **Lifetime**: All-time totals

---

## Cloning and Reusing

### For New Users

This dashboard is designed to be easily cloned and reused for your own repositories. Follow this step-by-step guide:

### File Structure

```
github-traffic-dashboard/
|-- .github/
|   |-- workflows/
|       |-- main.yml              # Main workflow (EDIT THIS)
|-- scripts/
|   |-- generate_dashboard.py     # Graph generation (CONFIGURATION AT TOP)
|   |-- merge_history.py         # Data merging (CONFIGURATION AT TOP)
|-- graphs/                      # GENERATED (created on first run)
|-- history.json                 # GENERATED (created on first run)
|-- README.md                    # GENERATED (updated on each run)
|-- _config.yml                  # Jekyll configuration (OPTIONAL)
|-- index.md                     # This user guide (KEEP)
|-- DOWNTIME_HANDLING.md         # Downtime documentation (KEEP)
```

### Files to Keep

**Essential Files (Do Not Delete):**
- `.github/workflows/main.yml` - Main workflow configuration
- `scripts/generate_dashboard.py` - Graph generation script
- `scripts/merge_history.py` - Data merging script
- `index.md` - This user guide
- `DOWNTIME_HANDLING.md` - Downtime handling documentation
- `_config.yml` - Jekyll configuration (if using GitHub Pages)

**Optional Files:**
- `LICENSE` - License file
- `robots.txt` - SEO file
- `google80c63b7cde90aebc.html` - Google verification (if needed)

### Generated Files

**Auto-Generated (Do Not Edit):**
- `history.json` - Historical traffic data (created on first run)
- `README.md` - Dashboard output (updated on each run)
- `graphs/` - Directory containing all graph images (created on first run)

**Important Notes:**
- These files are automatically generated and overwritten
- Do not manually edit them (changes will be lost on next run)
- They will be created automatically on the first workflow run
- Commit them to your repository to preserve history

### Renaming Your Repository

When cloning for your own use, you can safely rename the repository. Here's how:

#### Step 1: Rename on GitHub

1. Go to your repository on GitHub
2. Click Settings > General
3. Under "Repository name", enter your new name
4. Click "Rename"

#### Step 2: Update Git Remote

```bash
cd github-traffic-dashboard
git remote set-url origin https://github.com/your-username/your-new-repo-name.git
git push -u origin main
```

#### Step 3: No Code Changes Required!

**Important:** You do NOT need to change any code in:
- `.github/workflows/main.yml`
- `scripts/generate_dashboard.py`
- `scripts/merge_history.py`

The repository name is only used for:
- GitHub URL (handled automatically)
- Git remote (updated in step 2)

### Adapting Configuration

#### For Your User and Repositories

**Step 1: Edit Workflow Repository List**

Edit `.github/workflows/main.yml` (around line 147-160):

```yaml
# BEFORE (example repositories)
repos=(
  "soul-traveller/Argyll_Printer_Profiler"
  "soul-traveller/Toggle_Display_Profile"
  "soul-traveller/rectarg"
)

# AFTER (your repositories)
repos=(
  "your-username/your-repo-1"
  "your-username/your-repo-2"
  "your-username/your-repo-3"
)
```

**Step 2: No Changes Needed in Python Scripts**

The Python scripts (`generate_dashboard.py` and `merge_history.py`) automatically:
- Read repository names from `history.json`
- Generate graphs for all repositories found
- Update README.md for all repositories

**Step 3: Configuration Options (Optional)**

If you want to customize behavior, you can edit the configuration sections:

**In `scripts/generate_dashboard.py` (lines 14-64):**
- Graph dimensions
- Colors
- Time periods
- Display options

**In `scripts/merge_history.py` (lines 33-69):**
- Zero-filling settings
- Data retention limits
- Merge strategy options

**In `.github/workflows/main.yml` (lines 7-53):**
- Workflow schedule
- API settings
- Timezone

#### Example: Complete Setup for New User

```bash
# 1. Clone the repository
git clone https://github.com/soul-traveller/github-traffic-dashboard.git my-traffic-dashboard
cd my-traffic-dashboard

# 2. Edit workflow with your repositories
# Edit .github/workflows/main.yml, line 147-160:
repos=(
  "john-doe/awesome-project"
  "john-doe/cool-library"
  "john-doe/useful-tool"
)

# 3. Create new repository on GitHub (named "my-traffic-dashboard")

# 4. Update git remote
git remote set-url origin https://github.com/john-doe/my-traffic-dashboard.git

# 5. Commit and push
git add .
git commit -m "Setup for john-doe repositories"
git push -u origin main

# 6. Go to GitHub and set up TRAFFIC_ACTION_TOKEN secret

# 7. Enable GitHub Actions in repository settings

# 8. Manually trigger workflow to test
# (Go to Actions tab > GitHub Traffic Dashboard > Run workflow)
```

---

## Configuration Details

### Workflow Configuration

The workflow configuration is at the top of `.github/workflows/main.yml` (lines 7-53):

```yaml
# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS FOR YOUR REPOSITORIES
# ============================================================================

# QUICK SETUP GUIDE:
# 1. GitHub Secret Token: Create a secret named TRAFFIC_ACTION_TOKEN with 'repo' scope
#    (Settings > Secrets and variables > Actions > New repository secret)
# 2. Repository List: Edit the REPOS array below with your repositories
# 3. Workflow Schedule: Edit the cron expression if needed (default: daily at 2 AM UTC)
```

#### Repository List (Lines 147-160)

```yaml
repos=(
  "your-username/your-repo-1"
  "your-username/your-repo-2"
)
```

**Format:** `"owner/repository-name"`

**Tips:**
- Add one repository per line
- Use your GitHub username as owner
- Repository name must match exactly (case-sensitive)
- You can track repositories owned by others (if public)

#### Workflow Schedule (Line 37)

```yaml
schedule:
  - cron: "0 2 * * *"   # every day at 2 AM UTC
```

**Common Schedules:**
- `"0 2 * * *"` - Daily at 2 AM UTC (default)
- `"0 */6 * * *"` - Every 6 hours
- `"0 0 * * 0"` - Weekly on Sunday at midnight UTC
- `"0 12 * * 1"` - Weekly on Monday at noon UTC

**Format:** `minute hour day month day-of-week`

#### API Configuration (Lines 50-53)

```yaml
env:
  GITHUB_API_BASE_URL: "https://api.github.com"
  GITHUB_API_VERSION: "2022-11-28"
  TIMEZONE: "UTC"
```

**Note:** These rarely need to be changed.

### Python Script Configuration

Both Python scripts have configuration sections at the top with clear guidance.

#### generate_dashboard.py (Lines 14-64)

```python
# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS FOR YOUR NEEDS
# ============================================================================

# File Paths Configuration
HISTORY_FILE_PATH = "history.json"           # Path to historical traffic data
README_FILE_PATH = "README.md"               # Path to README file to update
GRAPHS_DIRECTORY = "graphs"                  # Directory for storing graph images

# Graph Configuration
GRAPH_DPI = 100                              # Dots per inch for graph quality
GRAPH_FIGSIZE_DAILY = (12, 6)                # Dimensions for daily graphs (width, height)
GRAPH_FIGSIZE_WEEKLY = (14, 6)               # Dimensions for weekly graphs
GRAPH_FIGSIZE_BIWEEKLY = (16, 6)             # Dimensions for bi-weekly graphs
GRAPH_FIGSIZE_CUMULATIVE = (14, 6)           # Dimensions for cumulative graphs

# Time Period Configuration
DAILY_GRAPH_DAYS = 30                        # Days to show in daily graphs
WEEKLY_GRAPH_WEEKS = 12                     # Weeks to show in weekly graphs (3 months)
BIWEEKLY_GRAPH_PERIODS = 26                 # Bi-weekly periods to show (1 year)

# Statistics Periods
STATS_PERIOD_30_DAYS = 30                   # Short-term statistics period
STATS_PERIOD_90_DAYS = 90                   # Medium-term statistics period

# Graph Style Configuration
CLONES_COLOR = "#2196F3"                    # Blue for clones
VIEWS_COLOR = "#4CAF50"                     # Green for views
GRID_COLOR = "#E0E0E0"                      # Light gray for grid lines
TEXT_COLOR = "#333333"                      # Dark gray for text

# Repository Display Configuration
SHOW_FULL_REPO_NAME = False                  # If False, shows only repository name

# README Generation Configuration
README_HEADER_LEVEL = 1                      # Markdown header level for repository names (1-6)
INCLUDE_CUMULATIVE_GRAPHS = True            # Whether to include cumulative graphs
INCLUDE_SEPARATE_CUMULATIVE = True          # Whether to include separate clones/views cumulative graphs
```

**All 21 configuration parameters are actively used and affect the dashboard behavior.**

#### merge_history.py (Lines 33-69)

```python
# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS FOR YOUR NEEDS
# ============================================================================

# File Paths Configuration
DEFAULT_HISTORY_FILE = "history.json"           # Path to existing historical data
DEFAULT_NEW_DATA_FILE = "traffic_data.json"     # Path to newly fetched data
DEFAULT_OUTPUT_FILE = "merged_history.json"     # Path for merged output

# Data Handling Configuration
ZERO_FILL_ENABLED = True                       # Whether to fill missing dates with zeros
ZERO_FILL_START_OFFSET_DAYS = 365              # Days before earliest data to start zero-filling
RECALCULATE_TOTALS = True                      # Whether to recalculate totals after merge
VALIDATE_STRUCTURE = True                      # Whether to validate JSON structure

# Date Configuration
TIMEZONE = "UTC"                               # Timezone for all date calculations
DATE_FORMAT = "%Y-%m-%d"                       # Date format for string representation
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"        # DateTime format for timestamps

# Data Retention Configuration
MAX_HISTORY_DAYS = 365                         # Maximum days of history to retain
# Set to None to keep all data (no limit)

# Merge Strategy Configuration
NEW_DATA_TAKES_PRECEDENCE = True               # New data overwrites existing data for same date
KEEP_OLD_METADATA_IF_NEW_MISSING = True       # Keep old metadata if new data doesn't have it
```

**All merge_history.py configuration parameters are actively used and affect data merging behavior.**

### Graph Customization

You can customize graph appearance by editing the configuration in `scripts/generate_dashboard.py`:

#### Colors

```python
CLONES_COLOR = "#2196F3"  # Blue for clones
VIEWS_COLOR = "#4CAF50"   # Green for views
```

Use any valid hex color code.

#### Dimensions

```python
GRAPH_FIGSIZE_DAILY = (12, 6)  # Width, Height in inches
```

Larger values = larger graphs.

#### Quality

```python
GRAPH_DPI = 100  # Dots per inch
```

Higher values = higher quality but larger files.

#### Time Periods

```python
DAILY_GRAPH_DAYS = 30        # Days in daily graphs
WEEKLY_GRAPH_WEEKS = 12      # Weeks in weekly graphs
BIWEEKLY_GRAPH_PERIODS = 26  # Periods in bi-weekly graphs
```

---

## Features

### Automatic Data Collection

The dashboard automatically collects data every day:

- **Schedule**: 2 AM UTC (end of day in most timezones)
- **Data Types**: Clones, views, referrers
- **Source**: GitHub Traffic API
- **Retention**: Last 14 days from API, merged with historical data
- **Zero-Filling**: Ensures no gaps in historical record

### Graph Generation

For each repository, 6 types of graphs are created:

1. **Daily Traffic (30 Days)**: Daily intervals showing short-term trends
2. **Weekly Traffic (3 Months)**: Weekly aggregates showing medium-term trends
3. **Bi-Weekly Traffic (1 Year)**: Bi-weekly aggregates showing long-term trends
4. **Cumulative Traffic**: Running totals of both clones and views
5. **Cumulative Clones**: Separate cumulative graph for clones
6. **Cumulative Views**: Separate cumulative graph for views

All graphs are:
- Publication-ready quality
- Consistently styled
- Properly labeled
- Embedded in README.md

### Statistics Calculation

Statistics are calculated for three time periods:

**30 Days:**
- Total clones
- Unique clones
- Total views
- Unique views

**90 Days:**
- Total clones
- Unique clones
- Total views
- Unique views

**Lifetime:**
- Total clones
- Unique clones
- Total views
- Unique views

All statistics are displayed in README.md with clear formatting.

### Server Downtime Handling

The dashboard automatically handles server downtime:

**Automatic Detection:**
- Workflow detects when it hasn't run recently
- Calculates days since last successful run
- Logs warnings for missed runs
- Includes recovery information in commit messages

**Automatic Recovery:**
- GitHub API provides last 14 days of data
- Missed days are automatically recovered on next run
- Up to 14 consecutive days can be recovered without data loss
- Zero-filling ensures no gaps in historical record

**Example:**
```
Day 1: Server down - no data collected
Day 2: Workflow runs - API provides data for Day 1 and Day 2
Result: Both days have correct data in history.json
```

### Calendar Edge Cases

The dashboard correctly handles all calendar edge cases:

**Year Transitions:**
- December 31 to January 1
- Date sorting works correctly across year boundaries
- Zero-filling generates all dates regardless of year boundary

**Leap Years:**
- February 29 is handled automatically
- Python's datetime module manages varying month lengths
- No special logic needed

**Month Boundaries:**
- January 31 to February 1
- All date arithmetic uses UTC timezone
- Consistent behavior across all months

---

## Error Handling

### Error Codes

All error codes follow the format: `MODULE-CODE`

#### Workflow Errors

- **TF001**: Failed to fetch clones data
- **TF002**: Failed to fetch views data
- **TF003**: Failed to fetch referrers data
- **JV001**: Invalid clones JSON structure
- **JV002**: Invalid views JSON structure
- **JV003**: Invalid referrers JSON structure
- **HF001**: History file not found
- **HV001**: Invalid history JSON
- **HV002**: History missing required key
- **GD001-008**: Dashboard generation errors

#### Merge Script Errors

- **MH001**: File not found
- **MH002**: Invalid JSON format
- **MH003**: Load error
- **MH004**: Save error
- **MH005**: Wrong arguments
- **MH006**: Structure validation failure
- **MH007**: Data integrity error

### Troubleshooting

#### Workflow Fails with Authentication Error

**Symptom:** Error code TF001-003 with HTTP 401 or 403

**Solutions:**
1. Verify `TRAFFIC_ACTION_TOKEN` secret is set correctly
2. Check token has `repo` scope
3. Ensure token hasn't expired
4. Regenerate token if needed

#### Graphs Not Displaying in README

**Symptom:** Graph images show as broken links

**Solutions:**
1. Verify `graphs/` directory exists
2. Check that graph files are generated
3. Ensure relative paths in README are correct
4. Check that README.md was updated (check commit history)

#### History.json Validation Fails

**Symptom:** Error code HV001 or HV002

**Solutions:**
1. Check file format matches expected structure
2. Verify JSON is valid (use JSON validator)
3. Check that `metadata` and `repositories` keys exist
4. If migrating from old format, ensure proper conversion

#### Workflow Not Running

**Symptom:** No workflow runs in Actions tab

**Solutions:**
1. Verify GitHub Actions is enabled in repository settings
2. Check that workflow file is in `.github/workflows/`
3. Verify cron expression is valid
4. Check repository has Actions permission enabled

#### Data Not Updating

**Symptom:** README.md not updating with new data

**Solutions:**
1. Check workflow logs for errors
2. Verify `TRAFFIC_ACTION_TOKEN` is valid
3. Ensure repositories are accessible
4. Check if workflow is actually running (check Actions tab)

---

## Maintenance

### Adding Repositories

To add new repositories to track:

1. Edit `.github/workflows/main.yml`
2. Find the `repos` array (around line 147-160)
3. Add new repository in format: `"owner/repository-name"`
4. Commit and push changes
5. Workflow will automatically start tracking new repositories

**Example:**
```yaml
repos=(
  "your-username/existing-repo"
  "your-username/new-repo-1"      # Added
  "your-username/new-repo-2"      # Added
)
```

### Updating Configuration

To modify workflow behavior:

1. Edit `.github/workflows/main.yml`
2. Modify configuration parameters at the top (lines 7-53)
3. Commit and push changes
4. Next workflow run will use new configuration

To modify graph appearance:

1. Edit `scripts/generate_dashboard.py`
2. Modify configuration parameters at the top (lines 14-64)
3. Commit and push changes
4. Next workflow run will use new configuration

### Monitoring

**Regular Checks:**

1. **Workflow Runs**: Check Actions tab weekly to ensure workflow is running
2. **Commit Messages**: Look for "[Recovered X missed run(s)]" messages
3. **README.md**: Verify graphs and statistics are updating
4. **Error Logs**: Review workflow logs for any warnings or errors

**Alerts:**

- **Missed Runs**: Check if workflow hasn't run in >24 hours
- **Authentication Errors**: Review if TF001-003 errors appear
- **Data Gaps**: Verify no gaps in graphs (should be continuous)

---

## Technical Details

### Data Format

The `history.json` file uses a standard structured format:

```json
{
  "metadata": {
    "generated_at": "2026-04-13T18:41:38.805420Z",
    "last_updated": "2026-04-13T18:41:38.805430Z",
    "repositories": ["owner/repo1", "owner/repo2"]
  },
  "repositories": {
    "owner/repo": {
      "daily_data": [
        {
          "date": "2026-04-13",
          "clones_total": 10,
          "clones_unique": 5,
          "views_total": 50,
          "views_unique": 20
        }
      ],
      "referrers": [...],
      "metadata": {
        "last_fetched": "2026-04-13T18:41:38Z",
        "clones_total": 100,
        "clones_unique_total": 50,
        "views_total": 500,
        "views_unique_total": 200
      }
    }
  }
}
```

### Technical Stack

- **Python 3**: Primary programming language
- **GitHub Actions**: Workflow automation
- **Matplotlib**: Graph generation
- **Pandas**: Data processing
- **NumPy**: Numerical operations
- **GitHub API**: Traffic data source

### Dependencies

Python dependencies (installed automatically by workflow):

```bash
pip install matplotlib pandas numpy
```

For local testing:

```bash
python -m pip install matplotlib pandas numpy
```

---

## Limitations

1. **Data Recovery Limit**: Up to 14 consecutive days can be recovered. Beyond that, data is permanently lost (GitHub API limitation).

2. **Rate Limits**: GitHub API has rate limits. Current usage is well within limits for daily runs.

3. **Repository Access**: You must have access to the repositories you're tracking (or they must be public).

4. **Historical Data**: Only data from when you start tracking is available. No historical data before first run.

---

## License and Credits

This project is provided as-is for tracking GitHub repository traffic statistics.

Inspired by and compatible with principles from:
- [github-repo-stats](https://github.com/jgehrcke/github-repo-stats) by jgehrcke
- GitHub Traffic API documentation

---

## Summary

The GitHub Traffic Dashboard is a complete, production-ready solution that:

- Automatically collects and tracks repository traffic data
- Generates comprehensive graphs and statistics
- Handles server downtime and calendar edge cases robustly
- Provides clear error reporting and troubleshooting information
- Includes comprehensive documentation for maintenance and operation

The solution requires minimal manual intervention and provides continuous, reliable tracking of GitHub repository traffic statistics.

**Ready to use?** Follow the [Quick Start](#quick-start) guide to get started in minutes!
