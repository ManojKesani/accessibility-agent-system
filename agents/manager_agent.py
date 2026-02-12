from .base_agent import BaseAgent
from .domain_experts import HTMLAccessibilityExpert, CSSAccessibilityExpert, JavaScriptAccessibilityExpert
from typing import Dict, Any, List
import json

class ManagerAgent(BaseAgent):
    """Manager agent that delegates tasks to domain experts."""
    
    def __init__(self):
        super().__init__(
            name="ManagerAgent",
            role="Accessibility Project Manager",
            goal="Efficiently delegate accessibility fixes to the right domain experts and coordinate their work",
            backstory="""You are an experienced project manager who understands web 
            accessibility and knows how to efficiently delegate tasks to specialists. 
            You understand which expert is best suited for each type of issue."""
        )
        
        # Initialize domain experts
        self.html_expert = HTMLAccessibilityExpert()
        self.css_expert = CSSAccessibilityExpert()
        self.js_expert = JavaScriptAccessibilityExpert()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delegate issues to appropriate domain experts.
        
        Args:
            input_data: Dictionary containing 'enriched_issues' and 'source_files'
            
        Returns:
            Dictionary with fixes from all experts
        """
        enriched_issues = input_data.get('enriched_issues', [])
        source_files = input_data.get('source_files', {})
        
        all_fixes = []
        
        for issue in enriched_issues:
            # Determine which expert to use
            expert = self._select_expert(issue)
            
            # Get file content
            file_path = issue.get('file')
            file_content = source_files.get(file_path, '')
            
            # Delegate to expert
            print(f"  Delegating to {expert.name}: {issue.get('description', 'Unknown issue')[:50]}...")
            
            fix_result = expert.execute({
                'issue': issue,
                'file_content': file_content
            })
            
            all_fixes.append({
                'issue': issue,
                'fix': fix_result,
                'expert': expert.name,
                'file': file_path
            })
        
        return {
            'fixes': all_fixes,
            'total_fixes': len(all_fixes),
            'successful_fixes': sum(1 for f in all_fixes if f['fix'].get('success', False))
        }
    
    def _select_expert(self, issue: Dict) -> BaseAgent:
        """Select the appropriate expert for an issue."""
        
        file_path = issue.get('file', '').lower()
        description = issue.get('description', '').lower()
        category = issue.get('category', '').lower()
        
        # File extension based selection
        if file_path.endswith('.css'):
            return self.css_expert
        elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            return self.js_expert
        
        # Content-based selection
        css_keywords = ['color', 'contrast', 'focus', 'outline', 'font', 'size', 'visible', 'display']
        js_keywords = ['click', 'event', 'keyboard', 'focus', 'dynamic', 'interactive', 'listener']
        html_keywords = ['alt', 'aria', 'label', 'heading', 'semantic', 'role', 'landmark', 'form']
        
        # Count keyword matches
        css_score = sum(1 for kw in css_keywords if kw in description)
        js_score = sum(1 for kw in js_keywords if kw in description)
        html_score = sum(1 for kw in html_keywords if kw in description)
        
        # Select based on highest score
        if css_score >= js_score and css_score >= html_score and css_score > 0:
            return self.css_expert
        elif js_score >= html_score and js_score > 0:
            return self.js_expert
        else:
            return self.html_expert
    
    def generate_delegation_report(self, fixes: List[Dict]) -> str:
        """Generate a report of how tasks were delegated."""
        
        report = "TASK DELEGATION REPORT\n"
        report += "=" * 60 + "\n\n"
        
        # Group by expert
        by_expert = {}
        for fix in fixes:
            expert = fix.get('expert', 'Unknown')
            by_expert[expert] = by_expert.get(expert, 0) + 1
        
        report += "Tasks by Expert:\n"
        for expert, count in sorted(by_expert.items()):
            report += f"  {expert}: {count} tasks\n"
        
        report += "\n"
        
        # Success rate
        successful = sum(1 for f in fixes if f['fix'].get('success', False))
        total = len(fixes)
        success_rate = (successful / total * 100) if total > 0 else 0
        
        report += f"Success Rate: {successful}/{total} ({success_rate:.1f}%)\n"
        
        return report
