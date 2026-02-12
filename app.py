import streamlit as st
import os
from workflows import AccessibilityWorkflow
import config
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Accessibility Agent System",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .step-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .error-box {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">♿ Accessibility Agent System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated Web Accessibility Testing & Fixing</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key configuration
        st.subheader("API Keys")
        groq_key = st.text_input(
            "Groq API Key",
            value=config.GROQ_API_KEY or "",
            type="password",
            help="Your Groq API key for LLM access"
        )
        
        github_token = st.text_input(
            "GitHub Token",
            value=config.GITHUB_TOKEN or "",
            type="password",
            help="Your GitHub personal access token"
        )
        
        # Update config
        if groq_key:
            os.environ['GROQ_API_KEY'] = groq_key
            config.GROQ_API_KEY = groq_key
        
        if github_token:
            os.environ['GITHUB_TOKEN'] = github_token
            config.GITHUB_TOKEN = github_token
        
        st.divider()
        
        # Model configuration
        st.subheader("Model Settings")
        model_name = st.selectbox(
            "LLM Model",
            ["openai/gpt-oss-20b", "moonshotai/kimi-k2-instruct", "llama-3.1-8b-instant"],
            index=0
        )
        config.MODEL_NAME = model_name
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1
        )
        config.TEMPERATURE = temperature
        
        st.divider()
        
        # About
        st.subheader("About")
        st.info("""
        This system uses multiple AI agents to:
        1. Analyze code for accessibility issues
        2. Locate specific problems
        3. Generate fixes via domain experts
        4. Critique and validate solutions
        5. Push fixes to GitHub
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🚀 Run Analysis", "📊 Results", "📚 Documentation"])
    
    with tab1:
        st.header("Repository Analysis")
        
        # Input form
        with st.form("repo_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                repo_url = st.text_input(
                    "GitHub Repository URL",
                    placeholder="https://github.com/username/repository",
                    help="Full URL to the GitHub repository"
                )
            
            with col2:
                repo_name = st.text_input(
                    "Repository Name",
                    placeholder="username/repository",
                    help="Repository in format: username/repository"
                )
            
            submit_button = st.form_submit_button("🔍 Start Analysis", use_container_width=True)
        
        # Run workflow
        if submit_button:
            if not repo_url or not repo_name:
                st.error("❌ Please provide both repository URL and name")
            elif not config.GROQ_API_KEY:
                st.error("❌ Please provide Groq API key in the sidebar")
            else:
                run_workflow(repo_url, repo_name)
    
    with tab2:
        st.header("Analysis Results")
        
        if 'workflow_results' in st.session_state:
            display_results(st.session_state.workflow_results)
        else:
            st.info("👆 Run an analysis to see results here")
    
    with tab3:
        st.header("Documentation")
        display_documentation()

def run_workflow(repo_url: str, repo_name: str):
    """Run the accessibility workflow."""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize workflow
        status_text.text("Initializing workflow...")
        progress_bar.progress(10)
        
        workflow = AccessibilityWorkflow()
        
        # Create container for live updates
        live_output = st.empty()
        
        with st.spinner("Running accessibility analysis..."):
            # Run workflow
            status_text.text("Running analysis...")
            progress_bar.progress(20)
            
            result = workflow.run(repo_url, repo_name)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
        
        # Store results
        st.session_state.workflow_results = result
        
        # Display summary
        st.success("✅ Workflow completed successfully!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Issues Found", len(result.get('issues', [])))
        
        with col2:
            st.metric("Fixes Generated", len(result.get('fixes', [])))
        
        with col3:
            approved = sum(1 for c in result.get('critiques', []) if c.get('approved', False))
            st.metric("Approved Fixes", approved)
        
        with col4:
            files_modified = result.get('github_result', {}).get('files_modified', 0)
            st.metric("Files Modified", files_modified)
        
        # Show reports
        if result.get('reports'):
            st.subheader("📄 Generated Reports")
            
            for report_type, report_path in result['reports'].items():
                if os.path.exists(report_path):
                    with open(report_path, 'r') as f:
                        report_content = f.read()
                    
                    with st.expander(f"📋 {report_type.title()} Report"):
                        st.text(report_content)
                        st.download_button(
                            f"Download {report_type} Report",
                            report_content,
                            file_name=os.path.basename(report_path),
                            mime="text/plain"
                        )
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        progress_bar.progress(0)
        status_text.text("Error occurred")

def display_results(results: dict):
    """Display workflow results."""
    
    # Overview
    st.subheader("📊 Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="step-box success-box">', unsafe_allow_html=True)
        st.markdown(f"**Repository:** {results.get('repo_name', 'N/A')}")
        st.markdown(f"**Files Analyzed:** {len(results.get('source_files', {}))}")
        st.markdown(f"**Current Step:** {results.get('current_step', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        github_result = results.get('github_result', {})
        if github_result.get('success'):
            st.markdown('<div class="step-box success-box">', unsafe_allow_html=True)
            st.markdown("**GitHub Status:** ✅ Success")
            if github_result.get('pull_request_url'):
                st.markdown(f"**PR:** [{github_result['pull_request_url']}]({github_result['pull_request_url']})")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="step-box warning-box">', unsafe_allow_html=True)
            st.markdown("**GitHub Status:** ⚠️ Not pushed")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Issues
    st.subheader("🔍 Accessibility Issues")
    
    issues = results.get('issues', [])
    if issues:
        # Group by severity
        by_severity = {}
        for issue in issues:
            severity = issue.get('severity', 'Unknown')
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(issue)
        
        # Display by severity
        for severity in ['Critical', 'High', 'Medium', 'Low']:
            if severity in by_severity:
                with st.expander(f"🔴 {severity} ({len(by_severity[severity])} issues)"):
                    for issue in by_severity[severity]:
                        st.markdown(f"""
                        **File:** `{issue.get('file', 'Unknown')}`  
                        **Line:** {issue.get('line', 'N/A')}  
                        **WCAG:** {issue.get('wcag', 'N/A')}  
                        **Description:** {issue.get('description', 'No description')}  
                        **Recommendation:** {issue.get('recommendation', 'No recommendation')}
                        """)
                        st.divider()
    else:
        st.info("No accessibility issues found!")
    
    # Fixes
    st.subheader("🔧 Applied Fixes")
    
    critiques = results.get('critiques', [])
    approved = [c for c in critiques if c.get('approved', False)]
    
    if approved:
        for critique in approved:
            with st.expander(f"✅ {critique.get('file', 'Unknown file')}"):
                st.markdown(f"**Issue:** {critique.get('issue_description', 'N/A')}")
                st.markdown(f"**Rating:** {critique.get('rating', 'N/A')}/10")
                
                if critique.get('strengths'):
                    st.markdown("**Strengths:**")
                    for strength in critique['strengths']:
                        st.markdown(f"- {strength}")
                
                if critique.get('suggestions'):
                    st.markdown("**Suggestions:**")
                    for suggestion in critique['suggestions']:
                        st.markdown(f"- {suggestion}")
    else:
        st.info("No fixes were approved")
    
    # Errors
    if results.get('errors'):
        st.subheader("⚠️ Errors")
        for error in results['errors']:
            st.error(error)

def display_documentation():
    """Display documentation."""
    
    st.markdown("""
    ## 🎯 System Overview
    
    The Accessibility Agent System is a multi-agent AI system that automatically:
    
    1. **Analyzes** website source code for WCAG 2.1 violations
    2. **Locates** specific code that needs fixing
    3. **Generates** fixes through specialized domain experts
    4. **Critiques** proposed solutions for quality
    5. **Applies** approved fixes and pushes to GitHub
    
    ## 🤖 Agents
    
    ### AccessibilityAnalyzer
    - Scans HTML, CSS, and JavaScript files
    - Identifies WCAG violations
    - Categorizes issues by severity
    
    ### IssueLocator
    - Maps issues to exact code locations
    - Extracts problematic code snippets
    - Suggests fix approaches
    
    ### ManagerAgent
    - Delegates tasks to domain experts
    - Coordinates workflow
    - Tracks progress
    
    ### Domain Experts
    - **HTMLAccessibilityExpert**: Fixes HTML/ARIA issues
    - **CSSAccessibilityExpert**: Fixes styling issues
    - **JavaScriptAccessibilityExpert**: Fixes interactive issues
    
    ### CriticAgent
    - Reviews proposed fixes
    - Validates solutions
    - Approves or rejects changes
    
    ### GitHubAgent
    - Creates branches
    - Commits changes
    - Creates pull requests
    
    ## 📋 WCAG Guidelines Covered
    
    - **Perceivable**: Alt text, color contrast, captions
    - **Operable**: Keyboard navigation, focus management
    - **Understandable**: Clear labels, error messages
    - **Robust**: Semantic HTML, ARIA usage
    
    ## 🚀 Getting Started
    
    1. Enter your Groq API key in the sidebar
    2. (Optional) Enter GitHub token for push access
    3. Provide repository URL and name
    4. Click "Start Analysis"
    5. Review results and reports
    
    ## 📊 Reports Generated
    
    - **Accessibility Report**: All issues found
    - **Fix Report**: Changes made to each file
    - **Critique Report**: Review of solutions
    
    ## 🔧 Configuration
    
    - **Model**: Choose the LLM model
    - **Temperature**: Control creativity (lower = more deterministic)
    
    ## ⚠️ Requirements
    
    - Groq API key (required)
    - GitHub token (optional, for pushing changes)
    - Public GitHub repository URL
    """)

if __name__ == "__main__":
    main()
