from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class IssueLocator(BaseAgent):
    """Agent that maps accessibility issues to specific code locations."""
    
    def __init__(self):
        super().__init__(
            name="IssueLocator",
            role="Code Analysis Specialist",
            goal="Precisely locate accessibility issues in source code and identify the exact code that needs modification",
            backstory="""You are a meticulous code analyst with expertise in parsing and 
            understanding HTML, CSS, and JavaScript. You excel at pinpointing exact 
            locations of issues and identifying the minimal changes needed to fix them."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map issues to specific code locations.
        
        Args:
            input_data: Dictionary containing 'issues' and 'source_files'
            
        Returns:
            Dictionary with enriched issues including code context
        """
        issues = input_data.get('issues', [])
        source_files = input_data.get('source_files', {})
        
        enriched_issues = []
        
        for issue in issues:
            enriched = self._locate_issue(issue, source_files)
            enriched_issues.append(enriched)
        
        return {
            'enriched_issues': enriched_issues,
            'total_located': len(enriched_issues)
        }
    
    def _locate_issue(self, issue: Dict, source_files: Dict[str, str]) -> Dict:
        """Locate a specific issue in the source code."""
        
        file_path = issue.get('file')
        if file_path not in source_files:
            return {**issue, 'code_context': None, 'exact_location': None}
        
        content = source_files[file_path]
        
        prompt = self.create_prompt("""
Given an accessibility issue and the source code file, identify the exact code that needs to be fixed.

Issue Details:
- Description: {description}
- WCAG: {wcag}
- Recommendation: {recommendation}
- Approximate Line: {line}

Source Code:
```
{content}
```

Analyze the code and provide:
1. The exact line number where the issue occurs
2. The problematic code snippet (5-10 lines of context)
3. The specific element or attribute causing the issue
4. The minimum code change needed to fix it

Return your response as JSON with keys:
- exact_line: number
- code_snippet: string (the problematic code with context)
- problematic_element: string (what exactly is wrong)
- fix_approach: string (how to fix it)

Example:
{{
  "exact_line": 42,
  "code_snippet": "<img src='logo.png'>",
  "problematic_element": "img element without alt attribute",
  "fix_approach": "Add alt='Company Logo' to the img tag"
}}

Respond with ONLY the JSON object, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "description": issue.get('description', ''),
                "wcag": issue.get('wcag', ''),
                "recommendation": issue.get('recommendation', ''),
                "line": issue.get('line', 'Unknown'),
                "content": content[:6000]
            })
            
            # Parse JSON response
            content_text = response.content.strip()
            
            # Remove markdown code blocks if present
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            location_data = json.loads(content_text)
            
            return {
                **issue,
                'exact_line': location_data.get('exact_line'),
                'code_snippet': location_data.get('code_snippet'),
                'problematic_element': location_data.get('problematic_element'),
                'fix_approach': location_data.get('fix_approach')
            }
            
        except Exception as e:
            print(f"Warning: Could not locate issue precisely: {str(e)}")
            return {
                **issue,
                'exact_line': issue.get('line'),
                'code_snippet': None,
                'problematic_element': None,
                'fix_approach': issue.get('recommendation')
            }
