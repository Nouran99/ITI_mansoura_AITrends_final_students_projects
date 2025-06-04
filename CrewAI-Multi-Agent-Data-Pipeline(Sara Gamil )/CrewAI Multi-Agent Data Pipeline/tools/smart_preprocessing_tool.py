import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from crewai.tools import BaseTool

class SmartPreprocessingTool(BaseTool):
    name: str = "Smart Preprocessing Tool"
    description: str = "Preprocesses dataset: removes duplicates, handles nulls, scales outliers, and encodes categorical data."

    def _run(self, csv_path: str) -> str:
        if not os.path.exists(csv_path):
            return f"❌ File not found: {csv_path}"

        df = pd.read_csv(csv_path)
        original_shape = df.shape

        # Optional: check for EDA file
        eda_text = ""
        if os.path.exists("eda_report.txt"):
            with open("eda_report.txt", "r", encoding="utf-8") as file:
                eda_text = file.read()[:800] + "..."

        strategy = ["📊 **PREPROCESSING STRATEGY REPORT** 📊", f"📁 File: {csv_path}"]
        if eda_text:
            strategy.append(f"\n🧠 Based on EDA Insights:\n{eda_text}")

        # 1. Remove duplicates
        duplicates_removed = df.duplicated().sum()
        df.drop_duplicates(inplace=True)
        strategy.append(f"✅ Removed {duplicates_removed} duplicate rows.")

        # 2. Handle missing values
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df.select_dtypes(include='object').columns

        df[num_cols] = df[num_cols].apply(lambda x: x.fillna(x.median()))
        df[cat_cols] = df[cat_cols].apply(lambda x: x.fillna(x.mode()[0]))

        strategy.append(f"🧼 Filled missing values (numerical: median, categorical: mode).")

        # 3. Scale numerical features
        scaler = RobustScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
        strategy.append("📐 Scaled numerical features using RobustScaler.")

        # 4. Encode categorical features
        ordinal_features = ['CALC', 'CAEC']
        ordinal_mapping = {
            'CALC': ['no', 'Sometimes', 'Frequently', 'Always'],
            'CAEC': ['no', 'Sometimes', 'Frequently', 'Always']
        }

        for col in ordinal_features:
            if col in df.columns:
                df[col] = pd.Categorical(df[col], categories=ordinal_mapping[col], ordered=True)

        ordinal_cols = [col for col in ordinal_features if col in df.columns]
        nominal_cols = list(set(cat_cols) - set(ordinal_cols))

        transformers = []
        if ordinal_cols:
            transformers.append(('ord', OrdinalEncoder(), ordinal_cols))
        if nominal_cols:
            transformers.append(('nom', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), nominal_cols))

        if transformers:
            preprocessor = ColumnTransformer(transformers, remainder='passthrough')
            df_processed = preprocessor.fit_transform(df)

            new_columns = []
            if ordinal_cols:
                new_columns.extend(ordinal_cols)
            if nominal_cols:
                ohe = preprocessor.named_transformers_['nom']
                new_columns.extend(ohe.get_feature_names_out(nominal_cols))
            new_columns.extend([col for col in df.columns if col not in ordinal_cols + nominal_cols])

            df = pd.DataFrame(df_processed, columns=new_columns)

        strategy.append(f"🔠 Encoded: Ordinal({ordinal_cols}) + OneHot({nominal_cols})")

        os.makedirs("processed_output", exist_ok=True)
        processed_path = os.path.join("processed_output", "processed_data.csv")
        strategy_path = os.path.join("processed_output", "preprocessing_strategy.txt")

        df.to_csv(processed_path, index=False)
        with open(strategy_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(strategy))

        return f"""
✅ Preprocessing completed successfully.
📄 Processed data saved to: {processed_path}
📝 Strategy explanation saved to: {strategy_path}

📌 Sample Processed Data Preview:
{df.head(5).to_string(index=False)}
"""

