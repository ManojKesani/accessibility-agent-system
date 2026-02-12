from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class HTMLAccessibilityExpert(BaseAgent):
    """Expert in fixing HTML accessibility issues."""
    
    def __init__(self):
        super().__init__(
            name="HTMLAccessibilityExpert",
            role="HTML & ARIA Specialist",
            goal="Fix HTML and ARIA-related accessibility issues following best practices",
            backstory="""You are an expert in semantic HTML and ARIA. You know when to 
            use native HTML elements vs ARIA attributes, and you always prioritize 
            semantic markup. You understand the accessibility tree and how assistive 
            technologies interpret HTML."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix HTML-related accessibility issues."""
        issue = input_data.get('issue')
        file_content = input_data.get('file_content')
        
        return self._generate_fix(issue, file_content)
    
    def _generate_fix(self, issue: Dict, file_content: str) -> Dict:
        """Generate fix for HTML issue."""
        
        prompt = self.create_prompt("""
Fix the following HTML accessibility issue:

Issue: {description}
WCAG: {wcag}
Current Code:
```
{code_snippet}
```

Recommendation: {recommendation}

Provide the corrected code that:
1. Fixes the accessibility issue
2. Maintains the original functionality
3. Follows HTML best practices
4. Uses semantic HTML where possible
5. Implements ARIA correctly (only when necessary)

Return your response as JSON with keys:
- fixed_code: string (the corrected code)
- explanation: string (what was changed and why)
- additional_notes: string (any other considerations)

Respond with ONLY the JSON object, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "description": issue.get('description', ''),
                "wcag": issue.get('wcag', ''),
                "code_snippet": issue.get('code_snippet', ''),
                "recommendation": issue.get('recommendation', '')
            })
            
            content_text = response.content.strip()
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            fix_data = json.loads(content_text)
            
            return {
                'success': True,
                'fixed_code': fix_data.get('fixed_code'),
                'explanation': fix_data.get('explanation'),
                'additional_notes': fix_data.get('additional_notes'),
                'issue': issue
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'issue': issue
            }


class CSSAccessibilityExpert(BaseAgent):
    """Expert in fixing CSS accessibility issues."""
    
    def __init__(self):
        super().__init__(
            name="CSSAccessibilityExpert",
            role="CSS & Visual Accessibility Specialist",
            goal="Fix CSS-related accessibility issues including color contrast, focus indicators, and responsive design",
            backstory="""You are an expert in CSS accessibility. You understand color 
            contrast ratios, focus management, responsive design, and how CSS affects 
            screen readers. You know how to make beautiful designs that are also accessible."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix CSS-related accessibility issues."""
        issue = input_data.get('issue')
        file_content = input_data.get('file_content')
        
        return self._generate_fix(issue, file_content)
    
    def _generate_fix(self, issue: Dict, file_content: str) -> Dict:
        """Generate fix for CSS issue."""
        
        prompt = self.create_prompt("""
Fix the following CSS accessibility issue:

Issue: {description}
WCAG: {wcag}
Current Code:
```
{code_snippet}
```

Recommendation: {recommendation}

Provide the corrected CSS that:
1. Fixes the accessibility issue
2. Maintains visual design intent
3. Ensures WCAG 2.1 AA compliance (or AAA where possible)
4. Works across different screen sizes
5. Supports keyboard navigation and focus indicators

Return your response as JSON with keys:
- fixed_code: string (the corrected CSS)
- explanation: string (what was changed and why)
- additional_notes: string (any other considerations)

Respond with ONLY the JSON object, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "description": issue.get('description', ''),
                "wcag": issue.get('wcag', ''),
                "code_snippet": issue.get('code_snippet', ''),
                "recommendation": issue.get('recommendation', '')
            })
            
            content_text = response.content.strip()
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            fix_data = json.loads(content_text)
            
            return {
                'success': True,
                'fixed_code': fix_data.get('fixed_code'),
                'explanation': fix_data.get('explanation'),
                'additional_notes': fix_data.get('additional_notes'),
                'issue': issue
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'issue': issue
            }


class JavaScriptAccessibilityExpert(BaseAgent):
    """Expert in fixing JavaScript accessibility issues."""
    
    def __init__(self):
        super().__init__(
            name="JavaScriptAccessibilityExpert",
            role="JavaScript & Interactive Accessibility Specialist",
            goal="Fix JavaScript-related accessibility issues including keyboard interaction, dynamic content, and focus management",
            backstory="""You are an expert in accessible JavaScript. You understand how 
            to make dynamic web applications accessible, manage focus programmatically, 
            announce changes to screen readers, and implement keyboard navigation patterns."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix JavaScript-related accessibility issues."""
        issue = input_data.get('issue')
        file_content = input_data.get('file_content')
        
        return self._generate_fix(issue, file_content)
    
    def _generate_fix(self, issue: Dict, file_content: str) -> Dict:
        """Generate fix for JavaScript issue."""
        
        prompt = self.create_prompt("""
Fix the following JavaScript accessibility issue:

Issue: {description}
WCAG: {wcag}
Current Code:
```
{code_snippet}
```

Recommendation: {recommendation}

Provide the corrected JavaScript that:
1. Fixes the accessibility issue
2. Maintains functionality
3. Supports keyboard-only users
4. Manages focus appropriately
5. Announces changes to screen readers (using ARIA live regions if needed)

Return your response as JSON with keys:
- fixed_code: string (the corrected JavaScript)
- explanation: string (what was changed and why)
- additional_notes: string (any other considerations)

Respond with ONLY the JSON object, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "description": issue.get('description', ''),
                "wcag": issue.get('wcag', ''),
                "code_snippet": issue.get('code_snippet', ''),
                "recommendation": issue.get('recommendation', '')
            })
            
            content_text = response.content.strip()
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            fix_data = json.loads(content_text)
            
            return {
                'success': True,
                'fixed_code': fix_data.get('fixed_code'),
                'explanation': fix_data.get('explanation'),
                'additional_notes': fix_data.get('additional_notes'),
                'issue': issue
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'issue': issue
            }
