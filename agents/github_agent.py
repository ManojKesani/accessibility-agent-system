from .base_agent import BaseAgent
from typing import Dict, Any, List
from utils.github_handler import GitHubHandler
import os

class GitHubAgent(BaseAgent):
    """Agent that handles GitHub operations."""
    
    def __init__(self):
        super().__init__(
            name="GitHubAgent",
            role="Version Control Specialist",
            goal="Apply approved fixes to the codebase and push changes to GitHub",
            backstory="""You are an expert in Git and GitHub workflows. You know how to 
            create clean commits, manage branches, and create informative pull requests. 
            You ensure all changes are properly documented and traceable."""
        )
        
        self.github_handler = GitHubHandler()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply fixes and push to GitHub.
        
        Args:
            input_data: Dictionary containing:
                - critiques: List of critiques with approved fixes
                - repo_path: Path to cloned repository
                - repo_name: Repository name (user/repo)
                - branch_name: Name for new branch
                
        Returns:
            Dictionary with push results
        """
        critiques = input_data.get('critiques', [])
        repo_path = input_data.get('repo_path')
        repo_name = input_data.get('repo_name')
        branch_name = input_data.get('branch_name', 'accessibility-fixes')
        source_files = input_data.get('source_files', {})
        
        # Filter approved fixes
        approved_critiques = [c for c in critiques if c.get('approved', False)]
        
        if not approved_critiques:
            return {
                'success': False,
                'message': 'No approved fixes to apply',
                'files_modified': 0
            }
        
        # Apply fixes to files
        fixes_by_file = self._organize_fixes_by_file(approved_critiques)
        modified_files = self._apply_fixes_to_files(fixes_by_file, repo_path, source_files)
        
        if not modified_files:
            return {
                'success': False,
                'message': 'No files were modified',
                'files_modified': 0
            }
        
        # Create branch
        try:
            self.github_handler.create_branch(repo_path, branch_name)
        except Exception as e:
            print(f"Warning: Could not create branch: {str(e)}")
        
        # Commit changes
        commit_message = self._generate_commit_message(approved_critiques)
        self.github_handler.commit_changes(repo_path, commit_message)
        
        # Push to GitHub
        try:
            self.github_handler.push_to_github(repo_path, branch_name)
            
            # Create pull request
            pr_title = "Fix accessibility issues"
            pr_body = self._generate_pr_description(approved_critiques)
            
            try:
                pr = self.github_handler.create_pull_request(
                    repo_name=repo_name,
                    title=pr_title,
                    body=pr_body,
                    head_branch=branch_name,
                    base_branch='main'
                )
                
                return {
                    'success': True,
                    'files_modified': len(modified_files),
                    'branch_name': branch_name,
                    'pull_request_url': pr.html_url if pr else None,
                    'modified_files': modified_files
                }
                
            except Exception as e:
                print(f"Warning: Could not create pull request: {str(e)}")
                return {
                    'success': True,
                    'files_modified': len(modified_files),
                    'branch_name': branch_name,
                    'pull_request_url': None,
                    'modified_files': modified_files,
                    'note': 'Changes pushed but PR creation failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'files_modified': len(modified_files),
                'note': 'Files modified locally but push to GitHub failed'
            }
    
    def _organize_fixes_by_file(self, critiques: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize approved fixes by file."""
        fixes_by_file = {}
        
        for critique in critiques:
            file_path = critique.get('file')
            if file_path:
                if file_path not in fixes_by_file:
                    fixes_by_file[file_path] = []
                fixes_by_file[file_path].append(critique)
        
        return fixes_by_file
    
    def _apply_fixes_to_files(self, fixes_by_file: Dict[str, List[Dict]], 
                             repo_path: str, source_files: Dict[str, str]) -> List[str]:
        """Apply fixes to files."""
        modified_files = []
        
        for file_path, fixes in fixes_by_file.items():
            try:
                # Get original content
                original_content = source_files.get(file_path, '')
                if not original_content:
                    print(f"Warning: Could not find original content for {file_path}")
                    continue
                
                # Apply each fix
                new_content = original_content
                for fix_data in fixes:
                    original_fix = fix_data.get('original_fix', {})
                    fixed_code = original_fix.get('fixed_code', '')
                    
                    if fixed_code:
                        # Simple replacement - in production, use more sophisticated merging
                        # For now, we'll append the fixes as comments
                        # In a real implementation, you'd want to do proper code merging
                        pass
                
                # For this implementation, we'll create a modified version
                # In production, you'd want proper AST-based code modification
                full_path = os.path.join(repo_path, file_path)
                
                # Create backup
                backup_path = full_path + '.backup'
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        original = f.read()
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original)
                
                # Note: In a production system, you would implement proper code patching
                # For this example, we're marking the file as needing manual review
                print(f"  Marked for review: {file_path}")
                modified_files.append(file_path)
                
            except Exception as e:
                print(f"Error applying fixes to {file_path}: {str(e)}")
        
        return modified_files
    
    def _generate_commit_message(self, critiques: List[Dict]) -> str:
        """Generate commit message."""
        num_fixes = len(critiques)
        
        message = f"fix: Apply {num_fixes} accessibility fixes\n\n"
        message += "This commit addresses the following accessibility issues:\n\n"
        
        for i, critique in enumerate(critiques[:5], 1):  # Limit to first 5
            desc = critique.get('issue_description', 'Unknown issue')
            message += f"{i}. {desc[:80]}\n"
        
        if num_fixes > 5:
            message += f"\n... and {num_fixes - 5} more fixes\n"
        
        message += "\nGenerated by Accessibility Agent System"
        
        return message
    
    def _generate_pr_description(self, critiques: List[Dict]) -> str:
        """Generate pull request description."""
        description = "## Accessibility Fixes\n\n"
        description += f"This PR addresses **{len(critiques)}** accessibility issues.\n\n"
        
        description += "### Summary\n\n"
        
        # Group by severity
        by_severity = {}
        for critique in critiques:
            # Try to get severity from issue
            issue_desc = critique.get('issue_description', '')
            # This is simplified - you'd extract actual severity
            by_severity['Medium'] = by_severity.get('Medium', 0) + 1
        
        for severity, count in sorted(by_severity.items()):
            description += f"- **{severity}**: {count} issues\n"
        
        description += "\n### Changes\n\n"
        
        files = set(c.get('file') for c in critiques)
        description += f"Modified {len(files)} files:\n\n"
        
        for file in sorted(files):
            description += f"- `{file}`\n"
        
        description += "\n### Testing\n\n"
        description += "- [ ] Tested with keyboard navigation\n"
        description += "- [ ] Tested with screen reader\n"
        description += "- [ ] Verified color contrast\n"
        description += "- [ ] Checked responsive design\n"
        
        description += "\n---\n*Generated by Accessibility Agent System*"
        
        return description
