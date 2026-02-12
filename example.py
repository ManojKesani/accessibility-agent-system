#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the Accessibility Agent System.
"""

import os
from workflows import AccessibilityWorkflow
import config

def main():
    # Set up API keys (or use environment variables)
    if not config.GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not set")
        print("Please set it in .env file or as environment variable")
        return
    
    # Example repository
    repo_url = "https://github.com/your-username/your-repo"
    repo_name = "your-username/your-repo"
    
    print("=" * 60)
    print("Accessibility Agent System - Example")
    print("=" * 60)
    print(f"Repository: {repo_name}")
    print(f"URL: {repo_url}")
    print()
    
    # Initialize workflow
    print("Initializing workflow...")
    workflow = AccessibilityWorkflow()
    
    # Run analysis
    print("Running analysis (this may take several minutes)...")
    print()
    
    result = workflow.run(repo_url, repo_name)
    
    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    print(f"\nIssues Found: {len(result.get('issues', []))}")
    print(f"Fixes Generated: {len(result.get('fixes', []))}")
    
    critiques = result.get('critiques', [])
    approved = sum(1 for c in critiques if c.get('approved', False))
    print(f"Approved Fixes: {approved}/{len(critiques)}")
    
    github_result = result.get('github_result', {})
    if github_result.get('success'):
        print(f"\n✅ Changes pushed to GitHub")
        print(f"Branch: {github_result.get('branch_name', 'N/A')}")
        if github_result.get('pull_request_url'):
            print(f"PR: {github_result['pull_request_url']}")
    else:
        print(f"\n⚠️  Changes not pushed to GitHub")
    
    # Show reports
    reports = result.get('reports', {})
    if reports:
        print(f"\n📄 Reports Generated:")
        for report_type, report_path in reports.items():
            print(f"  - {report_type}: {report_path}")
    
    # Show errors if any
    errors = result.get('errors', [])
    if errors:
        print(f"\n⚠️  Errors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
