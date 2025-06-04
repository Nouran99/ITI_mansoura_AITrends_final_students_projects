from crewai.tools import BaseTool
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import base64

class DataDashboardTool(BaseTool):
    name: str = "Data Dashboard Tool"
    description: str = "Generates visualizations and insights from a given CSV file."

    def _run(self, csv_path: str) -> str:
       
            df = pd.read_csv(csv_path)
            output_dir = "dashboard_output"
            os.makedirs(output_dir, exist_ok=True)
            insights = []

            # Save data summary
            description = df.describe(include='all').transpose()
            description.to_csv(f"{output_dir}/summary.csv")

            image_tags = []

            # Numerical features plots and insights
            for column in df.select_dtypes(include=['int64', 'float64']).columns:
                data = df[column].dropna()

                # Histogram
                hist_path = f"{output_dir}/{column}_hist.png"
                plt.figure(figsize=(8, 5))
                sns.histplot(data, kde=True)
                plt.title(f"Distribution of {column}")
                plt.savefig(hist_path)
                plt.close()

                # Box plot
                box_path = f"{output_dir}/{column}_box.png"
                plt.figure(figsize=(8, 5))
                sns.boxplot(x=data)
                plt.title(f"Box Plot of {column}")
                plt.savefig(box_path)
                plt.close()

                # Insight about skewness and outliers
                skewness = data.skew()
                outliers = data[(data < data.quantile(0.25) - 1.5 * data.std()) |
                                (data > data.quantile(0.75) + 1.5 * data.std())]
                insights.append(f"<h3>{column}</h3>")
                insights.append(f"<p>Skewness: {skewness:.2f}</p>")
                if skewness > 1 or skewness < -1:
                    insights.append("<p>Highly skewed distribution.</p>")
                elif skewness > 0.5 or skewness < -0.5:
                    insights.append("<p>Moderately skewed.</p>")
                else:
                    insights.append("<p>Fairly symmetric.</p>")

                insights.append(f"<p>Outliers detected: {len(outliers)} values.</p>")

                # Encode images to base64 and create img tags
                for img_path in [hist_path, box_path]:
                    with open(img_path, "rb") as image_file:
                        encoded = base64.b64encode(image_file.read()).decode()
                        img_tag = f'<img src="data:image/png;base64,{encoded}" alt="{column} plot" style="max-width:100%;height:auto;">'
                        image_tags.append(img_tag)

            # Categorical features plots and insights
            for column in df.select_dtypes(include='object').columns:
                unique_vals = df[column].nunique()
                top_values = df[column].value_counts(normalize=True).head(3)

                if unique_vals <= 10:
                    count_path = f"{output_dir}/{column}_count.png"
                    plt.figure(figsize=(8, 5))
                    sns.countplot(x=column, data=df)
                    plt.title(f"Count Plot of {column}")
                    plt.xticks(rotation=45)
                    plt.savefig(count_path)
                    plt.close()

                    insights.append(f"<h3>{column}</h3>")
                    for cat, pct in top_values.items():
                        insights.append(f"<p>{cat}: {pct*100:.1f}%</p>")

                    # Encode image to base64 and create img tag
                    with open(count_path, "rb") as image_file:
                        encoded = base64.b64encode(image_file.read()).decode()
                        img_tag = f'<img src="data:image/png;base64,{encoded}" alt="{column} count plot" style="max-width:100%;height:auto;">'
                        image_tags.append(img_tag)

            # Generate HTML content
            html_content = "<html><head><title>Data Dashboard</title></head><body>"
            html_content += "<h1>Visual Insights</h1>"
            html_content += "".join(image_tags)
            html_content += "<h2>Insights</h2>"
            html_content += "".join(insights)
            html_content += "</body></html>"

            # Save HTML file
            html_path = f"{output_dir}/insights_dashboard.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return f"Dashboard and insights saved in '{html_path}'."


