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
    repo = entry["repository"]
    repos.setdefault(repo, []).append(entry)

os.makedirs("graphs", exist_ok=True)

def collect_daily_clones(entries):
    daily = {}

    for e in entries:
        for c in e["clones"]["clones"]:
            date = c["timestamp"][:10]
            daily[date] = daily.get(date, 0) + c["count"]

    return daily

def sum_period(daily, days):
    cutoff = datetime.utcnow() - timedelta(days=days)
    total = 0
    for d, count in daily.items():
        dt = datetime.fromisoformat(d)
        if dt > cutoff:
            total += count
    return total

# Generate markdown
md = "# 📊 GitHub Traffic Dashboard\n\n"

for repo, entries in repos.items():
    daily = collect_daily_clones(entries)

    # Sort dates
    dates = sorted(daily.keys())
    counts = [daily[d] for d in dates]

    # Stats
    last_90 = sum_period(daily, 90)
    last_365 = sum_period(daily, 365)
    total = sum(daily.values())

    # Create graph
    plt.figure()
    plt.plot(dates, counts)
    plt.xticks(rotation=45)
    plt.title(f"Clones over time: {repo}")
    plt.tight_layout()

    filename = f"graphs/{repo.replace('/', '_')}_clones.png"
    plt.savefig(filename)
    plt.close()

    # Add to markdown
    md += f"## {repo}\n"
    md += f"- Last 3 months: **{last_90} clones**\n"
    md += f"- Last 12 months: **{last_365} clones**\n"
    md += f"- Total: **{total} clones**\n\n"
    md += f"![Clones graph]({filename})\n\n"

# Write README
with open("README.md", "w") as f:
    f.write(md)
