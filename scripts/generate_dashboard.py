import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# Load data
with open("history.json") as f:
    data = json.load(f)

repos = {}

# Organize per repo
for entry in data:
    repo = entry.get("repository")
    if not repo:
        continue
    repos.setdefault(repo, []).append(entry)

os.makedirs("graphs", exist_ok=True)

# ----------------------------
# Helpers
# ----------------------------

def extract_series(entries, key):
    """Convert API array into {date: count}"""
    series = {}

    for e in entries:
        for item in e.get(key, []):
            ts = item.get("timestamp")
            count = item.get("count", 0)

            if not ts:
                continue

            day = ts[:10]
            series[day] = series.get(day, 0) + count

    return series


def rolling_sum(series, days):
    cutoff = datetime.utcnow() - timedelta(days=days)
    total = 0

    for d, v in series.items():
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            if dt >= cutoff:
                total += v
        except:
            continue

    return total


# ----------------------------
# FILL MISSING DAYS (DAILY)
# ----------------------------
def fill_daily(series, days=30):
    today = datetime.utcnow().date()
    filled_dates = []
    filled_values = []

    for i in range(days, -1, -1):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        filled_dates.append(d)
        filled_values.append(series.get(d, 0))

    return filled_dates, filled_values


# ----------------------------
# WEEKLY (7-day buckets with missing = 0)
# ----------------------------
def weekly_series(series, weeks=12):
    today = datetime.utcnow().date()

    weekly = []

    for w in range(weeks, -1, -1):
        week_start = today - timedelta(days=w * 7)

        total = 0
        for i in range(7):
            d = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            total += series.get(d, 0)

        weekly.append((week_start.strftime("%Y-%m-%d"), total))

    return weekly


# ----------------------------
# MONTHLY (30-day buckets approx, with gaps = 0)
# ----------------------------
def monthly_series(series, months=12):
    today = datetime.utcnow().date()

    monthly = []

    for m in range(months, -1, -1):
        month_start = today - timedelta(days=m * 30)

        total = 0
        for i in range(30):
            d = (month_start + timedelta(days=i)).strftime("%Y-%m-%d")
            total += series.get(d, 0)

        monthly.append((month_start.strftime("%Y-%m"), total))

    return monthly


# ----------------------------
# Build repo dataset
# ----------------------------
repo_data = {}

for repo, entries in repos.items():
    clones = extract_series(entries, "clones")
    views = extract_series(entries, "views")

    repo_data[repo] = {
        "clones": clones,
        "views": views,

        "clones_14": rolling_sum(clones, 14),
        "views_14": rolling_sum(views, 14),

        "clones_30": rolling_sum(clones, 30),
        "views_30": rolling_sum(views, 30),

        "clones_lifetime": sum(clones.values()),
        "views_lifetime": sum(views.values()),

        "weekly": weekly_series(clones),
        "monthly": monthly_series(clones)
    }


# ----------------------------
# Generate markdown
# ----------------------------
md = "# 📊 GitHub Traffic Dashboard\n\n"

for repo, d in repo_data.items():

    print(f"Processing {repo}")

    clones = d["clones"]
    views = d["views"]

    # ----------------------------
    # DAILY (FULL 30 DAYS WITH ZEROS)
    # ----------------------------
    dates, counts = fill_daily(clones, 30)
    dates_dt = [datetime.strptime(x, "%Y-%m-%d") for x in dates]

    filename_daily = f"graphs/{repo.replace('/', '_')}_daily.png"

    plt.figure()
    plt.plot(dates_dt, counts)
    plt.xticks(rotation=45)
    plt.title(f"Daily Clones (30d): {repo}")
    plt.tight_layout()
    plt.savefig(filename_daily)
    plt.close()

    # ----------------------------
    # WEEKLY (12 weeks WITH ZEROS)
    # ----------------------------
    w_dates = [x[0] for x in d["weekly"]]
    w_vals = [x[1] for x in d["weekly"]]

    w_dates_dt = [datetime.strptime(x, "%Y-%m-%d") for x in w_dates]

    filename_weekly = f"graphs/{repo.replace('/', '_')}_weekly.png"

    plt.figure()
    plt.plot(w_dates_dt, w_vals)
    plt.xticks(rotation=45)
    plt.title(f"Weekly Clones (3 months): {repo}")
    plt.tight_layout()
    plt.savefig(filename_weekly)
    plt.close()

    # ----------------------------
    # MONTHLY (12 months WITH ZEROS)
    # ----------------------------
    m_dates = [x[0] for x in d["monthly"]]
    m_vals = [x[1] for x in d["monthly"]]

    m_dates_dt = [datetime.strptime(x, "%Y-%m") for x in m_dates]

    filename_monthly = f"graphs/{repo.replace('/', '_')}_monthly.png"

    plt.figure()
    plt.plot(m_dates_dt, m_vals)
    plt.xticks(rotation=45)
    plt.title(f"Monthly Clones (1 year): {repo}")
    plt.tight_layout()
    plt.savefig(filename_monthly)
    plt.close()

    # ----------------------------
    # MARKDOWN
    # ----------------------------
    md += f"## {repo}\n\n"

    md += f"### Clones\n"
    md += f"- Last 14 days: **{d['clones_14']}**\n"
    md += f"- Last 30 days: **{d['clones_30']}**\n"
    md += f"- Lifetime: **{d['clones_lifetime']}**\n\n"

    md += f"### Views\n"
    md += f"- Last 14 days: **{d['views_14']}**\n"
    md += f"- Last 30 days: **{d['views_30']}**\n"
    md += f"- Lifetime: **{d['views_lifetime']}**\n\n"

    md += f"### Graphs\n"
    md += f"![Daily]({filename_daily})\n"
    md += f"![Weekly]({filename_weekly})\n"
    md += f"![Monthly]({filename_monthly})\n\n"


# ----------------------------
# WRITE README
# ----------------------------
with open("README.md", "w") as f:
    f.write(md)

print("✅ Dashboard generated")
