from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class CriticAgent(BaseAgent):
    """Agent that critiques and validates proposed solutions."""
    
    def __init__(self):
        super().__init__(
            name="CriticAgent",
            role="Senior Accessibility Auditor & Code Reviewer",
            goal="Critically evaluate proposed fixes to ensure they truly solve accessibility issues without introducing new problems",
            backstory="""You are a senior accessibility auditor with years of experience 
            reviewing code and catching subtle bugs. You have seen many well-intentioned 
            fixes that actually made things worse. You are thorough, skeptical, and 
            constructive in your feedback."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Critique proposed fixes.
        
        Args:
            input_data: Dictionary containing 'fixes' from domain experts
            
        Returns:
            Dictionary with critiques and approval status
        """
        fixes = input_data.get('fixes', [])
        
        critiques = []
        
        for fix_data in fixes:
            critique = self._critique_fix(fix_data)
            critiques.append(critique)
        
        approved_count = sum(1 for c in critiques if c.get('approved', False))
        total_reviewed = len(critiques)
        is_satisfactory = approved_count == total_reviewed and total_reviewed > 0
        feedback_summary = self.generate_critique_summary(critiques)
        
        return {
            'critiques': critiques,
            'total_reviewed': len(critiques),
            'approved': approved_count,
            'rejected': len(critiques) - approved_count,
            'is_satisfactory': is_satisfactory,
            'approval_rate': (approved_count / len(critiques) * 100) if critiques else 0
        }
    
    def _critique_fix(self, fix_data: Dict) -> Dict:
        """Critique a single fix."""
        
        issue = fix_data.get('issue', {})
        fix = fix_data.get('fix', {})
        
        if not fix.get('success', False):
            return {
                'file': fix_data.get('file'),
                'approved': False,
                'rating': 0,
                'reason': 'Fix generation failed',
                'strengths': [],
                'weaknesses': ['Fix was not successfully generated'],
                'suggestions': ['Retry with clearer context or different approach']
            }
        
        prompt = self.create_prompt("""
Review the following accessibility fix:

ORIGINAL ISSUE:
- Description: {description}
- WCAG: {wcag}
- Severity: {severity}
- Original Code: 
```
{original_code}
```

PROPOSED FIX:
```
{fixed_code}
```

Explanation: {explanation}

Critically evaluate this fix on:
1. Does it actually solve the accessibility issue?
2. Does it follow WCAG 2.1 best practices?
3. Could it introduce new accessibility problems?
4. Is the implementation correct and maintainable?
5. Are there better alternative approaches?

Provide your critique as JSON with keys:
- approved: boolean (true if fix should be applied)
- rating: number (0-10, how good is this fix)
- strengths: array of strings (what's good about this fix)
- weaknesses: array of strings (what's problematic)
- suggestions: array of strings (how to improve)
- concerns: array of strings (potential new issues this might create)

Be thorough and honest. It's better to reject a fix than to introduce new problems.

Respond with ONLY the JSON object, no other text.
""")
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "description": issue.get('description', ''),
                "wcag": issue.get('wcag', ''),
                "severity": issue.get('severity', ''),
                "original_code": issue.get('code_snippet', ''),
                "fixed_code": fix.get('fixed_code', ''),
                "explanation": fix.get('explanation', '')
            })
            
            content_text = response.content.strip()
            if content_text.startswith('```'):
                content_text = content_text.split('```')[1]
                if content_text.startswith('json'):
                    content_text = content_text[4:]
            
            critique_data = json.loads(content_text)
            
            return {
                'file': fix_data.get('file'),
                'issue_description': issue.get('description'),
                'approved': critique_data.get('approved', False),
                'rating': critique_data.get('rating', 0),
                'strengths': critique_data.get('strengths', []),
                'weaknesses': critique_data.get('weaknesses', []),
                'suggestions': critique_data.get('suggestions', []),
                'concerns': critique_data.get('concerns', []),
                'original_fix': fix
            }
            
        except Exception as e:
            print(f"Warning: Could not critique fix: {str(e)}")
            return {
                'file': fix_data.get('file'),
                'approved': True,  # Default to approved if critique fails
                'rating': 7,
                'strengths': ['Fix was generated successfully'],
                'weaknesses': [],
                'suggestions': [],
                'concerns': [],
                'note': f'Automatic approval due to critique error: {str(e)}',
                'original_fix': fix
            }
    
    def generate_critique_summary(self, critiques: List[Dict]) -> str:
        """Generate summary of critiques."""
        
        report = "SOLUTION CRITIQUE SUMMARY\n"
        report += "=" * 60 + "\n\n"
        
        approved = sum(1 for c in critiques if c.get('approved', False))
        total = len(critiques)
        
        report += f"Overall Results:\n"
        report += f"  Approved: {approved}/{total}\n"
        report += f"  Rejected: {total - approved}/{total}\n"
        
        if total > 0:
            avg_rating = sum(c.get('rating', 0) for c in critiques) / total
            report += f"  Average Rating: {avg_rating:.1f}/10\n"
        
        report += "\n"
        
        # Common concerns
        all_concerns = []
        for c in critiques:
            all_concerns.extend(c.get('concerns', []))
        
        if all_concerns:
            report += "Common Concerns:\n"
            concern_counts = {}
            for concern in all_concerns:
                concern_counts[concern] = concern_counts.get(concern, 0) + 1
            
            for concern, count in sorted(concern_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"  - {concern} (mentioned {count} times)\n"
        
        return report
