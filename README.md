# ♿ Accessibility Agent System

A sophisticated multi-agent AI system that automatically detects, analyzes, and fixes web accessibility issues using LangChain, LangGraph, and Groq LLMs.

## 🎯 Features

- **Automated Accessibility Auditing**: Scans HTML, CSS, and JavaScript for WCAG 2.1 violations
- **Multi-Agent Architecture**: Specialized agents for different aspects of accessibility
- **Domain Expertise**: Separate experts for HTML, CSS, and JavaScript fixes
- **Quality Control**: Critic agent validates all proposed solutions
- **GitHub Integration**: Automatically creates branches and pull requests
- **Comprehensive Reporting**: Detailed reports on issues, fixes, and critiques
- **Streamlit UI**: User-friendly web interface

## 🏗️ Architecture
! [lang graph](Screenshot from 2026-02-12 18-13-23.png)
### Agent Workflow (LangGraph)

```
┌─────────────────┐
│  Clone Repo     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyze Access. │  ← AccessibilityAnalyzer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Locate Issues   │  ← IssueLocator
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Delegate Fixes  │  ← ManagerAgent
└────────┬────────┘     │
   │        ▲        ├─→ HTMLAccessibilityExpert
   │        │        ├─→ CSSAccessibilityExpert
   │        │        └─→ JavaScriptAccessibilityExpert
   ▼        │
┌─────────────────┐
│ Critique Solns  │  ← CriticAgent
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Apply & Push    │  ← GitHubAgent
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Report │
└─────────────────┘
```

### Agents

1. **AccessibilityAnalyzer**
   - Scans source code for WCAG violations
   - Categorizes by severity (Critical, High, Medium, Low)
   - Identifies affected WCAG criteria

2. **IssueLocator**
   - Maps issues to exact code locations
   - Extracts problematic code snippets
   - Suggests specific fix approaches

3. **ManagerAgent**
   - Delegates tasks to appropriate domain experts
   - Coordinates workflow between agents
   - Tracks progress and results

4. **Domain Experts**
   - **HTMLAccessibilityExpert**: Semantic HTML, ARIA, landmarks
   - **CSSAccessibilityExpert**: Color contrast, focus indicators, responsive design
   - **JavaScriptAccessibilityExpert**: Keyboard navigation, dynamic content, focus management

5. **CriticAgent**
   - Reviews proposed fixes
   - Validates WCAG compliance
   - Approves or rejects changes
   - Provides constructive feedback

6. **GitHubAgent**
   - Creates feature branches
   - Commits changes with detailed messages
   - Creates pull requests
   - Manages version control

## 🚀 Installation

### Prerequisites

- Python 3.12+
- Docker (optional)
- Groq API key
- GitHub personal access token (for pushing changes)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd accessibility-agent-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```


## 🔑 Configuration

### Required API Keys

1. **Groq API Key**
   - Sign up at https://console.groq.com
   - Create an API key
   - Add to `.env` file or enter in Streamlit UI

2. **GitHub Token** (Optional, for pushing changes)
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate token with `repo` scope
   - Add to `.env` file or enter in Streamlit UI

### Environment Variables

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here

# LLM Configuration
MODEL_NAME=mixtral-8x7b-32768
TEMPERATURE=0.1
MAX_TOKENS=4096

# GitHub Configuration
GITHUB_USERNAME=your_github_username
DEFAULT_BRANCH=main
```

## 📖 Usage

### Web Interface (Streamlit)

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API keys** in the sidebar

3. **Enter repository details**
   - GitHub repository URL
   - Repository name (format: `username/repo`)

4. **Run analysis**
   - Click "Start Analysis"
   - Monitor progress in real-time
   - Review results and reports

5. **Download reports**
   - Accessibility issues report
   - Fix implementation report
   - Critique report

### Programmatic Usage

```python
from workflows import AccessibilityWorkflow

# Initialize workflow
workflow = AccessibilityWorkflow()

# Run analysis
result = workflow.run(
    repo_url="https://github.com/username/repository",
    repo_name="username/repository"
)

# Access results
issues = result['issues']
fixes = result['fixes']
critiques = result['critiques']
reports = result['reports']
```


### Adding New Agents

1. Create agent class in `agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` method
4. Add to workflow in `workflows/accessibility_workflow.py`


## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Orchestrated with [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Groq](https://groq.com)
- UI with [Streamlit](https://streamlit.io)
- Based on [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation
- Review existing issues

## 🔮 Future Enhancements

- [ ] DeepAgent Integration
- [ ] Support for more file types (Vue, Angular, Svelte)
- [ ] Real-time accessibility testing
- [ ] CI/CD pipeline integration
- [ ] Custom rule definitions
- [ ] Multi-language support
- [ ] Automated testing generation
- [ ] Performance optimization
- [ ] Advanced ARIA pattern detection


## 🎓 Learning Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [A11y Project](https://www.a11yproject.com/)
- [WebAIM](https://webaim.org/)
- [Deque University](https://dequeuniversity.com/)

---

Made with ♿ by the Accessibility Agent System
