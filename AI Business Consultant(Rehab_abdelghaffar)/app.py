import streamlit as st
from main import crew, save_pdf_report

# Add CSS for Custom Font Styling
st.markdown("""
<style>
.label {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Business Consultant")

# Input fields with styled labels
st.markdown('<div class="label">💼 Enter The Required Business Search Area</div>', unsafe_allow_html=True)
business = st.text_input("", key="business_input")

st.markdown('<div class="label">📊 Enter The Stakeholder Team</div>', unsafe_allow_html=True)
stakeholder = st.text_input("", key="stakeholder_input")

st.markdown('<div class="label">🌍 Enter the Country for the Business</div>', unsafe_allow_html=True)
country = st.text_input("", key="country_input")

# logo
image_url = "https://cdn-icons-png.flaticon.com/512/1998/1998614.png"
st.sidebar.image(image_url, caption="")
st.sidebar.write(" This AI Business Consultant is built using AI Multi-Agent system. It can give you business insights, statistical analysis and up-to-date information about any business topic. This AI Multi-Agent Business Consultant delivers knowledge on demand and for FREE!")

# Run Button
if st.button("Run"):
    if not business or not country or not stakeholder:
        st.error("Please fill all the fields.")
    else:
        with st.spinner('Processing...'):
            try:
                result = crew.kickoff(inputs={"topic": business, "stakeholder": stakeholder, "country": country})
                st.success("Execution Complete!")
                st.write(result.raw)

                # Save result.raw as PDF in output folder
                pdf_path = save_pdf_report(result.raw)
                st.info(f"PDF report saved at: `{pdf_path}`")

            except Exception as e:
                st.error(f"An error occurred: {e}")
