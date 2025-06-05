from crewai import Task

class AgileProjectTasks:
    def customer_intake_task(self, agent, project_description):
        return Task(
            description=f"""
            Analyze the following project description and extract:
            1. Core problem the product solves
            2. Target users
            3. Must-have features
            4. Budget and timeline constraints
            5. Platform preferences
            
            Project Description: {project_description}
            
            Provide a structured summary of all key information.
            """,
            agent=agent,
            expected_output="Structured project requirements document"
        )
    
    def extract_requirements_task(self, agent, context):
        return Task(
            description="""
            Based on the customer input, create a structured requirements document with:
            1. Business goals (list)
            2. Functional requirements (features the system must have)
            3. Non-functional requirements (performance, security, scalability needs)
            
            Format as JSON with clear categorization.
            """,
            agent=agent,
            context=context,
            expected_output="JSON formatted requirements specification"
        )
    
    def create_project_plan_task(self, agent, context):
        return Task(
            description="""
            Create a detailed project plan including:
            1. Feature breakdown into modules
            2. Sprint organization (2-week cycles)
            3. Milestones with dates
            4. Dependencies between features
            
            Consider the requirements and constraints provided.
            """,
            agent=agent,
            context=context,
            expected_output="Detailed sprint plan with timeline"
        )
    
    def generate_user_stories_task(self, agent, context):
        return Task(
            description="""
            Convert each feature into user stories following the format:
            "As a [type of user], I want to [action] so that [benefit]"
            
            Include:
            - Clear acceptance criteria for each story
            - Story points estimation
            - Priority level (High/Medium/Low)
            """,
            agent=agent,
            context=context,
            expected_output="Complete user stories with acceptance criteria"
        )

    def recommend_tech_stack_task(self, agent, context):
        return Task(
            description="""
            Based on the project requirements, recommend:
            1. Frontend framework
            2. Backend technology
            3. Database solution
            4. Cloud platform
            5. Additional tools/services needed
            
            Consider scalability, cost, and timeline constraints.
            """,
            agent=agent,
            context=context,
            expected_output="JSON formatted technology recommendations"
        )

    def package_project_plan_task(self, agent, context):
        return Task(
            description="""
        Create a comprehensive, professional project plan document formatted as clean, modern HTML with embedded CSS optimized for PDF conversion.

        ## Structure (Required):
        The document must be organized using semantic HTML5 tags and structured into clearly defined sections with modern design elements.

        ### Required Sections:
        1.  **Executive Summary** - High-level overview with highlight card
        2.  **Project Metrics** - Key metrics displayed in metric cards
        3.  **Project Goals and Objectives** - SMART goals in a structured list
        4.  **Requirements Overview** - Functional and non-functional requirements
        5.  **Sprint Plan and Timeline** - Modern table with hover effects
        6.  **User Stories** - Card-based layout or styled table
        7.  **Technology Stack** - Visual presentation of architecture
        8.  **Team Structure** - Roles table (no personal names)
        9.  **Budget Estimate** - Professional table with totals
        10. **Risk Assessment** - Risk matrix with color coding
        11. **Key Milestones** - Timeline with visual markers
        12. **Next Steps** - Action items with priorities

        ### Optional Sections:
        - Success Metrics Dashboard
        - Deployment Strategy
        - Post-Launch Support Plan
        - Stakeholder Communication Plan

        ## Design Requirements:
        - Modern gradient header with project title
        - Card-based sections with subtle shadows
        - Metric cards for key performance indicators
        - Professional color scheme with blue gradients
        - Large, readable fonts (18px base)
        - NO personal names - use role titles only
        - ehance text and marhins beased on the data and content
        - don't let alot of white space btween secions

        ## Required HTML Template:
        ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Project Plan</title>
            <style>
                /* CSS Variables for consistent theming */
                :root {
                    --primary-color: #1e3a5f;
                    --secondary-color: #4a90e2;
                    --accent-color: #01036d;
                    --text-primary: #2c3e50;
                    --text-secondary: #5a6c7d;
                    --bg-primary: #ffffff;
                    --bg-secondary: #f7f9fc;
                    --bg-accent: #050223;
                    --border-color: #e1e8ed;
                    --shadow-sm: 0 2px 4px rgba(0,0,0,0.06);
                    --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
                    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
                }

                /* Global Reset */
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }

                /* Base Typography */
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 18px;
                    line-height: 1.7;
                    color: var(--text-primary);
                    background: var(--bg-secondary);
                    -webkit-font-smoothing: antialiased;
                }

                /* Page Layout */
                .document {
                    max-width: 1000px;
                    margin: 40px auto;
                    background: var(--bg-primary);
                    box-shadow: var(--shadow-lg);
                    border-radius: 12px;
                    overflow: hidden;
                }

                .document-header {
                    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                    color: white;
                    padding: 60px 60px 40px;
                }

                .document-body {
                    padding: 60px;
                }

                /* Headers */
                h1 {
                    font-size: 42px;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: -1px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                .subtitle {
                    font-size: 20px;
                    opacity: 0.9;
                    font-weight: 300;
                }

                h2 {
                    font-size: 28px;
                    font-weight: 600;
                    color: var(--primary-color);
                    margin: 20px 0 20px 0;
                    position: relative;
                    padding-left: 15px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                h2:before {
                    content: '';
                    position: absolute;
                    left: 0;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 4px;
                    height: 30px;
                    background: var(--accent-color);
                    border-radius: 2px;
                }

                h3 {
                    font-size: 22px;
                    font-weight: 500;
                    color: var(--text-primary);
                    margin: 24px 0 16px 0;
                }

                /* Sections */
                .section {
                    background: #fafcff;
                    border-radius: 10px;
                    padding: 36px;
                    margin-bottom: 32px;
                    border: 1px solid var(--border-color);
                    transition: all 0.3s ease;
                    page-break-inside: avoid;
                }

                .section:hover {
                    transform: translateY(-2px);
                    box-shadow: var(--shadow-md);
                }

                /* Text Styles */
                p {
                    font-size: 18px;
                    color: var(--text-secondary);
                    margin-bottom: 20px;
                }

                strong {
                    color: var(--text-primary);
                    font-weight: 600;
                }

                /* Tables */
                .table-container {
                    overflow-x: auto;
                    margin: 24px 0;
                    border-radius: 10px;
                    box-shadow: var(--shadow-sm);
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    background: var(--bg-primary);
                    font-size: 16px;
                }

                th {
                    background: var(--primary-color);
                    color: white;
                    padding: 18px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 16px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                td {
                    padding: 16px 18px;
                    border-bottom: 1px solid var(--border-color);
                    color: var(--text-secondary);
                }

                tr:last-child td {
                    border-bottom: none;
                }

                tr:hover {
                    background: var(--bg-secondary);
                }

                /* Risk Matrix Colors */
                .risk-high { background-color: #fee; color: #c33; }
                .risk-medium { background-color: #ffeaa7; color: #d68910; }
                .risk-low { background-color: #d1f2eb; color: #27ae60; }

                /* Lists */
                ul, ol {
                    margin: 24px 0;
                    padding-left: 28px;
                }

                li {
                    margin-bottom: 14px;
                    font-size: 18px;
                    color: var(--text-secondary);
                }

                /* Special Elements */
                .highlight-card {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 24px;
                    border-radius: 10px;
                    margin: 24px 0;
                    box-shadow: var(--shadow-md);
                }

                .metric-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 24px 0;
                }

                .metric-card {
                    background: var(--bg-primary);
                    padding: 24px;
                    border-radius: 10px;
                    border: 2px solid var(--border-color);
                    text-align: center;
                    transition: all 0.3s ease;
                }

                .metric-card:hover {
                    border-color: var(--secondary-color);
                    transform: translateY(-2px);
                    box-shadow: var(--shadow-md);
                }

                .metric-value {
                    font-size: 32px;
                    font-weight: 700;
                    color: var(--secondary-color);
                    margin-bottom: 8px;
                }

                .metric-label {
                    font-size: 16px;
                    color: var(--text-secondary);
                }

                /* Timeline */
                .timeline-item {
                    position: relative;
                    padding-left: 40px;
                    margin-bottom: 24px;
                }

                .timeline-item:before {
                    content: '';
                    position: absolute;
                    left: 0;
                    top: 8px;
                    width: 12px;
                    height: 12px;
                    background: var(--secondary-color);
                    border-radius: 50%;
                }

                /* Footer */
                .footer {
                    text-align: center;
                    padding: 40px;
                    color: var(--text-secondary);
                    font-size: 16px;
                    border-top: 2px solid var(--border-color);
                }

                /* Print Styles */
                @media print {
                    @page {
                        margin: 0.75in;
                        size: letter;
                    }
                    
                    body {
                        background: white;
                        font-size: 12pt;
                    }
                    
                    .document {
                        box-shadow: none;
                        margin: 0;
                    }
                    
                    .document-header {
                        background: #f0f0f0 !important;
                        color: black !important;
                        print-color-adjust: exact;
                        -webkit-print-color-adjust: exact;
                    }
                    
                    .section {
                        page-break-inside: avoid;
                        box-shadow: none;
                        transform: none !important;
                    }
                    
                    table {
                        page-break-inside: avoid;
                    }
                    
                    .highlight-card {
                        background: #e0e0e0 !important;
                        color: black !important;
                    }
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .document-body {
                        padding: 30px;
                    }
                    
                    h1 {
                        font-size: 32px;
                    }
                    
                    h2 {
                        font-size: 24px;
                    }
                    
                    .metric-grid {
                        grid-template-columns: 1fr 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="document">
                <div class="document-header">
                    <h1>[Project Title]</h1>
                    <div class="subtitle">[Project Subtitle/Description]</div>
                </div>
                <div class="document-body">
                    <!-- Content sections go here -->
                </div>
            </div>
        </body>
        </html>

        ## Content Requirements:
        - Each section must contain substantial, professional content
        - Use specific dates, metrics, and measurable goals
        - Include realistic budget breakdowns with justifications
        - Risk assessments must include impact, likelihood, and mitigation strategies
        - Tables should have clear headers and well-organized data
        - NO PERSONAL NAMES - use only role titles (e.g., "Project Manager", "Senior Developer", "QA Lead")
        - add tech requriment on cool way 
        

        ## Special Components to Include:
        1. **Metric Cards**: Display key project metrics (timeline, budget, team size, etc.)
        2. **Highlight Cards**: Use for important callouts or critical information
        3. **Timeline Items**: For milestone visualization
        4. **Risk Matrix**: Color-coded table cells based on risk level


        ## Quality Standards:
        - Professional language throughout
        - Consistent formatting and spacing
        - Modern, clean design aesthetic
        - High readability with proper contrast
        - Mobile-responsive layout
        - Print-optimized with proper page breaks 

        ## Example Section Structure:

        <div class="section">
            <h2>Section Title</h2>
            <p>Section introduction or overview text...</p>
            
            <!-- For metrics -->
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">Value</div>
                    <div class="metric-label">Label</div>
                </div>
            </div>
            
            <!-- For tables -->
            <div class="table-container">
                <table>
                    <!-- Table content -->
                </table>
            </div>
            
            <!-- For highlights -->
            <div class="highlight-card">
                Important information or callout
            </div>
        </div>
        ```

        ## Output Requirements:
        - Complete, valid HTML5 document
        - All styles embedded in <style> tag
        - Professional appearance suitable for executive presentation
        - Optimized for both screen viewing and PDF conversion
        - Clean, semantic markup
        - No external dependencies or resources
        - No personal names or identifying information
        - Proper HTML structure with doctype, head, and body
        - All content wrapped in appropriate semantic tags
        - Tables must include thead and tbody elements
        - Images avoided (use CSS styling instead)
        - Font sizes large enough for easy reading (18px base)
        - Consistent use of CSS variables for theming
        - Proper meta tags for character encoding and viewport
        - Document ready for immediate PDF export without modifications

        """,
        agent=agent,
        context=context,
        expected_output="""A complete, professional HTML document containing a comprehensive project plan with:
        - Modern gradient header with project title
        - All required sections properly formatted with the provided CSS classes
        - Metric cards displaying key project indicators
        - Professional tables with hover effects
        - Risk assessments with color-coded cells
        - Timeline visualization for milestones
        - Highlight cards for important information
        - Clean, readable typography with 18px base font
        - Responsive layout that works on all devices
        - Print-optimized styles for PDF conversion
        - No personal names (roles/titles only)
        - No images (use CSS for styling)
        - Proper HTML structure with doctype, head, and body
        - All content wrapped in appropriate semantic tags
        - Tables must include thead and tbody elements
        - Font sizes large enough for easy reading
        - Consistent use of CSS variables for theming
        - Proper meta tags for character encoding and viewport
        - Document ready for immediate PDF export without modifications
        - Header with project title and subtitle
        - Main content area with sections
        - Footer with document metadata and github user :@3lis0 link(https://github.com/3lis0)

        
        The final output should be a single, self-contained HTML file that looks professional 
        both on screen and when converted to PDF, with no external dependencies."""
    )