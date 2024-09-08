# LLM_PowerBi

---

# **LLM_PowerBi is kind of AI-Enhanced Interactive Dashboard Builder**

An interactive AI-powered dashboard builder that provides insightful visualizations such as bar charts, line charts, scatter plots, and heatmaps. The dashboard dynamically adjusts based on user input and provides trend analysis, predictions, and anomaly detection.

## **Features**

- **File Upload**: Upload CSV files directly to visualize your data.
- **Dynamic Visualizations**: Automatically generate bar charts, line charts, scatter plots, and heatmaps from your dataset.
- **KPI Adjustment**: Use sliders to adjust KPI values in real-time, with updated visualizations.
- **AI-Powered Recommendations**: Receive AI-generated suggestions for data visualization and layout based on your dataset.
- **Anomaly Detection**: Detect anomalies in KPI trends using basic statistical methods.
- **Trend Analysis**: See rolling average trends for your KPIs over time.

## **Getting Started**

### **1. Prerequisites**

Ensure you have Python installed and the required libraries. To install the necessary dependencies, run:

```bash
pip install groq gradio pandas numpy matplotlib plotly
```

### **2. Running the Application**

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Run the Python file using the following command:

```bash
python app.py
```

4. A local server will be started. Open your browser and navigate to the URL provided (usually `http://127.0.0.1:7860/`).

### **3. Usage**

- **Upload CSV File**: Upload your dataset in CSV format.
- **KPI Column**: Specify which column in your dataset represents the KPI values.
- **Adjust KPI**: Use the slider to adjust KPI values dynamically.
- **View Visualizations**: The AI will automatically generate a variety of charts and graphs based on the data and provide insights.
  ![111](https://github.com/user-attachments/assets/160bae9f-7852-4443-a4b5-85fee4933fbd)

![222](https://github.com/user-attachments/assets/7ba426d3-e6ab-4d51-bf62-896818ec6483)


### **4. Features**

- **Data Upload**: Easily upload CSV files to input data.
- **KPI Value Adjustments**: Dynamically adjust KPI values using a slider and see the effects in real-time.
- **AI Recommendations**: Get suggestions from the Groq AI for the best visualizations and data representations.
- **Charts & Visualizations**: See various visualizations, including bar charts, line charts, scatter plots, and heatmaps.
- **Anomaly Detection**: Identify outliers and anomalies in the data.
- **Trend Analysis**: Analyze trends over time with rolling averages.

## **Project Structure**

```plaintext
.
├── app.py                 # Main application file
├── README.md              # Project documentation
└── requirements.txt       # Python package requirements
```

## **Built With**

- **[Groq](https://groq.com)** - AI model for recommendations and natural language processing.
- **[Gradio](https://gradio.app)** - Web-based interface for interacting with machine learning models.
- **[Plotly](https://plotly.com/python/)** - Interactive graphs and visualizations.
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis.
- **[NumPy](https://numpy.org/)** - Numerical computations.

## **Contributing**

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or new features.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
