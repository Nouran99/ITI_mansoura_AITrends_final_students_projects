# data_processing_agent.py

import pandas as pd

class DataProcessingAgent:
    def read_file(self, file):
        filename = file.name if hasattr(file, 'name') else file

        if filename.endswith('.csv'):
            df = pd.read_csv(file)  
            return df
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file)
            return df
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8') if hasattr(file, 'read') else open(file, encoding='utf-8').read()
            return text
        else:
            return "Unsupported file type. Please upload CSV, Excel, or TXT."

    def convert_data_to_prompt(self, data):
        if isinstance(data, pd.DataFrame):
            prompt_blocks = []
            for idx, row in data.iterrows():
                user_info = [f"{col}: {row[col]}" for col in row.index]
                user_block = f"User {idx + 1}:\n\n" + "\n".join(user_info)
                prompt_blocks.append(user_block)
            prompt = "\n\n".join(prompt_blocks)

        elif isinstance(data, str):
            prompt = "User 1:\n\n" + data.strip()

        else:
            prompt = "Can't read data."

        return prompt
