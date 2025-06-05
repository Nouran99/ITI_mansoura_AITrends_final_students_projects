def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Light mode variables (default) - IMPROVED */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --border-color: #e2e8f0;
        --shadow-light: rgba(0,0,0,0.08);
        --shadow-medium: rgba(0,0,0,0.12);
        --shadow-strong: rgba(0,0,0,0.16);
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-hover-shadow: rgba(102, 126, 234, 0.15);
        --success-bg: #f0fff4;
        --success-border: #9ae6b4;
        --success-text: #22543d;
        --error-bg: #fed7d7;
        --error-border: #feb2b2;
        --error-text: #742a2a;
        --info-bg: #ebf8ff;
        --info-border: #90cdf4;
        --info-text: #2a4365;
    }
    
    /* Auto dark mode (system preference) */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #c9d1d9;
            --text-muted: #8b949e;
            --border-color: #30363d;
            --shadow-light: rgba(0,0,0,0.3);
            --shadow-medium: rgba(0,0,0,0.4);
            --shadow-strong: rgba(0,0,0,0.5);
            --card-hover-shadow: rgba(102, 126, 234, 0.3);
            --success-bg: #0d1d17;
            --success-border: #2ea043;
            --success-text: #3fb950;
            --error-bg: #2d1b1b;
            --error-border: #da3633;
            --error-text: #f85149;
            --info-bg: #0c1929;
            --info-border: #1f6feb;
            --info-text: #79c0ff;
        }
    }
    
    /* Manual dark mode override */
    [data-theme="dark"] {
        --bg-primary: #0d1117 !important;
        --bg-secondary: #161b22 !important;
        --bg-card: #21262d !important;
        --text-primary: #f0f6fc !important;
        --text-secondary: #c9d1d9 !important;
        --text-muted: #8b949e !important;
        --border-color: #30363d !important;
        --shadow-light: rgba(0,0,0,0.3) !important;
        --shadow-medium: rgba(0,0,0,0.4) !important;
        --shadow-strong: rgba(0,0,0,0.5) !important;
        --card-hover-shadow: rgba(102, 126, 234, 0.3) !important;
        --success-bg: #0d1d17 !important;
        --success-border: #2ea043 !important;
        --success-text: #3fb950 !important;
        --error-bg: #2d1b1b !important;
        --error-border: #da3633 !important;
        --error-text: #f85149 !important;
        --info-bg: #0c1929 !important;
        --info-border: #1f6feb !important;
        --info-text: #79c0ff !important;
    }
    
    /* Manual light mode override */
    [data-theme="light"] {
        --bg-primary: #ffffff !important;
        --bg-secondary: #f8fafc !important;
        --bg-card: #ffffff !important;
        --text-primary: #1a202c !important;
        --text-secondary: #4a5568 !important;
        --text-muted: #718096 !important;
        --border-color: #e2e8f0 !important;
        --shadow-light: rgba(0,0,0,0.08) !important;
        --shadow-medium: rgba(0,0,0,0.12) !important;
        --shadow-strong: rgba(0,0,0,0.16) !important;
        --card-hover-shadow: rgba(102, 126, 234, 0.15) !important;
        --success-bg: #f0fff4 !important;
        --success-border: #9ae6b4 !important;
        --success-text: #22543d !important;
        --error-bg: #fed7d7 !important;
        --error-border: #feb2b2 !important;
        --error-text: #742a2a !important;
        --info-bg: #ebf8ff !important;
        --info-border: #90cdf4 !important;
        --info-text: #2a4365 !important;
    }
    
    /* Base application styling */
    .main {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    .stApp > div {
        background-color: var(--bg-primary);
    }
    
    /* IMPROVED Domain cards */
    .domain-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid var(--border-color);
        box-shadow: 0 4px 16px var(--shadow-light);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-align: center;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    
    /* Light mode gradient overlay for domain cards */
    .domain-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, var(--card-color)08, var(--card-color)03);
        pointer-events: none;
        border-radius: 14px;
    }
    
    .domain-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px var(--card-hover-shadow);
        border-color: var(--card-color);
    }
    
    .domain-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
        position: relative;
        z-index: 1;
    }
    
    .domain-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
        position: relative;
        z-index: 1;
    }
    
    .domain-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.5;
        position: relative;
        z-index: 1;
    }
    
    /* Chat container */
    .chat-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .chat-container h3 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .chat-container p {
        color: var(--text-secondary);
    }
    
    /* User info form */
    .user-info-form {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 20px var(--shadow-light);
        border: 1px solid var(--border-color);
        border-left: 4px solid #667eea;
    }
    
    .user-info-form h3 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .user-info-form p {
        color: var(--text-secondary);
    }
    
    /* IMPROVED Stats cards */
    .stats-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px var(--shadow-light);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px var(--shadow-medium);
    }
    
    .stats-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
        display: block;
        margin-bottom: 0.25rem;
    }
    
    .stats-label {
        color: var(--text-muted);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* IMPROVED Header */
    .header-container {
        background: var(--gradient-primary);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .header-container h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-container p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* IMPROVED Buttons */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* IMPROVED Messages */
    .success-message, .stSuccess {
        background: var(--success-bg);
        border: 1px solid var(--success-border);
        color: var(--success-text);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message, .stError {
        background: var(--error-bg);
        border: 1px solid var(--error-border);
        color: var(--error-text);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .stInfo {
        background: var(--info-bg);
        border: 1px solid var(--info-border);
        color: var(--info-text);
        border-radius: 12px;
        font-weight: 500;
    }
    
    /* IMPROVED Streamlit component overrides */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stTextInput > div > div > input {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* IMPROVED Expanders */
    .stExpander {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .stExpander > div > div > div > div {
        background-color: var(--bg-card);
        color: var(--text-primary);
        padding: 1rem;
    }
    
    .stExpander summary {
        color: var(--text-primary);
        font-weight: 500;
        padding: 1rem;
        background-color: var(--bg-secondary);
        border-bottom: 1px solid var(--border-color);
    }
    
    /* IMPROVED Code blocks */
    code {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.9rem;
    }
    
    pre code {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        display: block;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background-color: var(--border-color);
        border-radius: 10px;
    }
    
    .stProgress > div > div > div {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.05));
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    .stChatMessage[data-testid="assistant"] {
        background-color: var(--bg-secondary);
        border-color: var(--border-color);
    }
    
    /* Form elements */
    .stForm {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px var(--shadow-light);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-secondary);
        border-radius: 12px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        background-color: transparent;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--text-primary);
        background-color: var(--bg-card);
        box-shadow: 0 2px 4px var(--shadow-light);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    
    /* Smooth transitions for theme switching */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fef3cd;
        border: 1px solid #fad02c;
        color: #8a6914;
        border-radius: 12px;
        font-weight: 500;
    }
    
    [data-theme="dark"] .stWarning {
        background-color: #2d2a17;
        border: 1px solid #5a4a2d;
        color: #ffd93d;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    .css-17eq0hr {
        background-color: var(--bg-primary);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: var(--bg-card);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    </style>
    """