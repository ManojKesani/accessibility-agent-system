import os
from datetime import datetime
from typing import Dict, List
import json
import config

class ReportGenerator:
    """Generate accessibility reports."""
    
    def __init__(self, report_dir: str = None):
        self.report_dir = report_dir or config.REPORTS_DIR
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_accessibility_report(self, issues: List[Dict], 
                                     repo_name: str) -> str:
        """
        Generate accessibility issues report.
        
        Args:
            issues: List of accessibility issues
            repo_name: Name of the repository
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"accessibility_report_{repo_name}_{timestamp}.txt"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"ACCESSIBILITY AUDIT REPORT\n")
            f.write(f"Repository: {repo_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Summary
            f.write(f"SUMMARY\n")
            f.write(f"-" * 80 + "\n")
            f.write(f"Total Issues Found: {len(issues)}\n")
            
            # Group by severity
            severity_counts = {}
            for issue in issues:
                severity = issue.get('severity', 'Unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            for severity, count in sorted(severity_counts.items()):
                f.write(f"{severity}: {count}\n")
            
            f.write("\n")
            
            # Detailed issues
            f.write(f"DETAILED ISSUES\n")
            f.write(f"-" * 80 + "\n\n")
            
            for idx, issue in enumerate(issues, 1):
                f.write(f"Issue #{idx}\n")
                f.write(f"  File: {issue.get('file', 'Unknown')}\n")
                f.write(f"  Line: {issue.get('line', 'Unknown')}\n")
                f.write(f"  Severity: {issue.get('severity', 'Unknown')}\n")
                f.write(f"  Category: {issue.get('category', 'Unknown')}\n")
                f.write(f"  WCAG: {issue.get('wcag', 'Unknown')}\n")
                f.write(f"  Description: {issue.get('description', 'No description')}\n")
                f.write(f"  Impact: {issue.get('impact', 'No impact description')}\n")
                f.write(f"  Recommendation: {issue.get('recommendation', 'No recommendation')}\n")
                f.write("\n")
        
        print(f"✓ Accessibility report generated: {filepath}")
        return filepath
    
    def generate_fix_report(self, fixes: Dict[str, Dict], 
                           repo_name: str) -> str:
        """
        Generate fix implementation report.
        
        Args:
            fixes: Dictionary of fixes applied
            repo_name: Name of the repository
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fix_report_{repo_name}_{timestamp}.txt"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"ACCESSIBILITY FIX REPORT\n")
            f.write(f"Repository: {repo_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"SUMMARY\n")
            f.write(f"-" * 80 + "\n")
            f.write(f"Total Files Modified: {len(fixes)}\n\n")
            
            for file_path, fix_info in fixes.items():
                f.write(f"File: {file_path}\n")
                f.write(f"  Issues Fixed: {len(fix_info.get('issues_fixed', []))}\n")
                f.write(f"  Changes Made:\n")
                
                for change in fix_info.get('changes', []):
                    f.write(f"    - {change}\n")
                
                f.write("\n")
        
        print(f"✓ Fix report generated: {filepath}")
        return filepath
    
    def generate_critique_report(self, critiques: List[Dict], 
                                 repo_name: str) -> str:
        """
        Generate critique report.
        
        Args:
            critiques: List of critiques
            repo_name: Name of the repository
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"critique_report_{repo_name}_{timestamp}.txt"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"SOLUTION CRITIQUE REPORT\n")
            f.write(f"Repository: {repo_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, critique in enumerate(critiques, 1):
                f.write(f"Critique #{idx}\n")
                f.write(f"  File: {critique.get('file', 'Unknown')}\n")
                f.write(f"  Rating: {critique.get('rating', 'N/A')}/10\n")
                f.write(f"  Strengths:\n")
                for strength in critique.get('strengths', []):
                    f.write(f"    + {strength}\n")
                f.write(f"  Weaknesses:\n")
                for weakness in critique.get('weaknesses', []):
                    f.write(f"    - {weakness}\n")
                f.write(f"  Suggestions:\n")
                for suggestion in critique.get('suggestions', []):
                    f.write(f"    • {suggestion}\n")
                f.write(f"  Approved: {critique.get('approved', False)}\n")
                f.write("\n")
        
        print(f"✓ Critique report generated: {filepath}")
        return filepath
    
    def save_json_report(self, data: Dict, filename: str) -> str:
        """Save report data as JSON."""
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ JSON report saved: {filepath}")
        return filepath
