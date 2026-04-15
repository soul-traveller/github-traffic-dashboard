# GitHub Traffic Dashboard - User Guide

This is a user guide for the GitHub Traffic Dashboard. It provides instructions on how to use the dashboard and its features. This Reference and Usage Guide can be found at:<br>
https://soul-traveller.github.io/github-traffic-dashboard/

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
- **Detailed Statistics**: Calculates statistics for configurable short-term, medium-term, and lifetime periods
- **Referrer Analysis**: Tracks top referrer sources and unique referrer counts
- **Visitor Engagement**: Analyzes repeat visitors vs new visitors
- **Clickable Navigation**: Auto-generated table of contents for quick repository access
- **Robust Error Handling**: Comprehensive error codes and clear error messages
- **Server Downtime Recovery**: Automatically recovers up to 14 days of missed data
- **Calendar Edge Case Handling**: Correctly handles year transitions, leap years, and month boundaries
- **Scalable Architecture**: Easy to add multiple repositories with minimal configuration

### What It Does

1. **Fetches Data**: Daily at 2 AM UTC, the workflow fetches traffic data (clones, views, referrers) from GitHub API
2. **Merges Data**: New data is merged with historical data, with zero-filling for missing dates
3. **Generates Graphs**: Creates professional graphs showing traffic trends over different time periods
4. **Calculates Statistics**: Computes totals and unique counts for configurable short-term, medium-term, and lifetime periods
5. **Analyzes Referrers**: Tracks top referrer sources and unique referrer counts
6. **Measures Engagement**: Calculates repeat visitors vs new visitors
7. **Creates Navigation**: Auto-generates clickable table of contents for quick access
8. **Updates Dashboard**: Automatically updates README.md with statistics, tables, and embedded graph images

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

**Using Command Line:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/soul-traveller/github-traffic-dashboard.git
   cd github-traffic-dashboard
   ```

2. **Configure your repositories**
   - Edit `.github/workflows/main.yml`
   - Add your repositories in the `repos` array (lines 151-158)
   - Example: `"your-username/your-repo"`

3. **Set up GitHub secret**
   - Go to repository Settings > Secrets and variables > Actions
   - Create a new secret named `TRAFFIC_ACTION_TOKEN`
   - Generate a Personal Access Token with `repo` scope and paste it

**Using GitHub Desktop:**

1. **Clone the repository**
   - Open GitHub Desktop
   - Click "File" > "Clone Repository"
   - URL: `https://github.com/soul-traveller/github-traffic-dashboard.git`
   - Local path: Choose a folder
   - Click "Clone"

2. **Configure your repositories**
   - Open the cloned repository in your text editor
   - Navigate to `.github/workflows/main.yml`
   - Edit line 151-158 to add your repositories

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

**Using Command Line:**

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

**Using GitHub Desktop:**

1. Clone the repository:
   - Open GitHub Desktop
   - Click "File" > "Clone Repository"
   - URL: `https://github.com/soul-traveller/github-traffic-dashboard.git`
   - Local path: Choose a folder
   - Click "Clone"

2. Configure your repositories (see [Configuration](#configuration))

3. Set up GitHub secret (see [Quick Start](#quick-start))

4. Push to your GitHub repository:
   - In GitHub Desktop, go to "Repository" > "Repository Settings"
   - Under "Remote", change the URL to: `https://github.com/your-username/your-repo.git`
   - Click "Save"
   - In the main window, you'll see your changes
   - Enter commit message: "Initial setup"
   - Click "Commit to main"
   - Click "Push origin" to push to GitHub

5. Enable GitHub Actions in repository settings

#### Option 2: Fork and Customize

**Using Command Line:**

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/github-traffic-dashboard.git
   cd github-traffic-dashboard
   ```

3. Follow steps 2-5 from Option 1

**Using GitHub Desktop:**

1. Fork the repository on GitHub
   - Go to https://github.com/soul-traveller/github-traffic-dashboard
   - Click "Fork" button in the top-right
   - Choose your account as the destination

2. Clone your fork:
   - Open GitHub Desktop
   - Click "File" > "Clone Repository"
   - URL: `https://github.com/your-username/github-traffic-dashboard.git`
   - Local path: Choose a folder
   - Click "Clone"

3. Follow steps 2-5 from Option 1 (using GitHub Desktop alternatives)

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
- Updating stored repository data within the 14-day API retention window

**Important Notes:**
- GitHub API retains traffic data for the last 14 days only
- Manual runs will fetch the latest 14 days of data from the API
- The merge process ensures no historical data is duplicated
- New API data takes precedence over existing data for the same dates
- This allows you to correct wrong data by manually running the workflow
- All data within the 14-day window will be updated to the latest values

### Understanding the Output

#### README.md Structure

Your README.md will contain:

```
# GitHub Traffic Dashboard

## Table of Contents

- [Repository 1](#repository-1)
- [Repository 2](#repository-2)
...

# Repository Name

### Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last [short-term period] Days | X | Y |
| Last [medium-term period] Days | X | Y |
| Lifetime | X | Y |

### Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last [short-term period] Days | X | Y | Z | P% |
| Last [medium-term period] Days | X | Y | Z | P% |
| Lifetime | X | Y | Z | P% |

### Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last [short-term period] Days | X | Y |
| Last [medium-term period] Days | X | Y |
| Lifetime | X | Y |

### Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** N

| Referrer | Total Views | Unique Visitors |
|----------|-------------|----------------|
| referrer1.com | X | Y |
| referrer2.com | X | Y |
...

### Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last [short-term period] Days | X | Y | Z | P% |
| Last [medium-term period] Days | X | Y | Z | P% |
| Lifetime | X | Y | Z | P% |

### Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days (configurable via DAILY_GRAPH_DAYS). Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/repo_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/repo_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/repo_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/repo_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/repo_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/repo_cumulative_views.png)
```

**Note:** Statistics are displayed in professional table format for easy comparison and readability.

#### Graph Types

1. **Daily Traffic (30 Days)**: Shows daily clones and views trends for the last 30 days (configurable via DAILY_GRAPH_DAYS). Useful for identifying short-term patterns and recent activity spikes.
2. **Weekly Traffic (12 Weeks)**: Shows weekly aggregated clones and views for the last 12 weeks (~3 months, configurable via WEEKLY_GRAPH_WEEKS). Useful for identifying medium-term trends and seasonal patterns.
3. **Bi-Weekly Traffic (26 Periods)**: Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year, configurable via BIWEEKLY_GRAPH_PERIODS). Useful for identifying long-term trends and yearly patterns.
4. **Cumulative Traffic**: Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.
5. **Cumulative Clones**: Separate cumulative graph for clones only, allowing for focused analysis of clone adoption.
6. **Cumulative Views**: Separate cumulative graph for views only, allowing for focused analysis of view trends.

#### Statistics Explained

**Clone and View Statistics:**
- **Total**: Sum of all clones/views in the period
- **Unique**: Count of unique users who cloned/viewed
- **Short-term period**: Configurable via STATS_PERIOD_SHORT_TERM (default: 30 days)
- **Medium-term period**: Configurable via STATS_PERIOD_MEDIUM_TERM (default: 90 days)
- **Lifetime**: All-time totals

**Repeat vs New Clones:**
- **Total Clones**: Total number of clones in the period
- **Unique Clones**: Number of unique clones (new users)
- **Repeat Clones**: Total clones minus unique clones
- **Repeat Percentage**: Percentage of clones from repeat users
- Available for short-term, medium-term, and lifetime periods (all configurable)

**Note:** GitHub API does not provide geographical location data for cloners. Location-based statistics are not available.

**Referrer Statistics:**
- **Total Unique Referrers**: Count of distinct referrer sources (websites, search engines, etc.)
- **Referrer**: The source URL or domain that referred visitors to your repository
- **Total Views**: Total number of views from this referrer
- **Unique Visitors**: Number of unique visitors from this referrer

**Repeat vs New Visitors:**
- **Total Views**: Total number of page views in the period
- **Unique Visitors**: Number of unique visitors (new users)
- **Repeat Visitors**: Total views minus unique visitors
- **Repeat Percentage**: Percentage of views from repeat visitors
- Available for short-term, medium-term, and lifetime periods (all configurable)

**Note:** GitHub API does not provide geographical location data for visitors. Location-based statistics are not available.

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

**Using Command Line:**

```bash
cd github-traffic-dashboard
git remote set-url origin https://github.com/your-username/your-new-repo-name.git
git push -u origin main
```

**Using GitHub Desktop:**

1. In GitHub Desktop, go to "Repository" > "Repository Settings"
2. Under "Remote", change the URL to: `https://github.com/your-username/your-new-repo-name.git`
3. Click "Save"
4. Click "Push origin" to update the remote URL

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
- README generation settings

**In `scripts/merge_history.py` (lines 33-57):**
- File paths (default paths for input/output files)
- Note: Data handling behaviors are hardcoded (zero-filling, merging, recalculating totals, data retention)

**In `.github/workflows/main.yml` (lines 7-53):**
- Workflow schedule
- API settings
- Repository list

#### Example: Complete Setup for New User

**Using Command Line:**

```bash
# 1. Clone the repository
git clone https://github.com/soul-traveller/github-traffic-dashboard.git my-traffic-dashboard
cd my-traffic-dashboard

# 2. Edit workflow with your repositories
# Edit .github/workflows/main.yml, line 151-158:
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

**Using GitHub Desktop:**

1. **Clone the repository:**
   - Open GitHub Desktop
   - Click "File" > "Clone Repository"
   - URL: `https://github.com/soul-traveller/github-traffic-dashboard.git`
   - Local path: Choose a folder (e.g., `my-traffic-dashboard`)
   - Click "Clone"

2. **Edit workflow with your repositories:**
   - Open the cloned repository in your text editor
   - Navigate to `.github/workflows/main.yml`
   - Edit line 151-158 to add your repositories:
   ```yaml
   repos=(
     "john-doe/awesome-project"
     "john-doe/cool-library"
     "john-doe/useful-tool"
   )
   ```

3. **Create new repository on GitHub:**
   - Go to GitHub.com
   - Click "+" > "New repository"
   - Name: `my-traffic-dashboard`
   - Make it public or private as needed
   - Click "Create repository"

4. **Update repository remote:**
   - In GitHub Desktop, go to "Repository" > "Repository Settings"
   - Under "Remote", change the URL to: `https://github.com/john-doe/my-traffic-dashboard.git`
   - Click "Save"

5. **Commit and push:**
   - In GitHub Desktop, you'll see your changes in the left panel
   - Enter commit message: "Setup for john-doe repositories"
   - Click "Commit to main"
   - Click "Push origin" to push to GitHub

6. **Set up TRAFFIC_ACTION_TOKEN secret:**
   - Go to your new repository on GitHub
   - Click "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `TRAFFIC_ACTION_TOKEN`
   - Value: Your GitHub personal access token (with 'repo' scope)
   - Click "Add secret"

7. **Enable GitHub Actions:**
   - In repository settings, go to "Actions" > "General"
   - Under "Actions permissions", select "Allow all actions and reusable workflows"
   - Click "Save"

8. **Manually trigger workflow to test:**
   - Go to "Actions" tab in your repository
   - Select "GitHub Traffic Dashboard" workflow
   - Click "Run workflow" button
   - Select branch (usually `main`)
   - Click "Run workflow"

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

#### Workflow Schedule (Line 33)

```yaml
schedule:
  - cron: "0 2 * * *"   # every day at 2 AM UTC
```

**Schedule Options - All Work Without Data Loss**

The GitHub Traffic API provides only the last 14 days of traffic data, but `merge_history.py` preserves all historical data in `history.json`. Therefore:

- **Daily runs (recommended):** Dashboard updates daily, see changes day by day
- **Weekly runs:** Dashboard updates weekly, all data preserved
- **Bi-weekly runs:** Dashboard updates bi-weekly, all data preserved

**How It Works:**

The `merge_history.py` script:
1. Keeps all existing data in `history.json`
2. Adds new data from the API (last 14 days)
3. Updates overlapping dates with fresh API data
4. Never deletes old historical data

**Example with Weekly Runs:**
- Day 1: Run, get days 1-14 from API, save to history.json
- Day 8: Run, get days 8-21 from API, merge with history.json (days 8-14 already saved, days 15-21 added)
- Day 15: Run, get days 15-28 from API, merge with history.json (days 15-21 already saved, days 22-28 added)

**No data is lost** - all historical data is preserved in `history.json` forever.

**Common Schedules:**
- `"0 2 * * *"` - Daily at 2 AM UTC (default, recommended for frequent updates)
- `"0 */6 * * *"` - Every 6 hours (more frequent, wastes API quota)
- `"0 0 * * 0"` - Weekly on Sunday at midnight UTC (works fine, less frequent updates)
- `"0 12 * * 1"` - Weekly on Monday at noon UTC (works fine, less frequent updates)

**Trade-offs:**
- **Daily runs:** More frequent dashboard updates, see daily changes
- **Weekly runs:** Less frequent dashboard updates, but all data preserved
- **Bi-weekly runs:** Even less frequent updates, but all data preserved

**Format:** `minute hour day month day-of-week`

#### API Configuration (Lines 46-48)

```yaml
env:
  GITHUB_API_BASE_URL: "https://api.github.com"
  GITHUB_API_VERSION: "2022-11-28"
```

**Note:** All date calculations use UTC timezone for consistency.

**Note:** These rarely need to be changed.

### Python Script Configuration

Both Python scripts have configuration sections at the top with clear guidance.

#### generate_dashboard.py (Lines 15-64)

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
STATS_PERIOD_SHORT_TERM = 30               # Short-term statistics period (default: 30 days)
STATS_PERIOD_MEDIUM_TERM = 90               # Medium-term statistics period (default: 90 days)

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

#### merge_history.py (Lines 34-57)

```python
# ============================================================================
# CONFIGURATION SECTION - MODIFY THESE PARAMETERS FOR YOUR NEEDS
# ============================================================================

# File Paths Configuration
DEFAULT_HISTORY_FILE = "history.json"           # Path to existing historical data
DEFAULT_NEW_DATA_FILE = "traffic_data.json"     # Path to newly fetched data
DEFAULT_OUTPUT_FILE = "merged_history.json"     # Path for merged output
```

**Note:** The following behaviors are hardcoded and always active in merge_history.py:
- Zero-filling: Always enabled, fills missing dates with zeros for 365 days
- Data merging: New data always overwrites existing data for the same date
- Metadata: Uses new metadata if available, otherwise keeps existing metadata
- Totals: Always recalculated from merged data
- Data retention: All historical data is retained indefinitely
- Timezone: All operations use UTC
- Date format: All dates use YYYY-MM-DD format
- DateTime format: All timestamps use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

**Only 3 configuration parameters are available in merge_history.py (all file paths).**

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

1. **Daily Traffic (30 Days)**: Daily intervals showing short-term trends (configurable via DAILY_GRAPH_DAYS)
2. **Weekly Traffic (3 Months)**: Weekly aggregates showing medium-term trends (configurable via WEEKLY_GRAPH_WEEKS)
3. **Bi-Weekly Traffic (1 Year)**: Bi-weekly aggregates showing long-term trends (configurable via BIWEEKLY_GRAPH_PERIODS)
4. **Cumulative Traffic**: Running totals of both clones and views
5. **Cumulative Clones**: Separate cumulative graph for clones
6. **Cumulative Views**: Separate cumulative graph for views

All graphs are:
- Publication-ready quality
- Consistently styled
- Properly labeled
- Embedded in README.md

### Statistics Calculation

Statistics are calculated for three configurable periods:

**Clone and View Statistics:**

**Short-term Period (configurable via STATS_PERIOD_SHORT_TERM, default: 30 days):**
- Total clones
- Unique clones
- Total views
- Unique views

**Medium-term Period (configurable via STATS_PERIOD_MEDIUM_TERM, default: 90 days):**
- Total clones
- Unique clones
- Total views
- Unique views

**Lifetime:**
- Total clones
- Unique clones
- Total views
- Unique views

**Referrer Statistics:**
- Total unique referrers (lifetime)
- Top 10 referrers by total views
- Total views per referrer
- Unique visitors per referrer

**Repeat vs New Clones:**

**Short-term Period (configurable via STATS_PERIOD_SHORT_TERM, default: 30 days):**
- Total clones vs unique clones
- Repeat clones calculation (total - unique)
- Repeat clone percentage

**Medium-term Period (configurable via STATS_PERIOD_MEDIUM_TERM, default: 90 days):**
- Total clones vs unique clones
- Repeat clones calculation (total - unique)
- Repeat clone percentage

**Lifetime:**
- Total clones vs unique clones
- Repeat clones calculation (total - unique)
- Repeat clone percentage
- Available for short-term, medium-term, and lifetime periods (all configurable)

**Repeat vs New Visitors:**

**Short-term Period (configurable via STATS_PERIOD_SHORT_TERM, default: 30 days):**
- Total views vs unique visitors
- Repeat visitors calculation (total - unique)
- Repeat visitor percentage

**Medium-term Period (configurable via STATS_PERIOD_MEDIUM_TERM, default: 90 days):**
- Total views vs unique visitors
- Repeat visitors calculation (total - unique)
- Repeat visitor percentage

**Lifetime:**
- Total views vs unique visitors
- Repeat visitors calculation (total - unique)
- Repeat visitor percentage
- Available for short-term, medium-term, and lifetime periods (all configurable)

All statistics are displayed in README.md with:
- Professional table format
- Clear descriptions
- Clickable navigation index
- Graph titles and explanations

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

### Key Functions in generate_dashboard.py

**New Statistics Functions (lines 695-841):**

- `calculate_referrer_stats()` (line 695): Calculates referrer statistics including total unique referrers, referrers sorted by count, total views, and unique visitors from referrers.

- `calculate_repeat_vs_new_stats()` (line 738): Calculates repeat visitors vs new visitors statistics for different time periods (short-term via STATS_PERIOD_SHORT_TERM, medium-term via STATS_PERIOD_MEDIUM_TERM, lifetime). Shows engagement level and returning user behavior.

- `calculate_repeat_vs_new_clones_stats()` (line 791): Calculates repeat clones vs new clones statistics for different time periods (short-term via STATS_PERIOD_SHORT_TERM, medium-term via STATS_PERIOD_MEDIUM_TERM, lifetime). Shows repository adoption level and returning user behavior.

**README Generation Functions (lines 844-1049):**

- `generate_readme()` (line 844): Generates the complete README.md with:
  - Clickable table of contents (auto-generated based on configured repositories)
  - Clone statistics in table format
  - Repeat vs new clones table
  - View statistics in table format
  - Referrer statistics table
  - Repeat vs new visitors table
  - Traffic graphs with descriptive titles and explanations
  - Graph descriptions explaining what each graph shows

**Data Processing Functions (lines 154-692):**

- `calculate_period_stats()` (line 154): Calculates statistics for a specified time period
- `calculate_lifetime_stats()` (line 199): Calculates lifetime statistics from all available data
- `get_daily_data()` (line 239): Extracts daily data for specified number of days
- `get_weekly_data()` (line 278): Aggregates daily data into weekly periods
- `get_biweekly_data()` (line 335): Aggregates daily data into bi-weekly periods
- `get_cumulative_data()` (line 392): Calculates cumulative (running) totals
- `create_graph()` (line 436): Creates a single-line graph
- `create_multi_line_graph()` (line 504): Creates multi-line graphs for clones and views
- `generate_repository_graphs()` (line 580): Generates all graphs for a repository

### Key Functions in merge_history.py

**Data Merging Functions (lines 178-331):**

- `merge_daily_data()` (line 178): Merges daily data from existing and new sources. New data takes precedence for overlapping dates. This ensures no duplicate data and allows manual runs to correct wrong data within the 14-day API retention window.

- `merge_repositories()` (line 264): Merges repository data from existing and new sources. Handles daily data, referrers, and metadata. Referrers from new data (latest API fetch) take precedence, allowing manual updates within the 14-day window.

**Important Note on Data Merging:**
- The merge process ensures no historical data is duplicated
- New API data takes precedence over existing data for the same dates
- This allows manual workflow runs to update stored repository data to latest values
- Wrong data can be corrected by manually running the workflow
- All data within the 14-day API retention window will be updated to the latest values

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

5. **Geographical Location Data**: GitHub Traffic API does NOT provide geographical location data for visitors. This is a limitation of the GitHub API itself, not this dashboard. The referrer data only shows the source URL/domain (e.g., "github.com", "google.com") but not the physical location of visitors. Location-based statistics are not available through the GitHub API.

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
- Provides referrer analysis and visitor engagement metrics
- Handles server downtime and calendar edge cases robustly
- Provides clear error reporting and troubleshooting information
- Includes comprehensive documentation for maintenance and operation
- Offers clickable navigation and professional table formatting

The solution requires minimal manual intervention and provides continuous, reliable tracking of GitHub repository traffic statistics. All historical data is retained indefinitely for comprehensive analysis.

**Ready to use?** Follow the [Quick Start](#quick-start) guide to get started in minutes!
