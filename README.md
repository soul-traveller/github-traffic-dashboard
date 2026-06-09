See full Reference and Usage Guide at:
https://soul-traveller.github.io/github-traffic-dashboard/

# 📊 GitHub Traffic Dashboard

This dashboard tracks historical traffic data (clones and views) for GitHub repositories.

**Last Updated:** 2026-06-09T06:00:52.562515Z

## 📋 How Metrics Are Calculated

This dashboard uses GitHub Traffic API data to calculate the following metrics:

### 📊 Core Metrics

**Views:**
- Counted when someone visits the repository page
- Includes page views from web browsers
- Does not include visits via command-line tools or APIs

**Clones:**
- Counted when someone clones the repository
- Includes clones via `git clone`, GitHub Desktop, download ZIP, and API
- Can occur without a corresponding view event

**Important:** Views and Clones are **independent metrics**. Users can:
- View without cloning
- Clone without viewing (e.g., via `git clone` command)
- Both view and clone

### 🔢 Calculation Formulas

**For any time period (short-term, medium-term, lifetime):**

**Total Metrics:**
- Total Views = Sum of daily views for the period
- Total Clones = Sum of daily clones for the period

**Unique Metrics:**
- Unique Views = Sum of daily unique views for the period
- Unique Clones = Sum of daily unique clones for the period
  - Note: This sums daily unique counts, which may count the same user on multiple days

**Repeat Metrics:**
- Repeat Views = Total Views - Unique Views
- Repeat Clones = Total Clones - Unique Clones
- Repeat Percentage = (Repeat / Total) × 100

**Example:**
```
If a repository has:
- Total Views: 100
- Unique Views: 20
Then:
- Repeat Views = 100 - 20 = 80
- Repeat Percentage = (80 / 100) × 100 = 80%
```

### 📈 Graph Data Aggregation

**Daily Graphs:**
- Shows raw daily data points
- Each point represents one day's activity

**Weekly Graphs:**
- Aggregates daily data into 7-day periods
- Each point represents the sum of 7 consecutive days

**Bi-Weekly Graphs:**
- Aggregates daily data into 14-day periods
- Each point represents the sum of 14 consecutive days

**Cumulative Graphs:**
- Shows running totals over time
- Each point represents the sum of all previous days plus current day

## 📋 Table of Contents

Quick navigation to repository statistics:

- [Argyll_Printer_Profiler](#argyll-printer-profiler)
- [Argyll_Printer_Profiler_GUI](#argyll-printer-profiler-gui)
- [Toggle_Display_Profile](#toggle-display-profile)
- [rectarg](#rectarg)
- [github-traffic-dashboard](#github-traffic-dashboard)
- [average_ti3s_rgbgeom](#average-ti3s-rgbgeom)
- [read_image_patch_colors](#read-image-patch-colors)

# Argyll_Printer_Profiler

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 8 | 8 |
| Last 90 Days | 208 | 111 |
| Lifetime | 208 | 111 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 8 | 8 | 0 | 0.0% |
| Last 90 Days | 208 | 111 | 97 | 46.6% |
| Lifetime | 208 | 111 | 97 | 46.6% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 34 | 24 |
| Last 90 Days | 196 | 59 |
| Lifetime | 196 | 59 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 3

| Referrer | Total Views | Unique Visitors |
|----------|-------------|----------------|
| soul-traveller.github.io | 13 | 9 |
| github.com | 1 | 1 |
| printerknowledge.com | 1 | 1 |

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 34 | 24 | 10 | 29.4% |
| Last 90 Days | 196 | 59 | 137 | 69.9% |
| Lifetime | 196 | 59 | 137 | 69.9% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_Argyll_Printer_Profiler_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_Argyll_Printer_Profiler_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_Argyll_Printer_Profiler_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_Argyll_Printer_Profiler_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_Argyll_Printer_Profiler_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_Argyll_Printer_Profiler_cumulative_views.png)

---

# Argyll_Printer_Profiler_GUI

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 13 | 13 |
| Last 90 Days | 114 | 68 |
| Lifetime | 114 | 68 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 13 | 13 | 0 | 0.0% |
| Last 90 Days | 114 | 68 | 46 | 40.4% |
| Lifetime | 114 | 68 | 46 | 40.4% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 1 | 1 |
| Last 90 Days | 26 | 5 |
| Lifetime | 26 | 5 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 0

*No referrer data available.*

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 1 | 1 | 0 | 0.0% |
| Last 90 Days | 26 | 5 | 21 | 80.8% |
| Lifetime | 26 | 5 | 21 | 80.8% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_Argyll_Printer_Profiler_GUI_cumulative_views.png)

---

# Toggle_Display_Profile

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 16 | 16 |
| Last 90 Days | 138 | 89 |
| Lifetime | 138 | 89 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 16 | 16 | 0 | 0.0% |
| Last 90 Days | 138 | 89 | 49 | 35.5% |
| Lifetime | 138 | 89 | 49 | 35.5% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 0 | 0 |
| Last 90 Days | 86 | 9 |
| Lifetime | 86 | 9 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 0

*No referrer data available.*

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 0 | 0 | 0 | 0% |
| Last 90 Days | 86 | 9 | 77 | 89.5% |
| Lifetime | 86 | 9 | 77 | 89.5% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_Toggle_Display_Profile_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_Toggle_Display_Profile_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_Toggle_Display_Profile_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_Toggle_Display_Profile_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_Toggle_Display_Profile_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_Toggle_Display_Profile_cumulative_views.png)

---

# rectarg

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 14 | 13 |
| Last 90 Days | 84 | 76 |
| Lifetime | 84 | 76 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 14 | 13 | 1 | 7.1% |
| Last 90 Days | 84 | 76 | 8 | 9.5% |
| Lifetime | 84 | 76 | 8 | 9.5% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 1 | 1 |
| Last 90 Days | 10 | 6 |
| Lifetime | 10 | 6 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 1

| Referrer | Total Views | Unique Visitors |
|----------|-------------|----------------|
| github.com | 1 | 1 |

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 1 | 1 | 0 | 0.0% |
| Last 90 Days | 10 | 6 | 4 | 40.0% |
| Lifetime | 10 | 6 | 4 | 40.0% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_rectarg_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_rectarg_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_rectarg_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_rectarg_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_rectarg_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_rectarg_cumulative_views.png)

---

# github-traffic-dashboard

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 359 | 192 |
| Last 90 Days | 1679 | 783 |
| Lifetime | 1679 | 783 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 359 | 192 | 167 | 46.5% |
| Last 90 Days | 1679 | 783 | 896 | 53.4% |
| Lifetime | 1679 | 783 | 896 | 53.4% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 7 | 2 |
| Last 90 Days | 288 | 22 |
| Lifetime | 288 | 22 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 1

| Referrer | Total Views | Unique Visitors |
|----------|-------------|----------------|
| soul-traveller.github.io | 1 | 1 |

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 7 | 2 | 5 | 71.4% |
| Last 90 Days | 288 | 22 | 266 | 92.4% |
| Lifetime | 288 | 22 | 266 | 92.4% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_github-traffic-dashboard_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_github-traffic-dashboard_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_github-traffic-dashboard_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_github-traffic-dashboard_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_github-traffic-dashboard_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_github-traffic-dashboard_cumulative_views.png)

---

# average_ti3s_rgbgeom

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 15 | 14 |
| Last 90 Days | 28 | 27 |
| Lifetime | 28 | 27 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 15 | 14 | 1 | 6.7% |
| Last 90 Days | 28 | 27 | 1 | 3.6% |
| Lifetime | 28 | 27 | 1 | 3.6% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 2 | 1 |
| Last 90 Days | 2 | 1 |
| Lifetime | 2 | 1 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 1

| Referrer | Total Views | Unique Visitors |
|----------|-------------|----------------|
| github.com | 2 | 1 |

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 2 | 1 | 1 | 50.0% |
| Last 90 Days | 2 | 1 | 1 | 50.0% |
| Lifetime | 2 | 1 | 1 | 50.0% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_average_ti3s_rgbgeom_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_average_ti3s_rgbgeom_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_average_ti3s_rgbgeom_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_average_ti3s_rgbgeom_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_average_ti3s_rgbgeom_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_average_ti3s_rgbgeom_cumulative_views.png)

---

# read_image_patch_colors

### 🗅️ Clones

*Repository clone statistics showing total and unique clones over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 11 | 11 |
| Last 90 Days | 53 | 52 |
| Lifetime | 53 | 52 |

### 📄 Repeat vs New Clones

*Analysis of repository adoption showing repeat clones vs new unique clones.*

*Note: GitHub API does not provide geographical location data for cloners.*

| Period | Total Clones | Unique Clones | Repeat Clones | Repeat % |
|--------|--------------|----------------|----------------|----------|
| Last 30 Days | 11 | 11 | 0 | 0.0% |
| Last 90 Days | 53 | 52 | 1 | 1.9% |
| Lifetime | 53 | 52 | 1 | 1.9% |

### 👀 Views

*Repository view statistics showing total and unique views over different time periods.*

| Period | Total | Unique |
|--------|-------|--------|
| Last 30 Days | 0 | 0 |
| Last 90 Days | 2 | 2 |
| Lifetime | 2 | 2 |

### 📞 Referrers

*Top referrer sources driving traffic to this repository.*

**Total Unique Referrers:** 0

*No referrer data available.*

### 👥 Repeat vs New Visitors

*Analysis of visitor engagement showing repeat visitors vs new unique visitors.*

*Note: GitHub API does not provide geographical location data for visitors.*

| Period | Total Views | Unique Visitors | Repeat Visitors | Repeat % |
|--------|-------------|-----------------|-----------------|----------|
| Last 30 Days | 0 | 0 | 0 | 0% |
| Last 90 Days | 2 | 2 | 0 | 0.0% |
| Lifetime | 2 | 2 | 0 | 0.0% |

### 📈 Traffic Graphs

*Visual representations of traffic trends over different time periods.*

#### Daily Traffic (30 Days)

*Shows daily clones and views trends for the last 30 days. Useful for identifying short-term patterns and recent activity spikes.*

![Daily 30 Days](graphs/soul-traveller_read_image_patch_colors_daily_30d.png)

#### Weekly Traffic (12 Weeks)

*Shows weekly aggregated clones and views for the last 12 weeks (~3 months). Useful for identifying medium-term trends and seasonal patterns.*

![Weekly 12 Weeks](graphs/soul-traveller_read_image_patch_colors_weekly_12m.png)

#### Bi-Weekly Traffic (26 Periods)

*Shows bi-weekly aggregated clones and views for the last 26 periods (~1 year). Useful for identifying long-term trends and yearly patterns.*

![Bi-Weekly 26 Periods](graphs/soul-traveller_read_image_patch_colors_biweekly_26y.png)

#### Cumulative Traffic (Lifetime)

*Shows running totals of both clones and views over the entire lifetime of tracking. Useful for seeing overall growth and total adoption.*

![Cumulative](graphs/soul-traveller_read_image_patch_colors_cumulative.png)

#### Separate Cumulative Graphs

*Individual cumulative graphs for clones and views, allowing for easier comparison between the two metrics.*

**Cumulative Clones:**

![Cumulative Clones](graphs/soul-traveller_read_image_patch_colors_cumulative_clones.png)

**Cumulative Views:**

![Cumulative Views](graphs/soul-traveller_read_image_patch_colors_cumulative_views.png)

---

*This dashboard is automatically updated daily using GitHub Actions.*
