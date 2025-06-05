import os
from crewai import Agent, Task, Crew
from langchain_cohere import ChatCohere
from fpdf import FPDF



#=================
# LLM object and API Key
#=================
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")
llm = ChatCohere()


#=================
# Crew Agents
#=================

planner = Agent(
    role="Business Consultant",
    goal="Plan engaging and factually accurate content about the : {topic}",
    backstory="You're working on providing Insights about : {topic} "
              "in the country: {country} "
              "to your stakeholder who is : {stakeholder}."
              "You collect information that help them take decisions "
              "Your work is the basis for "
              "the Business Writer to deliver good insights.",
    allow_delegation=False,
	verbose=True,
    llm = llm
)


writer = Agent(
    role="Business Writer",
    goal="Write insightful and factually accurate "
         "insights about the topic: {topic}",
    backstory="You're writing a Business Insights document "
              "about the topic: {topic}. "
              "in the country: {country}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "and also the data analyst who will provide you with necessary analysis about the : {topic} "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provided by the Business Consultant."
              "design your document in a professional way to be presented to : {stakeholder}."
              ,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

analyst = Agent(
    role="Data Analyst",
    goal="Perform Comprehensive Statistical Analysis on the topic: {topic} ",
    backstory="You're using your strong analytical skills to provide a comprehensive statistical analysis with numbers "
              "about the topic: {topic}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide comprehensive statistical analysis with numbers to the Business Writer "
              "and back them up with information "
              "provided by the Business Consultant.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

#=================
# Crew Tasks
#=================

# Task Definitions
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on the {topic}in {country}.\n"
        "2. Place your business insights.\n"
        "3. Also give some suggestions and things to consider when \n "
            "dealing with International operators.\n"
        "5. Limit the document to only 500 words"
    ),
    expected_output="A comprehensive Business Consultancy document "
        "with an outline, and detailed insights, analysis and suggestions about {topic} in {country}.",
    agent=planner,
    # tools = [tool]

)



write = Task(
    description=(
        "1. Use the business consultant's plan to craft a compelling "
            "document about {topic}in {country}.\n"
		    "2. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "3. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
         "3. Limit the document to only 200 words "
         "4. Use impressive images and charts to reinforce your insights "
    ),
    expected_output="A well-written Document "
        "providing insights for {stakeholder} ",
    agent=writer
)


analyse = Task(
    description=(
        "1. Use the business consultant's plan to do "
            "the needed statistical analysis with numbers on {topic}.\n"
             "considering the country: {country}.\n"
		"2. to be presented to {stakeholder} "
            "in a document which will be deisgned by the Business Writer.\n"
        "3. You'll collaborate with your team of Business Consultant and Business writer "
            "to align on the best analysis to be provided about {topic}.\n"
        "4. Collaborate with your team to align on the best analysis about {topic} and {country}."    
 ),
    expected_output="A clear comprehensive data analysis "
        "providing insights and statistics with numbers to the Business Writer ",
    agent=analyst
)

#=================
# Execution
#=================

crew = Crew(
    agents=[planner, analyst, writer],
    tasks=[plan, analyse, write],
    verbose=True,
)

def save_pdf_report(text, filename="business_insights.pdf", output_dir="output"):
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.add_page()
            self.set_auto_page_break(auto=True, margin=15)
            self.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf', uni=True)
            self.set_font("DejaVu", size=12)

        def add_content(self, content):
            self.multi_cell(0, 10, content)

    pdf = PDF()
    pdf.add_content(text)

    os.makedirs(output_dir, exist_ok=True)
    pdf_file_path = os.path.join(output_dir, filename)
    pdf.output(pdf_file_path)
    return pdf_file_path