from groq import Groq
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import gradio as gr
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to query the Groq LLM
def recommend_dashboard(data_type, user_data):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    system_message = f"""You are an AI assistant specializing in data visualization and dashboard design. Analyze the given data and provide recommendations for:
    1. The most suitable dashboard layout
    2. Appropriate chart types for visualizing the data
    3. Key insights that can be derived from the data
    4. Potential interactive elements to enhance user experience
    5. Any additional features or analyses that could provide value

    Data type: {data_type}
    """

    user_message = f"Here is a sample of the user's data: {user_data[:500]}... Please provide detailed recommendations for creating an effective dashboard."

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=False,
    )
    
    return completion.choices[0].message.content

# Function to create various visualizations
def create_visualizations(data, kpi_column, category_column, date_column, adjustment_value=1.0):
    try:
        df = pd.read_csv(io.StringIO(data))
        
        # Check if all required columns exist
        required_columns = [kpi_column, category_column, date_column]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f"Error: The following columns are missing from the data: {', '.join(missing_columns)}"
        
        # Adjust KPI values based on slider
        df[kpi_column] = df[kpi_column] * adjustment_value

        # Create bar chart for KPI distribution
        bar_chart = px.bar(df, x=category_column, y=kpi_column, title=f"{kpi_column} Distribution by {category_column}")
        
        # Create line chart for KPI trend
        line_chart = px.line(df, x=date_column, y=kpi_column, title=f"{kpi_column} Trend Over Time")
        
        # Create scatter plot for correlation analysis
        scatter_plot = px.scatter(df, x=df.columns[0], y=kpi_column, color=category_column,
                                  title=f"Scatter Plot of {kpi_column} vs {df.columns[0]}")

        # Create heatmap for categorical data trends
        heatmap = px.density_heatmap(df, x=category_column, y=kpi_column, title=f"Heatmap of {kpi_column} Distribution")

        # Create box plot for distribution analysis
        box_plot = px.box(df, x=category_column, y=kpi_column, title=f"Box Plot of {kpi_column} by {category_column}")

        return bar_chart, line_chart, scatter_plot, heatmap, box_plot
    except Exception as e:
        return f"Error in creating visualizations: {str(e)}"

def dashboard_interface(data_type, data, kpi_column, category_column, date_column, adjustment_value):
    try:
        recommendation = recommend_dashboard(data_type, data)
        
        # Generate various charts
        vis_result = create_visualizations(data, kpi_column, category_column, date_column, adjustment_value)
        
        if isinstance(vis_result, str):  # If there's an error message
            return (recommendation, vis_result) + tuple([None] * 7)  # Return None for all plots and dataframes
        
        bar_chart, line_chart, scatter_plot, heatmap, box_plot = vis_result
        
        # Analyze trends and anomalies
        trend_result = analyze_trends_and_anomalies(data, kpi_column, date_column)
        
        if isinstance(trend_result, str):  # If there's an error message
            return (recommendation, bar_chart, line_chart, scatter_plot, heatmap, box_plot, trend_result) + tuple([None] * 2)
        
        trend_data, forecast_data = trend_result
        
        # Create combined trend and forecast plot
        trend_forecast_plot = go.Figure()
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column], y=trend_data[kpi_column], mode='lines', name='Actual'))
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column], y=trend_data['Rolling_Avg'], mode='lines', name='Rolling Average'))
        trend_forecast_plot.add_trace(go.Scatter(x=forecast_data[date_column], y=forecast_data['Forecast'], mode='lines', name='Forecast', line=dict(dash='dash')))
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column][trend_data['Anomaly']], 
                                                 y=trend_data[kpi_column][trend_data['Anomaly']], 
                                                 mode='markers', name='Anomalies', marker=dict(color='red', size=10)))
        trend_forecast_plot.update_layout(title=f"{kpi_column} Trend, Forecast, and Anomalies", xaxis_title="Date", yaxis_title=kpi_column)
        
        return (recommendation, bar_chart, line_chart, scatter_plot, heatmap, box_plot, 
                trend_forecast_plot, trend_data.to_dict('records'), forecast_data.to_dict('records'))
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (error_message,) + tuple([None] * 8)  # Return None for all plots and dataframes

# Update the Gradio interface
interface = gr.Interface(
    fn=dashboard_interface,
    inputs=[
        gr.Textbox(label="Data Type", placeholder="e.g., Sales Data, Weather Data"),
        gr.Textbox(label="Data (CSV format)", placeholder="Paste your CSV data here"),
        gr.Textbox(label="KPI Column", placeholder="Enter the KPI column name"),
        gr.Textbox(label="Category Column", placeholder="Enter the category column name"),
        gr.Textbox(label="Date Column", placeholder="Enter the date column name"),
        gr.Slider(minimum=0.5, maximum=1.5, value=1.0, label="Adjust KPI Value")
    ],
    outputs=[
        gr.Textbox(label="AI Recommendation or Error Message"),
        gr.Plot(label="KPI Distribution (Bar Chart)"),
        gr.Plot(label="KPI Trend (Line Chart)"),
        gr.Plot(label="Scatter Plot"),
        gr.Plot(label="Heatmap"),
        gr.Plot(label="Box Plot"),
        gr.Plot(label="Trend, Forecast, and Anomalies"),
        gr.Dataframe(label="Trend and Anomaly Analysis Data"),
        gr.Dataframe(label="Forecast Data")
    ],
    title="AI-Enhanced Interactive Dashboard Builder",
    description="Upload your data and get AI-powered recommendations and visualizations for your dashboard."
)
# Analyze trends and highlight anomalies
def analyze_trends_and_anomalies(data, kpi_column, date_column):
    try:
        df = pd.read_csv(io.StringIO(data))
        
        if kpi_column not in df.columns or date_column not in df.columns:
            return f"Error: KPI column '{kpi_column}' or Date column '{date_column}' not found in the data."
        
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
        
        # Calculate rolling average and standard deviation
        window_size = min(30, len(df) // 2)  # Adjust window size based on data length
        df['Rolling_Avg'] = df[kpi_column].rolling(window=window_size).mean()
        df['Rolling_Std'] = df[kpi_column].rolling(window=window_size).std()

        # Detect anomalies (points outside 2 standard deviations)
        df['Anomaly'] = np.abs(df[kpi_column] - df['Rolling_Avg']) > (2 * df['Rolling_Std'])
        
        # Simple forecasting: extend the rolling average for future trend
        future_dates = pd.date_range(start=df[date_column].max(), periods=30, freq='D')
        future_df = pd.DataFrame({date_column: future_dates})
        future_df['Forecast'] = df['Rolling_Avg'].iloc[-1]
        
        return df[[date_column, kpi_column, 'Rolling_Avg', 'Anomaly']], future_df
    except Exception as e:
        return f"Error in analyzing trends and anomalies: {str(e)}"
# Gradio interface for interactive dashboard
def dashboard_interface(data_type, data, kpi_column, category_column, date_column, adjustment_value):
    try:
        recommendation = recommend_dashboard(data_type, data)
        
        # Generate various charts
        vis_result = create_visualizations(data, kpi_column, category_column, date_column, adjustment_value)
        
        if isinstance(vis_result, str):  # If there's an error message
            return (vis_result, recommendation) + tuple([None] * 8)  # Return None for all plots and dataframes
        
        bar_chart, line_chart, scatter_plot, heatmap, box_plot = vis_result
        
        # Analyze trends and anomalies
        trend_result = analyze_trends_and_anomalies(data, kpi_column, date_column)
        
        if isinstance(trend_result, str):  # If there's an error message
            return (trend_result, recommendation, bar_chart, line_chart, scatter_plot, heatmap, box_plot) + tuple([None] * 3)
        
        trend_data, forecast_data = trend_result
        
        # Create combined trend and forecast plot
        trend_forecast_plot = go.Figure()
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column], y=trend_data[kpi_column], mode='lines', name='Actual'))
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column], y=trend_data['Rolling_Avg'], mode='lines', name='Rolling Average'))
        trend_forecast_plot.add_trace(go.Scatter(x=forecast_data[date_column], y=forecast_data['Forecast'], mode='lines', name='Forecast', line=dict(dash='dash')))
        trend_forecast_plot.add_trace(go.Scatter(x=trend_data[date_column][trend_data['Anomaly']], 
                                                 y=trend_data[kpi_column][trend_data['Anomaly']], 
                                                 mode='markers', name='Anomalies', marker=dict(color='red', size=10)))
        trend_forecast_plot.update_layout(title=f"{kpi_column} Trend, Forecast, and Anomalies", xaxis_title="Date", yaxis_title=kpi_column)
        
        return ("Success", recommendation, bar_chart, line_chart, scatter_plot, heatmap, box_plot, 
                trend_forecast_plot, trend_data.to_dict('records'), forecast_data.to_dict('records'))
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return (error_message, recommendation if 'recommendation' in locals() else None) + tuple([None] * 8)

# Update the Gradio interface
interface = gr.Interface(
    fn=dashboard_interface,
    inputs=[
        gr.Textbox(label="Data Type", placeholder="e.g., Sales Data, Weather Data"),
        gr.Textbox(label="Data (CSV format)", placeholder="Paste your CSV data here"),
        gr.Textbox(label="KPI Column", placeholder="Enter the KPI column name"),
        gr.Textbox(label="Category Column", placeholder="Enter the category column name"),
        gr.Textbox(label="Date Column", placeholder="Enter the date column name"),
        gr.Slider(minimum=0.5, maximum=1.5, value=1.0, label="Adjust KPI Value")
    ],
    outputs=[
        gr.Textbox(label="Status or Error Message"),
        gr.Textbox(label="AI Recommendation"),
        gr.Plot(label="KPI Distribution (Bar Chart)"),
        gr.Plot(label="KPI Trend (Line Chart)"),
        gr.Plot(label="Scatter Plot"),
        gr.Plot(label="Heatmap"),
        gr.Plot(label="Box Plot"),
        gr.Plot(label="Trend, Forecast, and Anomalies"),
        gr.Dataframe(label="Trend and Anomaly Analysis Data"),
        gr.Dataframe(label="Forecast Data")
    ],
    title="AI-Enhanced Interactive Dashboard Builder",
    description="Upload your data and get AI-powered recommendations and visualizations for your dashboard."
)


interface.launch()