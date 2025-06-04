import streamlit as st
import yaml
import subprocess
import os
import sys

# File paths
CONFIG_PATH = "config/config.yaml"
OUTPUT_PATH = "data/processed/marketing_analysis.md"

def update_config(company_name, industry):
    # Load existing YAML config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}

    # Update only the company section
    config.setdefault('company', {})
    config['company']['name'] = company_name
    config['company']['industry'] = industry

    # Save updated config
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f)

def run_main_script():
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, str(e)

def load_output():
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r') as f:
            return f.read()
    return None

def main():
    st.set_page_config(page_title="Marketing Strategy Generator", layout="centered")
    st.title("📊 AI Marketing Strategy Generator")

    with st.form("input_form"):
        company_name = st.text_input("Company Name", placeholder="e.g., EcoTech Solutions")
        industry = st.text_input("Industry", placeholder="e.g., Renewable Energy")
        submitted = st.form_submit_button("Generate Strategy")

    if submitted:
        if not company_name or not industry:
            st.error("Please fill in both Company Name and Industry.")
            return

        with st.spinner("Generating strategy..."):
            update_config(company_name, industry)
            success, error = run_main_script()

        if success:
            output = load_output()
            if output:
                st.success("✅ Strategy generated successfully!")
                st.markdown("### 📋 Marketing Report")
                st.markdown("---")
                st.markdown(f"<div style='font-family: monospace'>{output}</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Report",
                    data=output,
                    file_name="marketing_analysis.md",
                    mime="text/markdown"
                )
            else:
                st.error("Output file not found.")
        #else:
        #    st.error(f"❌ Error while running main.py:\n\n```\n{error}\n```")

if __name__ == "__main__":
    main()
