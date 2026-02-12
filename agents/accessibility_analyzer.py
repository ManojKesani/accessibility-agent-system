from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class AccessibilityAnalyzer(BaseAgent):
    """Agent that analyzes code for accessibility issues."""
    
    def __init__(self):
        super().__init__(
            name="AccessibilityAnalyzer",
            role="Accessibility Expert",
            goal="Identify all WCAG accessibility violations in website source code",
            backstory="""You are an expert in web accessibility with deep knowledge of 
            WCAG 2.1 guidelines, ARIA best practices, and modern web standards. You have 
            audited thousands of websites and can identify both obvious and subtle 
            accessibility issues."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze source code for accessibility issues.
        
        Args:
            input_data: Dictionary containing 'source_files' (Dict[str, str])
            
        Returns:
            Dictionary with 'issues' list and 'report'
        """
        source_files = input_data.get('source_files', {})
        
        all_issues = []
        
        for file_path, content in source_files.items():
            if not content.strip():
                continue
            
            # Analyze each file
            issues = self._analyze_file(file_path, content)
            all_issues.extend(issues)
        
        report = self._generate_report(all_issues)
        
        return {
            'issues': all_issues,
            'report': report,
            'total_issues': len(all_issues),
            'files_analyzed': len(source_files)
        }
    
    def _analyze_file(self, file_path: str, content: str) -> List[Dict]:
        """Analyze a single file for accessibility issues."""
        
        prompt = self.create_prompt("""
Analyze the following source code file for accessibility issues according to WCAG 2.1 guidelines.

File: {file_path}

Source Code:
```
{content}
```

Identify ALL accessibility issues in this file. For each issue, provide:
1. Severity (Critical, High, Medium, Low)
2. WCAG criterion violated (e.g., 1.1.1, 2.4.1)
3. Category (Perceivable, Operable, Understandable, Robust)
4. Line number (approximate if exact is not clear)
5. Description of the issue
6. Impact on users
7. Specific recommendation to fix

Return your response as a JSON array of issues. Each issue should be an object with keys:
file, line, severity, wcag, category, description, impact, recommendation

Example:
[
  {{
    "file": "index.html",
    "line": 15,
    "severity": "Critical",
    "wcag": "1.1.1",
    "category": "Perceivable",
    "description": "Image missing alt text",
    "impact": "Screen reader users cannot understand image content",
    "recommendation": "Add descriptive alt attribute to the img tag"
  }}
]

Respond with ONLY the JSON array, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "file_path": file_path,
                "content": content[:8000]  # Limit content size
            })
            
            # Parse JSON response
            content_text = response.content.strip()
            
            # Remove markdown code blocks if present
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            issues = json.loads(content_text)
            
            # Ensure file path is set correctly
            for issue in issues:
                issue['file'] = file_path
            
            return issues
            
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse JSON for {file_path}: {str(e)}")
            return []
        except Exception as e:
            print(f"Warning: Error analyzing {file_path}: {str(e)}")
            return []
    
    def _generate_report(self, issues: List[Dict]) -> str:
        """Generate summary report from issues."""
        
        if not issues:
            return "No accessibility issues found."
        
        report = f"Found {len(issues)} accessibility issues:\n\n"
        
        # Group by severity
        by_severity = {}
        for issue in issues:
            severity = issue.get('severity', 'Unknown')
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        report += "By Severity:\n"
        for severity in ['Critical', 'High', 'Medium', 'Low']:
            count = by_severity.get(severity, 0)
            if count > 0:
                report += f"  {severity}: {count}\n"
        
        # Group by category
        by_category = {}
        for issue in issues:
            category = issue.get('category', 'Unknown')
            by_category[category] = by_category.get(category, 0) + 1
        
        report += "\nBy Category:\n"
        for category, count in sorted(by_category.items()):
            report += f"  {category}: {count}\n"
        
        return report
