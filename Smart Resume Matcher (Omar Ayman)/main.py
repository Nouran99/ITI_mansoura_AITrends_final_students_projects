from agents.job_parser import JobParserAgent

job_desc = """We are looking for a Machine Learning Engineer with experience in NLP, Python,
and deploying models using Docker and AWS. Familiarity with Hugging Face Transformers is a plus."""

agent = JobParserAgent()
result = agent.run(job_desc)
print(result)
