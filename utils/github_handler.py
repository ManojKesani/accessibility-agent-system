import os
import git
import shutil
from github import Github
from typing import Optional, Dict, List
import tempfile
import config

class GitHubHandler:
    """Handle GitHub repository operations."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or config.GITHUB_TOKEN
        self.github = Github(self.token) if self.token else None
        self.temp_dir = None
        
    def clone_repository(self, repo_url: str, target_dir: Optional[str] = None) -> str:
        """
        Clone a GitHub repository.
        
        Args:
            repo_url: URL of the repository to clone
            target_dir: Optional target directory
            
        Returns:
            Path to cloned repository
        """
        if target_dir is None:
            target_dir = tempfile.mkdtemp(dir=config.TEMP_DIR)
            
        self.temp_dir = target_dir
        
        try:
            git.Repo.clone_from(repo_url, target_dir)
            print(f"✓ Repository cloned to {target_dir}")
            return target_dir
        except Exception as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def get_source_files(self, repo_path: str, extensions: List[str] = None) -> Dict[str, str]:
        """
        Get source files from repository.
        
        Args:
            repo_path: Path to repository
            extensions: List of file extensions to include (e.g., ['.html', '.css', '.js'])
            
        Returns:
            Dictionary mapping file paths to content
        """
        if extensions is None:
            extensions = ['.html', '.htm', '.css', '.js', '.jsx', '.tsx', '.vue']
        
        source_files = {}
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'dist', 'build']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source_files[relative_path] = f.read()
                    except Exception as e:
                        print(f"Warning: Could not read {relative_path}: {str(e)}")
        
        return source_files
    
    def create_branch(self, repo_path: str, branch_name: str):
        """Create a new branch in the repository."""
        try:
            repo = git.Repo(repo_path)
            repo.git.checkout('-b', branch_name)
            print(f"✓ Created branch: {branch_name}")
        except Exception as e:
            raise Exception(f"Failed to create branch: {str(e)}")
    
    def commit_changes(self, repo_path: str, message: str):
        """Commit changes to the repository."""
        try:
            repo = git.Repo(repo_path)
            repo.git.add(A=True)
            repo.index.commit(message)
            print(f"✓ Changes committed: {message}")
        except Exception as e:
            raise Exception(f"Failed to commit changes: {str(e)}")
    
    def push_to_github(self, repo_path: str, branch_name: str):
        """Push changes to GitHub."""
        try:
            repo = git.Repo(repo_path)
            origin = repo.remote('origin')
            origin.push(branch_name)
            print(f"✓ Pushed to GitHub: {branch_name}")
        except Exception as e:
            raise Exception(f"Failed to push to GitHub: {str(e)}")
    
    def create_pull_request(self, repo_name: str, title: str, body: str, 
                          head_branch: str, base_branch: str = "main"):
        """Create a pull request."""
        if not self.github:
            raise Exception("GitHub token not configured")
        
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            print(f"✓ Pull request created: {pr.html_url}")
            return pr
        except Exception as e:
            raise Exception(f"Failed to create pull request: {str(e)}")
    
    def apply_fixes(self, repo_path: str, fixes: Dict[str, str]):
        """
        Apply fixes to files in the repository.
        
        Args:
            repo_path: Path to repository
            fixes: Dictionary mapping file paths to new content
        """
        for file_path, new_content in fixes.items():
            full_path = os.path.join(repo_path, file_path)
            
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Write new content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                print(f"✓ Applied fix to {file_path}")
            except Exception as e:
                print(f"✗ Failed to apply fix to {file_path}: {str(e)}")
    
    def cleanup(self):
        """Clean up temporary directories."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"✓ Cleaned up {self.temp_dir}")
            except Exception as e:
                print(f"Warning: Could not clean up {self.temp_dir}: {str(e)}")
