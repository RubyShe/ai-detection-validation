#!/usr/bin/env python3
"""
AI-PR-Watcher Detection Test Runner

This script creates controlled test cases to evaluate how ai-pr-watcher
detects AI-generated PRs based on their detection methodology.
"""

import sys
import os
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_watcher_tester import AIWatcherTester
from test_cases.test_code_samples import (
    TEST_1_HUMAN_CODE_COPILOT_BRANCH,
    TEST_2_AI_CODE_NORMAL_BRANCH,
    TEST_3_CLAUDE_CODE_PATTERN,
    TEST_4_HUMAN_CODE_CURSOR_BRANCH
)

def main():
    # Load environment variables
    load_dotenv()
    
    # Configuration
    REPO_OWNER = "RubyShe"
    REPO_NAME = "ai-detection-validation"
    
    print("🚀 Starting AI-PR-Watcher Detection Tests")
    print("=" * 60)
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print(f"Testing ai-pr-watcher detection methodology")
    print()
    
    # Initialize tester
    try:
        tester = AIWatcherTester(REPO_OWNER, REPO_NAME)
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please make sure GITHUB_TOKEN is set in your .env file")
        return
    
    # Define test cases
    test_cases = [
        {
            "name": "test_1_human_code_copilot_pattern",
            "branch": "copilot/simple-math-functions",
            "file_path": "src/simple_math.py", 
            "code": TEST_1_HUMAN_CODE_COPILOT_BRANCH,
            "commit_msg": "Add basic math functions for testing",
            "pr_title": "Add simple math utility functions",
            "pr_description": """## Description
Basic mathematical utility functions for the project.

## Changes
- Added `add_numbers()` function for addition
- Added `multiply_numbers()` function for multiplication  
- Added `calculate
