from typing import TypedDict, Annotated, Sequence
from typing import Dict, Any, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import operator
from agents import (
    AccessibilityAnalyzer,
    IssueLocator,
    ManagerAgent,
    CriticAgent,
    GitHubAgent
)
from utils import GitHubHandler, ReportGenerator


class AgentState(TypedDict):
    """State object for the agent workflow."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    repo_url: str
    repo_name: str
    repo_path: str
    source_files: dict
    issues: list
    enriched_issues: list
    fixes: list
    critiques: list
    github_result: dict
    reports: dict
    current_step: str
    errors: list



github_handler = GitHubHandler()
report_generator = ReportGenerator()
analyzer = AccessibilityAnalyzer()
locator = IssueLocator()
manager = ManagerAgent()
critic = CriticAgent()
github_agent = GitHubAgent()




def clone_repo( state: AgentState) -> AgentState:
    """Step 1: Clone the GitHub repository."""
    print("\n" + "="*60)
    print("STEP 1: Cloning Repository")
    print("="*60)
    
    try:
        repo_url = state['repo_url']
        print(f"Cloning: {repo_url}")
        
        repo_path = github_handler.clone_repository(repo_url)
        source_files = github_handler.get_source_files(repo_path)
        
        print(f"✓ Cloned successfully")
        print(f"✓ Found {len(source_files)} source files")
        
        state['repo_path'] = repo_path
        state['source_files'] = source_files
        state['current_step'] = 'clone_repo'
        
    except Exception as e:
        print(f"✗ Error cloning repository: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Clone error: {str(e)}")
    
    return state

def analyze_accessibility( state: AgentState) -> AgentState:
    """Step 2: Analyze code for accessibility issues."""
    print("\n" + "="*60)
    print("STEP 2: Analyzing Accessibility")
    print("="*60)
    
    try:
        result = analyzer.execute({
            'source_files': state['source_files']
        })
        
        issues = result['issues']
        print(f"✓ Found {len(issues)} accessibility issues")
        print(f"  Files analyzed: {result['files_analyzed']}")
        
        state['issues'] = issues
        state['current_step'] = 'analyze_accessibility'
        
    except Exception as e:
        print(f"✗ Error analyzing accessibility: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Analysis error: {str(e)}")
        state['issues'] = []
    
    return state

def locate_issues( state: AgentState) -> AgentState:
    """Step 3: Locate issues in source code."""
    print("\n" + "="*60)
    print("STEP 3: Locating Issues in Code")
    print("="*60)
    
    try:
        result = locator.execute({
            'issues': state['issues'],
            'source_files': state['source_files']
        })
        
        enriched_issues = result['enriched_issues']
        print(f"✓ Located {len(enriched_issues)} issues in code")
        
        state['enriched_issues'] = enriched_issues
        state['current_step'] = 'locate_issues'
        
    except Exception as e:
        print(f"✗ Error locating issues: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Location error: {str(e)}")
        state['enriched_issues'] = state.get('issues', [])
    
    return state

def delegate_fixes( state: AgentState) -> AgentState:
    """Step 4: Delegate fixes to domain experts."""
    print("\n" + "="*60)
    print("STEP 4: Delegating Fixes to Domain Experts")
    print("="*60)
    
    try:
        result = manager.execute({
            'enriched_issues': state['enriched_issues'],
            'source_files': state['source_files']
        })
        
        fixes = result['fixes']
        print(f"✓ Generated {result['total_fixes']} fixes")
        print(f"  Successful: {result['successful_fixes']}")
        
        state['fixes'] = fixes
        state['current_step'] = 'delegate_fixes'
        
    except Exception as e:
        print(f"✗ Error delegating fixes: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Delegation error: {str(e)}")
        state['fixes'] = []
    
    return state

def critique_solutions( state: AgentState) -> AgentState:
    """Step 5: Critique the proposed solutions."""
    print("\n" + "="*60)
    print("STEP 5: Critiquing Solutions")
    print("="*60)
    
    try:
        result = critic.execute({
            'fixes': state['fixes']
        })
        
        critiques = result['critiques']
        print(f"✓ Reviewed {result['total_reviewed']} solutions")
        print(f"  Approved: {result['approved']}")
        print(f"  Rejected: {result['rejected']}")
        print(f"  Approval Rate: {result['approval_rate']:.1f}%")
        
        state['critiques'] = critiques
        state['current_step'] = 'critique_solutions'
        
    except Exception as e:
        print(f"✗ Error critiquing solutions: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Critique error: {str(e)}")
        state['critiques'] = []
    
    return state

def apply_and_push( state: AgentState) -> AgentState:
    """Step 6: Apply fixes and push to GitHub."""
    print("\n" + "="*60)
    print("STEP 6: Applying Fixes and Pushing to GitHub")
    print("="*60)
    
    try:
        result = github_agent.execute({
            'critiques': state['critiques'],
            'repo_path': state['repo_path'],
            'repo_name': state['repo_name'],
            'branch_name': 'accessibility-fixes',
            'source_files': state['source_files']
        })
        
        if result['success']:
            print(f"✓ Successfully pushed changes")
            print(f"  Files modified: {result['files_modified']}")
            print(f"  Branch: {result.get('branch_name', 'N/A')}")
            if result.get('pull_request_url'):
                print(f"  PR: {result['pull_request_url']}")
        else:
            print(f"✗ Failed to push changes: {result.get('error', 'Unknown error')}")
        
        state['github_result'] = result
        state['current_step'] = 'apply_and_push'
        
    except Exception as e:
        print(f"✗ Error pushing to GitHub: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"GitHub error: {str(e)}")
        state['github_result'] = {'success': False, 'error': str(e)}
    
    return state

def generate_reports( state: AgentState) -> AgentState:
    """Step 7: Generate final reports."""
    print("\n" + "="*60)
    print("STEP 7: Generating Reports")
    print("="*60)
    
    try:
        # Generate accessibility report
        accessibility_report = report_generator.generate_accessibility_report(
            state['issues'],
            state['repo_name']
        )
        
        # Generate fix report
        fixes_info = {}
        for critique in state.get('critiques', []):
            if critique.get('approved'):
                file_path = critique.get('file')
                if file_path not in fixes_info:
                    fixes_info[file_path] = {
                        'issues_fixed': [],
                        'changes': []
                    }
                fixes_info[file_path]['issues_fixed'].append(critique.get('issue_description'))
                
                original_fix = critique.get('original_fix', {})
                if original_fix.get('explanation'):
                    fixes_info[file_path]['changes'].append(original_fix['explanation'])
        
        fix_report = report_generator.generate_fix_report(
            fixes_info,
            state['repo_name']
        )
        
        # Generate critique report
        critique_report = report_generator.generate_critique_report(
            state.get('critiques', []),
            state['repo_name']
        )
        
        print(f"✓ Generated reports:")
        print(f"  - {accessibility_report}")
        print(f"  - {fix_report}")
        print(f"  - {critique_report}")
        
        state['reports'] = {
            'accessibility': accessibility_report,
            'fixes': fix_report,
            'critiques': critique_report
        }
        state['current_step'] = 'generate_reports'
        
    except Exception as e:
        print(f"✗ Error generating reports: {str(e)}")
        state['errors'] = state.get('errors', [])
        state['errors'].append(f"Report error: {str(e)}")
    
    return state



def decide_if_fixed(state: Dict[str, Any]):
    # This checks the key we just added to the CriticAgent's return dict
    if state.get("is_satisfactory"):
        return "proceed"
    return "retry"
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("clone_repo", clone_repo)
workflow.add_node("analyze_accessibility", analyze_accessibility)
workflow.add_node("locate_issues", locate_issues)
workflow.add_node("delegate_fixes", delegate_fixes)
workflow.add_node("critique_solutions", critique_solutions)
workflow.add_node("apply_and_push", apply_and_push)
workflow.add_node("generate_reports", generate_reports)

# Define edges (workflow)
workflow.add_edge("clone_repo", "analyze_accessibility")
workflow.add_edge("analyze_accessibility", "locate_issues")
workflow.add_edge("locate_issues", "delegate_fixes")
workflow.add_edge("delegate_fixes", "critique_solutions")
# workflow.add_edge("critique_solutions", "apply_and_push") # use if hitting rate limits
workflow.add_conditional_edges(
    "critique_solutions",
    decide_if_fixed,
    {
        "retry": "delegate_fixes",  # The loop back
        "proceed": "apply_and_push" # The forward path
    }
)
workflow.add_edge("apply_and_push", "generate_reports")
workflow.add_edge("generate_reports", END)

# Set entry point
workflow.set_entry_point("clone_repo")


print("\n" + "="*60)
print("STARTING ACCESSIBILITY WORKFLOW")
print("="*60)



final_state = workflow.compile()

print("\n" + "="*60)
print("WORKFLOW COMPLETE")
print("="*60)



# initial_state = {
#     'messages': [],
#     'repo_url': https://github.com/ManojKesani/portfolio.git,
#     'repo_name': ManojKesani/portfolio,
#     'repo_path': '',
#     'source_files': {},
#     'issues': [],
#     'enriched_issues': [],
#     'fixes': [],
#     'critiques': [],
#     'github_result': {},
#     'reports': {},
#     'current_step': '',
#     'errors': []
    # }