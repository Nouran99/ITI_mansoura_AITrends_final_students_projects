from crewai.tools import BaseTool
import pandas as pd
import io

class ExploreCSVDataTool(BaseTool):
    name: str = "Explore CSV Data Tool"
    description: str = "Performs EDA on CSV data string and returns a report."

    def _run(self, csv_string: str) -> str:
        
            df = pd.read_csv(io.StringIO(csv_string))
            report = []

            report.append("🔍 **DATA EXPLORATION REPORT** 🔍")
            report.append(f"\n🧾 Shape of the data: {df.shape[0]} rows, {df.shape[1]} columns")
            report.append("\n📋 Columns and Data Types:\n" + str(df.dtypes))
            report.append("\n🧹 Missing Values per Column:\n" + str(df.isnull().sum()))
            report.append("\n📊 Number of Unique Values per Column:\n" + str(df.nunique()))
            report.append("\n📈 Descriptive Statistics (Numerical Columns):\n" + str(df.describe(include='number').round(2)))
            report.append("\n🔢 Descriptive Statistics (Categorical Columns):\n" + str(df.describe(include='object')))

            # Top frequent values for each column
            report.append("\n📌 Top Frequent Values per Column:")
            for col in df.columns:
                top_values = df[col].value_counts(dropna=False).head(3)
                report.append(f"\n🔹 {col}:\n{top_values.to_string()}")

            # Correlation matrix
            numeric_cols = df.select_dtypes(include='number')
            if not numeric_cols.empty:
                corr = numeric_cols.corr().round(2)
                report.append("\n🔗 Correlation Matrix (numeric columns):\n" + str(corr))
            else:
                report.append("\n🔗 No numeric columns to compute correlation matrix.")

            return "\n\n".join(report)


