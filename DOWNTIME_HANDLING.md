# Server Downtime Handling and Calendar Edge Cases

## Overview

This document explains how the GitHub Traffic Dashboard handles server downtime, missed workflow runs, and calendar edge cases to ensure data integrity and continuous operation.

## Server Downtime Handling

### How It Works

The GitHub Traffic API provides data for the **last 14 days**. This feature is leveraged to recover from server downtime automatically:

1. **Normal Operation**: Workflow runs daily at 2 AM UTC
2. **Server Down**: If the workflow misses a day (e.g., GitHub Actions server down), no data is collected
3. **Recovery**: On the next successful run, the API provides the last 14 days of data, including the missed day(s)
4. **Merge**: The merge script integrates this data, filling in the gaps
5. **Zero-Filling**: Ensures no dates are missing in the historical record

### Recovery Capabilities

- **Maximum Recovery**: Up to 14 consecutive days can be recovered without data loss
- **Automatic Detection**: Workflow detects when it hasn't run recently
- **Transparent Recovery**: No manual intervention required
- **Data Integrity**: All recovered data is properly validated and integrated

### Example Scenario

```
Day 1 (April 10): Workflow runs normally - collects data
Day 2 (April 11): Server down - workflow doesn't run
Day 3 (April 12): Workflow runs - API provides data for April 10, 11, 12
Result: All three days are in history.json with correct data
```

### Workflow Detection

The workflow includes a "Check for missed runs" step that:

1. Compares current date with `last_updated` timestamp in history.json
2. Calculates days since last successful run
3. Logs warnings if runs were missed
4. Provides recovery information in commit messages

Example commit message:
```
Update traffic dashboard - 2026-04-12 [Recovered 1 missed run(s)]
```

## Calendar Edge Cases

### Year Transitions

The system correctly handles year boundaries (December 31 to January 1):

- **Date Sorting**: Uses ISO date format (YYYY-MM-DD) which sorts correctly across years
- **Zero-Filling**: Generates all dates from start to end, regardless of year boundary
- **Calculations**: All date arithmetic uses UTC timezone for consistency

Example:
```
Dates: ['2025-12-30', '2025-12-31', '2026-01-01', '2026-01-02']
Sorted: ['2025-12-30', '2025-12-31', '2026-01-01', '2026-01-02']  # Correct
```

### Leap Years

The system handles leap years automatically:

- Python's `datetime` module correctly handles February 29
- Date calculations account for varying month lengths
- No special logic needed - standard library handles it

Example:
```
2024 is a leap year: February has 29 days
2025 is not a leap year: February has 28 days
```

### Month Boundaries

Month transitions are handled transparently:

- Date arithmetic uses `timedelta(days=1)` which works across month boundaries
- Zero-filling generates all dates regardless of month changes
- No edge case handling needed

Example:
```
Dates: ['2026-01-30', '2026-01-31', '2026-02-01', '2026-02-02']
Correctly spans January to February
```

## Data Integrity Guarantees

### No Duplicate Dates

The merge script uses a dictionary to ensure each date appears only once:

```python
merged_dict = {}
for entry in existing_data:
    merged_dict[entry['date']] = entry
for entry in new_data:
    merged_dict[entry['date']] = entry  # Overwrites if exists
```

### No Missing Dates

Zero-filling ensures all dates from start to end are present:

```python
while current_date <= end_date:
    if date not in data_dict:
        data_dict[date] = zero_filled_entry
    current_date += timedelta(days=1)
```

### Correct Totals

Metadata totals are recalculated from daily_data after each merge:

```python
totals = sum(entry['clones_total'] for entry in daily_data)
metadata['clones_total'] = totals
```

### Data Validation

Multiple validation steps ensure data integrity:

1. JSON structure validation (workflow)
2. JSON syntax validation (merge script)
3. Date range validation (zero-filling)
4. Total calculation verification (data integrity tests)

## Error Handling

### Server Downtime Errors

- **Detection**: Workflow detects missed runs automatically
- **Logging**: Clear warnings when runs are missed
- **Recovery**: Automatic data recovery up to 14 days
- **Commit Messages**: Include recovery information

### API Errors

- **HTTP Status Codes**: Validated for each API call (TF001-003)
- **JSON Validation**: API responses validated before processing (JV001-003)
- **Graceful Failure**: Workflow stops with clear error messages

### Data Errors

- **File Not Found**: HF001 - history.json not found
- **Invalid JSON**: HV001 - history.json is not valid JSON
- **Missing Keys**: HV002 - history.json missing 'repositories' key
- **Merge Failures**: MH001 - Failed to merge history data

## Testing

The `test_downtime.py` script verifies:

1. **Server Downtime**: Confirms API provides last 14 days including missed days
2. **Year Transition**: Verifies date sorting works across year boundaries
3. **Zero-Filling**: Confirms gaps are filled with zeros
4. **Merge with Gaps**: Verifies API data properly merges with history
5. **Data Integrity**: Confirms no duplicates, no gaps, totals match

Run tests:
```bash
python scripts/test_downtime.py
```

## Limitations

### Data Loss Beyond 14 Days

If the workflow is down for more than 14 consecutive days:

- Days beyond 14 days ago will be permanently lost
- GitHub API only provides last 14 days of data
- Historical data older than 14 days cannot be recovered

### Mitigation

- Monitor workflow runs regularly
- Set up GitHub Actions notifications
- Consider manual intervention if extended downtime occurs

## Best Practices

### Monitoring

1. **Check Workflow Runs**: Regularly verify the workflow is running daily
2. **Review Commit Messages**: Look for "[Recovered X missed run(s)]" messages
3. **Monitor Logs**: Check for warnings about missed runs

### Recovery

1. **Automatic**: No action needed for downtime up to 14 days
2. **Manual**: For extended downtime, consider manual API calls
3. **Verification**: Run `test_downtime.py` after recovery to verify data

### Maintenance

1. **Regular Testing**: Run test suite periodically
2. **Backup**: Keep backups of history.json
3. **Documentation**: Review this document for updates

## Technical Details

### Merge Algorithm

```
1. Load existing history.json (365+ days of data)
2. Load new API data (last 14 days)
3. Merge: existing + new (new takes precedence for overlaps)
4. Zero-fill: ensure all dates from start to end present
5. Recalculate totals from merged daily_data
6. Validate structure and integrity
7. Save merged data
```

### Date Handling

- **Timezone**: All dates in UTC for consistency
- **Format**: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- **Sorting**: String sorting works correctly for ISO dates
- **Arithmetic**: Python's `datetime` handles all edge cases

### API Integration

- **Endpoint**: `/repos/{owner}/{repo}/traffic/{clones|views}`
- **Response**: Last 14 days of daily data
- **Rate Limit**: GitHub API rate limits apply
- **Authentication**: Uses `TRAFFIC_ACTION_TOKEN` secret

## Summary

The GitHub Traffic Dashboard is designed to handle server downtime and calendar edge cases robustly:

- **Automatic Recovery**: Up to 14 days of missed data recovered automatically
- **Calendar Edge Cases**: Year transitions, leap years, month boundaries handled correctly
- **Data Integrity**: No duplicates, no gaps, correct totals
- **Comprehensive Error Handling**: Clear error codes and messages
- **Testing**: Automated tests verify all edge cases

The system requires minimal manual intervention and provides clear visibility into its operation through logs and commit messages.
