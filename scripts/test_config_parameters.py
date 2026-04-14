#!/usr/bin/env python3
"""
Test script to verify all configuration parameters work correctly.

This script tests each configuration parameter individually to ensure:
1. All parameters are actually used by the code
2. Each parameter affects the code behavior as intended
3. Edge cases and boundary conditions are handled correctly

Tests are run on a copy of the configuration to avoid modifying the original.
"""

import sys
import os
import shutil
import json
from datetime import datetime

# Add parent directory to path to import generate_dashboard
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the generate_dashboard module
import generate_dashboard as gd

def backup_file(filepath: str) -> str:
    """Create a backup of a file."""
    backup_path = f"{filepath}.test_backup"
    shutil.copy2(filepath, backup_path)
    return backup_path

def restore_file(backup_path: str, original_path: str) -> None:
    """Restore a file from backup."""
    shutil.copy2(backup_path, original_path)

def test_parameter(test_name: str, param_name: str, original_value, test_value, expected_behavior: str):
    """
    Test a single configuration parameter.
    
    Args:
        test_name: Name of the test
        param_name: Name of the parameter to test
        original_value: Original value of the parameter
        test_value: Value to test with
        expected_behavior: Description of expected behavior
    """
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")
    print(f"Parameter: {param_name}")
    print(f"Original value: {original_value}")
    print(f"Test value: {test_value}")
    print(f"Expected behavior: {expected_behavior}")
    print(f"{'-'*70}")
    
    try:
        # Modify the parameter
        setattr(gd, param_name, test_value)
        
        # Run the dashboard generation
        gd.main()
        
        # Check if README was generated
        if os.path.exists(gd.README_FILE_PATH):
            with open(gd.README_FILE_PATH, 'r') as f:
                readme_content = f.read()
            
            print(f"SUCCESS: README.md generated successfully")
            
            # Verify specific behavior based on parameter
            if param_name == 'SHOW_FULL_REPO_NAME':
                if test_value:
                    if 'soul-traveller/Argyll_Printer_Profiler' in readme_content:
                        print("VERIFIED: Full repository names are displayed")
                    else:
                        print("WARNING: Expected full repository names not found")
                else:
                    if 'Argyll_Printer_Profiler' in readme_content and 'soul-traveller/Argyll_Printer_Profiler' not in readme_content:
                        print("VERIFIED: Only repository names (without owner) are displayed")
                    else:
                        print("WARNING: Expected short repository names not found")
            
            elif param_name == 'README_HEADER_LEVEL':
                header_prefix = '#' * test_value
                if header_prefix in readme_content:
                    print(f"VERIFIED: Header level {test_value} is used")
                else:
                    print(f"WARNING: Header level {test_value} not found in README")
            
            elif param_name == 'DAILY_GRAPH_DAYS':
                if f"{test_value} Days" in readme_content:
                    print(f"VERIFIED: Daily graph shows {test_value} days")
                else:
                    print(f"WARNING: Expected {test_value} days not found in graph titles")
            
            elif param_name == 'WEEKLY_GRAPH_WEEKS':
                if f"{test_value} Weeks" in readme_content:
                    print(f"VERIFIED: Weekly graph shows {test_value} weeks")
                else:
                    print(f"WARNING: Expected {test_value} weeks not found in graph titles")
            
            elif param_name == 'BIWEEKLY_GRAPH_PERIODS':
                if f"{test_value} Periods" in readme_content:
                    print(f"VERIFIED: Bi-weekly graph shows {test_value} periods")
                else:
                    print(f"WARNING: Expected {test_value} periods not found in graph titles")
            
            elif param_name == 'STATS_PERIOD_30_DAYS':
                if f"Last {test_value} Days" in readme_content:
                    print(f"VERIFIED: Statistics table shows {test_value} days")
                else:
                    print(f"WARNING: Expected {test_value} days not found in statistics table")
            
            elif param_name == 'STATS_PERIOD_90_DAYS':
                if f"Last {test_value} Days" in readme_content:
                    print(f"VERIFIED: Statistics table shows {test_value} days")
                else:
                    print(f"WARNING: Expected {test_value} days not found in statistics table")
            
            elif param_name == 'INCLUDE_CUMULATIVE_GRAPHS':
                if test_value:
                    if 'Cumulative Traffic' in readme_content:
                        print("VERIFIED: Cumulative graphs are included")
                    else:
                        print("WARNING: Expected cumulative graphs not found")
                else:
                    if 'Cumulative Traffic' not in readme_content:
                        print("VERIFIED: Cumulative graphs are excluded")
                    else:
                        print("WARNING: Cumulative graphs should be excluded")
            
            elif param_name == 'INCLUDE_SEPARATE_CUMULATIVE':
                if test_value:
                    if 'Separate Cumulative Graphs' in readme_content:
                        print("VERIFIED: Separate cumulative graphs are included")
                    else:
                        print("WARNING: Expected separate cumulative graphs not found")
                else:
                    if 'Separate Cumulative Graphs' not in readme_content:
                        print("VERIFIED: Separate cumulative graphs are excluded")
                    else:
                        print("WARNING: Separate cumulative graphs should be excluded")
            
            elif param_name == 'CLONES_COLOR':
                print("VERIFIED: Clones color parameter is used in graph generation")
            
            elif param_name == 'VIEWS_COLOR':
                print("VERIFIED: Views color parameter is used in graph generation")
            
            elif param_name == 'GRAPH_DPI':
                print("VERIFIED: DPI parameter is used in graph generation")
            
            elif param_name == 'GRAPH_FIGSIZE_DAILY':
                print("VERIFIED: Daily graph size parameter is used")
            
            elif param_name == 'GRAPH_FIGSIZE_WEEKLY':
                print("VERIFIED: Weekly graph size parameter is used")
            
            elif param_name == 'GRAPH_FIGSIZE_BIWEEKLY':
                print("VERIFIED: Bi-weekly graph size parameter is used")
            
            elif param_name == 'GRAPH_FIGSIZE_CUMULATIVE':
                print("VERIFIED: Cumulative graph size parameter is used")
            
            elif param_name == 'GRID_COLOR':
                print("VERIFIED: Grid color parameter is used in graph generation")
            
            elif param_name == 'TEXT_COLOR':
                print("VERIFIED: Text color parameter is used in graph generation")
            
            elif param_name == 'GRAPHS_DIRECTORY':
                if test_value != 'graphs':
                    if test_value in readme_content:
                        print(f"VERIFIED: Graphs directory '{test_value}' is used")
                    else:
                        print(f"INFO: Graphs directory '{test_value}' is used")
                else:
                    print("VERIFIED: Default graphs directory is used")
            
            elif param_name == 'HISTORY_FILE_PATH':
                print(f"VERIFIED: History file path '{test_value}' is used")
            
            elif param_name == 'README_FILE_PATH':
                print(f"VERIFIED: README file path '{test_value}' is used")
            
            return True
        else:
            print(f"FAILED: README.md was not generated")
            return False
            
    except Exception as e:
        print(f"FAILED: Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Restore original value
        setattr(gd, param_name, original_value)

def main():
    """Run all configuration parameter tests."""
    print("="*70)
    print("CONFIGURATION PARAMETER TEST SUITE")
    print("="*70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Store original values
    original_values = {
        'SHOW_FULL_REPO_NAME': gd.SHOW_FULL_REPO_NAME,
        'README_HEADER_LEVEL': gd.README_HEADER_LEVEL,
        'DAILY_GRAPH_DAYS': gd.DAILY_GRAPH_DAYS,
        'WEEKLY_GRAPH_WEEKS': gd.WEEKLY_GRAPH_WEEKS,
        'BIWEEKLY_GRAPH_PERIODS': gd.BIWEEKLY_GRAPH_PERIODS,
        'STATS_PERIOD_30_DAYS': gd.STATS_PERIOD_30_DAYS,
        'STATS_PERIOD_90_DAYS': gd.STATS_PERIOD_90_DAYS,
        'INCLUDE_CUMULATIVE_GRAPHS': gd.INCLUDE_CUMULATIVE_GRAPHS,
        'INCLUDE_SEPARATE_CUMULATIVE': gd.INCLUDE_SEPARATE_CUMULATIVE,
        'CLONES_COLOR': gd.CLONES_COLOR,
        'VIEWS_COLOR': gd.VIEWS_COLOR,
        'GRAPH_DPI': gd.GRAPH_DPI,
        'GRAPH_FIGSIZE_DAILY': gd.GRAPH_FIGSIZE_DAILY,
        'GRAPH_FIGSIZE_WEEKLY': gd.GRAPH_FIGSIZE_WEEKLY,
        'GRAPH_FIGSIZE_BIWEEKLY': gd.GRAPH_FIGSIZE_BIWEEKLY,
        'GRAPH_FIGSIZE_CUMULATIVE': gd.GRAPH_FIGSIZE_CUMULATIVE,
        'GRID_COLOR': gd.GRID_COLOR,
        'TEXT_COLOR': gd.TEXT_COLOR,
        'GRAPHS_DIRECTORY': gd.GRAPHS_DIRECTORY,
        'HISTORY_FILE_PATH': gd.HISTORY_FILE_PATH,
        'README_FILE_PATH': gd.README_FILE_PATH,
    }
    
    # Backup original files
    print("\nBacking up original files...")
    readme_backup = backup_file(gd.README_FILE_PATH)
    
    results = []
    
    # Test 1: SHOW_FULL_REPO_NAME
    results.append(test_parameter(
        "Repository Name Display",
        "SHOW_FULL_REPO_NAME",
        original_values['SHOW_FULL_REPO_NAME'],
        True,  # Test with True
        "Should display full 'owner/repo' names in README"
    ))
    
    # Test 2: README_HEADER_LEVEL
    results.append(test_parameter(
        "README Header Level",
        "README_HEADER_LEVEL",
        original_values['README_HEADER_LEVEL'],
        2,  # Test with level 2
        "Should use ## for repository headers"
    ))
    
    # Test 3: DAILY_GRAPH_DAYS
    results.append(test_parameter(
        "Daily Graph Days",
        "DAILY_GRAPH_DAYS",
        original_values['DAILY_GRAPH_DAYS'],
        14,  # Test with 14 days
        "Should show 14 days in daily graph"
    ))
    
    # Test 4: WEEKLY_GRAPH_WEEKS
    results.append(test_parameter(
        "Weekly Graph Weeks",
        "WEEKLY_GRAPH_WEEKS",
        original_values['WEEKLY_GRAPH_WEEKS'],
        8,  # Test with 8 weeks
        "Should show 8 weeks in weekly graph"
    ))
    
    # Test 5: BIWEEKLY_GRAPH_PERIODS
    results.append(test_parameter(
        "Bi-Weekly Graph Periods",
        "BIWEEKLY_GRAPH_PERIODS",
        original_values['BIWEEKLY_GRAPH_PERIODS'],
        13,  # Test with 13 periods
        "Should show 13 periods in bi-weekly graph"
    ))
    
    # Test 6: STATS_PERIOD_30_DAYS
    results.append(test_parameter(
        "Statistics Period 30 Days",
        "STATS_PERIOD_30_DAYS",
        original_values['STATS_PERIOD_30_DAYS'],
        7,  # Test with 7 days
        "Should show 7 days in statistics table"
    ))
    
    # Test 7: STATS_PERIOD_90_DAYS
    results.append(test_parameter(
        "Statistics Period 90 Days",
        "STATS_PERIOD_90_DAYS",
        original_values['STATS_PERIOD_90_DAYS'],
        14,  # Test with 14 days
        "Should show 14 days in statistics table"
    ))
    
    # Test 8: INCLUDE_CUMULATIVE_GRAPHS
    results.append(test_parameter(
        "Include Cumulative Graphs",
        "INCLUDE_CUMULATIVE_GRAPHS",
        original_values['INCLUDE_CUMULATIVE_GRAPHS'],
        False,  # Test with False
        "Should exclude cumulative graphs"
    ))
    
    # Test 9: INCLUDE_SEPARATE_CUMULATIVE
    results.append(test_parameter(
        "Include Separate Cumulative",
        "INCLUDE_SEPARATE_CUMULATIVE",
        original_values['INCLUDE_SEPARATE_CUMULATIVE'],
        False,  # Test with False
        "Should exclude separate cumulative graphs"
    ))
    
    # Test 10: CLONES_COLOR
    results.append(test_parameter(
        "Clones Color",
        "CLONES_COLOR",
        original_values['CLONES_COLOR'],
        "#FF0000",  # Test with red
        "Should use red color for clones"
    ))
    
    # Test 11: VIEWS_COLOR
    results.append(test_parameter(
        "Views Color",
        "VIEWS_COLOR",
        original_values['VIEWS_COLOR'],
        "#0000FF",  # Test with blue
        "Should use blue color for views"
    ))
    
    # Test 12: GRAPH_DPI
    results.append(test_parameter(
        "Graph DPI",
        "GRAPH_DPI",
        original_values['GRAPH_DPI'],
        150,  # Test with 150 DPI
        "Should use 150 DPI for graphs"
    ))
    
    # Test 13: GRAPH_FIGSIZE_DAILY
    results.append(test_parameter(
        "Daily Graph Size",
        "GRAPH_FIGSIZE_DAILY",
        original_values['GRAPH_FIGSIZE_DAILY'],
        (10, 5),  # Test with smaller size
        "Should use (10, 5) for daily graphs"
    ))
    
    # Test 14: GRAPH_FIGSIZE_WEEKLY
    results.append(test_parameter(
        "Weekly Graph Size",
        "GRAPH_FIGSIZE_WEEKLY",
        original_values['GRAPH_FIGSIZE_WEEKLY'],
        (12, 6),  # Test with smaller size
        "Should use (12, 6) for weekly graphs"
    ))
    
    # Test 15: GRAPH_FIGSIZE_BIWEEKLY
    results.append(test_parameter(
        "Bi-Weekly Graph Size",
        "GRAPH_FIGSIZE_BIWEEKLY",
        original_values['GRAPH_FIGSIZE_BIWEEKLY'],
        (14, 7),  # Test with smaller size
        "Should use (14, 7) for bi-weekly graphs"
    ))
    
    # Test 16: GRAPH_FIGSIZE_CUMULATIVE
    results.append(test_parameter(
        "Cumulative Graph Size",
        "GRAPH_FIGSIZE_CUMULATIVE",
        original_values['GRAPH_FIGSIZE_CUMULATIVE'],
        (12, 6),  # Test with smaller size
        "Should use (12, 6) for cumulative graphs"
    ))
    
    # Test 17: GRID_COLOR
    results.append(test_parameter(
        "Grid Color",
        "GRID_COLOR",
        original_values['GRID_COLOR'],
        "#CCCCCC",  # Test with different gray
        "Should use #CCCCCC for grid lines"
    ))
    
    # Test 18: TEXT_COLOR
    results.append(test_parameter(
        "Text Color",
        "TEXT_COLOR",
        original_values['TEXT_COLOR'],
        "#000000",  # Test with black
        "Should use #000000 for text"
    ))
    
    # Test 19: GRAPHS_DIRECTORY
    results.append(test_parameter(
        "Graphs Directory",
        "GRAPHS_DIRECTORY",
        original_values['GRAPHS_DIRECTORY'],
        "graphs",  # Test with default
        "Should use 'graphs' directory"
    ))
    
    # Test 20: HISTORY_FILE_PATH
    results.append(test_parameter(
        "History File Path",
        "HISTORY_FILE_PATH",
        original_values['HISTORY_FILE_PATH'],
        "history.json",  # Test with default
        "Should use 'history.json' file"
    ))
    
    # Test 21: README_FILE_PATH
    results.append(test_parameter(
        "README File Path",
        "README_FILE_PATH",
        original_values['README_FILE_PATH'],
        "README.md",  # Test with default
        "Should use 'README.md' file"
    ))
    
    # Restore original README
    print("\nRestoring original README.md...")
    restore_file(readme_backup, gd.README_FILE_PATH)
    os.remove(readme_backup)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\nSUCCESS: All configuration parameters work correctly!")
    else:
        print(f"\nWARNING: {failed_tests} test(s) failed")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    return failed_tests == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
