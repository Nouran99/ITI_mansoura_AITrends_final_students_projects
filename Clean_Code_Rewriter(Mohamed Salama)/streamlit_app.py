import streamlit as st
import re
from crew_make import run_code_improvement_workflow  # your CrewAI call

def parse_crewai_output(output):
    """
    Robust parser to handle all possible CrewAI output scenarios.
    Returns tuple: (refactored_code, lessons)
    """
    output = output.strip()
    
    # Initialize variables
    refactored_code = ""
    lessons = ""
    
    # Scenario 1: Try to find code blocks with triple backticks first
    code_pattern = r'```(?:javascript|python|cpp|c\+\+|java|html|css)?\s*\n(.*?)\n```'
    code_matches = re.findall(code_pattern, output, re.DOTALL | re.IGNORECASE)
    
    if code_matches:
        # Take the largest code block (likely the main refactored code)
        refactored_code = max(code_matches, key=len).strip()
    
    # Scenario 2: Look for specific headers and sections
    sections = {
        'lessons': [],
        'code': []
    }
    
    # Define possible section headers for lessons
    lesson_headers = [
        r'\*\*CLEAN CODE LESSONS:\*\*',
        r'CLEAN CODE LESSONS:',
        r'\*\*Clean Code Lessons:\*\*',
        r'Clean Code Lessons:',
        r'\*\*LESSONS:\*\*',
        r'LESSONS:'
    ]
    
    # Define possible section headers for code
    code_headers = [
        r'\*\*Refactored Code:\*\*',
        r'Refactored Code:',
        r'\*\*REFACTORED CODE:\*\*',
        r'REFACTORED CODE:',
        r'\*\*Code:\*\*',
        r'Code:'
    ]
    
    # Try to split by lesson headers
    for pattern in lesson_headers:
        matches = re.split(pattern, output, flags=re.IGNORECASE)
        if len(matches) > 1:
            # Found lessons section
            lessons_section = matches[1]
            
            # Remove any code section that might be mixed in
            for code_pattern in code_headers:
                parts = re.split(code_pattern, lessons_section, flags=re.IGNORECASE)
                if len(parts) > 1:
                    lessons_section = parts[0]
                    if not refactored_code and len(parts) > 1:
                        potential_code = parts[1].strip()
                        # Clean up the code section
                        potential_code = re.sub(r'```[a-zA-Z]*\n?', '', potential_code)
                        potential_code = re.sub(r'\n```', '', potential_code)
                        if potential_code:
                            sections['code'].append(potential_code)
            
            sections['lessons'].append(lessons_section.strip())
            break
    
    # Try to split by code headers if we haven't found code yet
    if not refactored_code:
        for pattern in code_headers:
            matches = re.split(pattern, output, flags=re.IGNORECASE)
            if len(matches) > 1:
                code_section = matches[1]
                
                # Remove any lessons section that might be mixed in
                for lesson_pattern in lesson_headers:
                    parts = re.split(lesson_pattern, code_section, flags=re.IGNORECASE)
                    if len(parts) > 1:
                        code_section = parts[0]
                        if not lessons:
                            sections['lessons'].append(parts[1].strip())
                
                # Clean up code block markers
                code_section = re.sub(r'```[a-zA-Z]*\n?', '', code_section)
                code_section = re.sub(r'\n```', '', code_section)
                sections['code'].append(code_section.strip())
                break
    
    # Fallback: if still no clear sections, try to separate by common patterns
    if not sections['lessons'] and not sections['code']:
        # Look for numbered lists (likely lessons)
        numbered_pattern = r'(\d+\.\s+\*\*.*?\*\*:.*?)(?=\d+\.\s+\*\*|\*\*Refactored Code\*\*|```|$)'
        numbered_matches = re.findall(numbered_pattern, output, re.DOTALL)
        if numbered_matches:
            sections['lessons'].extend(numbered_matches)
        
        # Look for function definitions or class definitions (likely code)
        code_pattern = r'((?:function\s+\w+|class\s+\w+|def\s+\w+|#include|using namespace).*?)(?=\*\*.*?LESSONS|$)'
        code_matches = re.findall(code_pattern, output, re.DOTALL)
        if code_matches:
            sections['code'].extend(code_matches)
    
    # Final assembly
    if not refactored_code and sections['code']:
        refactored_code = max(sections['code'], key=len).strip()
    
    if not lessons and sections['lessons']:
        lessons = '\n\n'.join(sections['lessons']).strip()
    
    # Last resort: if we still don't have clear separation
    if not refactored_code and not lessons:
        # Split the output in half and make educated guesses
        lines = output.split('\n')
        mid_point = len(lines) // 2
        
        first_half = '\n'.join(lines[:mid_point])
        second_half = '\n'.join(lines[mid_point:])
        
        # Check which half is more likely to be code
        if any(keyword in first_half.lower() for keyword in ['function', 'def ', 'class ', 'var ', 'let ', 'const ']):
            refactored_code = first_half
            lessons = second_half
        else:
            lessons = first_half
            refactored_code = second_half
    
    # Clean up the results
    if refactored_code:
        # Remove any remaining markdown code block markers
        refactored_code = re.sub(r'^```[a-zA-Z]*\n?', '', refactored_code)
        refactored_code = re.sub(r'\n```$', '', refactored_code)
        refactored_code = refactored_code.strip()
    
    if lessons:
        # Clean up lesson headers and formatting
        lessons = re.sub(r'^\*\*.*?LESSONS?\*\*:?\s*\n?', '', lessons, flags=re.IGNORECASE)
        lessons = lessons.strip()
    
    # If we still don't have both sections, provide defaults
    if not refactored_code:
        refactored_code = "// No refactored code found in the output\n" + output
    
    if not lessons:
        lessons = "_No clean code lessons found in the output._"
    
    return refactored_code, lessons

def detect_language(code_content):
    """Detect programming language from code content."""
    code_lower = code_content.lower()
    
    # Language detection patterns
    if any(keyword in code_lower for keyword in ['#include', 'using namespace', 'int main()', 'cout', 'cin']):
        return "cpp"
    elif any(keyword in code_lower for keyword in ['function ', 'var ', 'let ', 'const ', 'console.log']):
        return "javascript"
    elif any(keyword in code_lower for keyword in ['def ', 'import ', 'print(', 'if __name__']):
        return "python"
    elif any(keyword in code_lower for keyword in ['public class', 'public static void', 'system.out']):
        return "java"
    elif any(keyword in code_lower for keyword in ['<html', '<div', '<script']):
        return "html"
    elif any(keyword in code_lower for keyword in ['.class', '#id', 'background-color']):
        return "css"
    else:
        return "text"

st.set_page_config(page_title="Clean Code Refactorer", layout="wide")

st.title("👨‍💻🧹 Clean Code Rewriter")
st.markdown("✨ Enter your code and make it clean and well-organized 🧹")
st.markdown("🧠 Plus, get smart tips to avoid those mistakes next time 😉")


# Initialize session state
if 'refactored_code' not in st.session_state:
    st.session_state.refactored_code = ""
if 'lessons' not in st.session_state:
    st.session_state.lessons = ""
if 'language' not in st.session_state:
    st.session_state.language = "text"
if 'raw_result' not in st.session_state:
    st.session_state.raw_result = ""
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Add language selection
language_options = ["Auto-detect", "Python", "JavaScript", "C++", "Java", "HTML", "CSS", "Other"]
selected_language = st.selectbox("🔤 Select input language (optional):", language_options)

code_input = st.text_area("📝 Paste your code here:", height=300, placeholder="Paste your code here and click 'Refactor Code' to get improvements and lessons...")

if st.button("🚀 Refactor Code"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some code before clicking.")
    else:
        with st.spinner("🔄 Analyzing and refactoring with clean code principles..."):
            try:
                result = run_code_improvement_workflow(code_input)
                
                # Save result for debugging
                with open('result.txt', 'w', encoding='utf-8') as f:
                    f.write(str(result))
                
                # Parse the output
                refactored_code, lessons = parse_crewai_output(str(result))
                
                # Detect language for syntax highlighting
                if selected_language != "Auto-detect":
                    language = selected_language.lower().replace("c++", "cpp")
                else:
                    language = detect_language(refactored_code)
                
                # Store results in session state
                st.session_state.refactored_code = refactored_code
                st.session_state.lessons = lessons
                st.session_state.language = language
                st.session_state.raw_result = str(result)
                st.session_state.show_results = True
                
            except Exception as e:
                st.error(f"❌ An error occurred while processing your request: {str(e)}")
                st.info("💡 Try again or check your code input.")

# Display results if they exist in session state
if st.session_state.show_results:
    # Display results
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("📋 Refactored Code")
        
        st.code(st.session_state.refactored_code, language=st.session_state.language)

    with col2:
        st.subheader("🎓 Clean Code Lessons")
        
        # Display lessons with better formatting
        if st.session_state.lessons and st.session_state.lessons != "_No clean code lessons found in the output._":
            # Split lessons into numbered points if they exist
            lesson_parts = re.split(r'\n(?=\d+\.)', st.session_state.lessons)
            
            for i, lesson in enumerate(lesson_parts):
                if lesson.strip():
                    # Clean up each lesson
                    clean_lesson = lesson.strip()
                    
                    # Make numbered lessons more readable
                    if re.match(r'^\d+\.', clean_lesson):
                        # Extract title and content
                        parts = clean_lesson.split(':', 1)
                        if len(parts) == 2:
                            title = parts[0].strip()
                            content = parts[1].strip()
                            st.markdown(f"**{title}:**")
                            st.markdown(content)
                        else:
                            st.markdown(clean_lesson)
                    else:
                        st.markdown(clean_lesson)
                    
                    if i < len(lesson_parts) - 1:
                        st.markdown("---")
        else:
            st.info("ℹ️ No specific clean code lessons were provided in the output.")
            st.markdown(st.session_state.lessons)

    # Add expandable sections for additional info
    with st.expander("🔍 View Raw Output (for debugging)", expanded=False):
        st.text_area("Full response from CrewAI:", value=st.session_state.raw_result, height=200, key="raw_output")
    
    with st.expander("📊 Analysis Summary", expanded=False):
        st.write(f"**Input Language:** {st.session_state.language}")
        st.write(f"**Code Length:** {len(st.session_state.refactored_code)} characters")
        st.write(f"**Lessons Found:** {'Yes' if st.session_state.lessons and st.session_state.lessons != '_No clean code lessons found in the output._' else 'No'}")
        
    # Add a button to clear results and start over
    if st.button("🔄 Start New Refactor"):
        st.session_state.show_results = False
        st.session_state.refactored_code = ""
        st.session_state.lessons = ""
        st.session_state.language = "text"
        st.session_state.raw_result = ""
        st.rerun()

# Add footer with tips
st.markdown("---")
st.markdown("""
**💡 Tips for better results:**
- Paste complete, functional code snippets
- Include context or comments about what your code does
- The more complex your code, the more detailed lessons you'll receive
""")