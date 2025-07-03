"""
Chart Generator Module for Brazil Hydro Energy Sector Analysis
Provides utilities for creating standardized visualizations
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class HydroChartGenerator:
    """Chart generator class for hydro energy sector analysis"""
    
    def __init__(self):
        """Initialize chart generator"""
        # Set default styles
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configure plotly
        import plotly.io as pio
        pio.templates.default = "plotly_white"
        
        # Define color schemes
        self.colors = {
            'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'qualitative': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
            'sequential': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c']
        }
    
    def create_market_trends_chart(self, market_summary, title="Brazil Hydro Energy Market Trends"):
        """Create comprehensive market trends visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Installed Capacity (MW)', 'Generation (GWh)', 
                           'Market Value (Million USD)', 'Investment (Million USD)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Installed Capacity
        fig.add_trace(
            go.Scatter(x=market_summary['year'], y=market_summary['installed_capacity_mw'],
                       mode='lines+markers', name='Installed Capacity',
                       line=dict(color=self.colors['primary'][0], width=3)),
            row=1, col=1
        )
        
        # Generation
        fig.add_trace(
            go.Scatter(x=market_summary['year'], y=market_summary['generation_gwh'],
                       mode='lines+markers', name='Generation',
                       line=dict(color=self.colors['primary'][1], width=3)),
            row=1, col=2
        )
        
        # Market Value
        fig.add_trace(
            go.Scatter(x=market_summary['year'], y=market_summary['market_value_million_usd'],
                       mode='lines+markers', name='Market Value',
                       line=dict(color=self.colors['primary'][2], width=3)),
            row=2, col=1
        )
        
        # Investment
        fig.add_trace(
            go.Scatter(x=market_summary['year'], y=market_summary['investment_million_usd'],
                       mode='lines+markers', name='Investment',
                       line=dict(color=self.colors['primary'][3], width=3)),
            row=2, col=2
        )
        
        fig.update_layout(
            title=title,
            height=800,
            showlegend=False
        )
        
        return fig
    
    def create_regional_analysis_chart(self, regional_data, title="Regional Market Analysis"):
        """Create regional market analysis visualization"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Market Share by Region', 'Installed Capacity by Region'),
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Market share pie chart
        fig.add_trace(
            go.Pie(labels=regional_data['region'], 
                   values=regional_data['market_value_million_usd'],
                   name="Market Share"),
            row=1, col=1
        )
        
        # Capacity bar chart
        fig.add_trace(
            go.Bar(x=regional_data['region'], 
                   y=regional_data['installed_capacity_mw'],
                   name="Installed Capacity"),
            row=1, col=2
        )
        
        fig.update_layout(
            title=title,
            height=500
        )
        
        return fig
    
    def create_competitor_analysis_chart(self, competitor_data, title="Competitive Analysis"):
        """Create competitive analysis visualization"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Market Share Distribution', 'Competitive Positioning'),
            specs=[[{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Market share pie chart
        fig.add_trace(
            go.Pie(labels=competitor_data['company_name'], 
                   values=competitor_data['market_share_percent'],
                   name="Market Share"),
            row=1, col=1
        )
        
        # Competitive positioning scatter
        fig.add_trace(
            go.Scatter(x=competitor_data['market_share_percent'],
                       y=competitor_data['strength_score'],
                       mode='markers+text',
                       text=competitor_data['company_name'],
                       textposition="top center",
                       marker=dict(size=competitor_data['installed_capacity_mw']/1000),
                       name="Positioning"),
            row=1, col=2
        )
        
        fig.update_layout(
            title=title,
            height=600
        )
        
        fig.update_xaxes(title_text="Market Share (%)", row=1, col=2)
        fig.update_yaxes(title_text="Strength Score", row=1, col=2)
        
        return fig
    
    def create_customer_segmentation_chart(self, customer_data, title="Customer Segmentation"):
        """Create customer segmentation visualization"""
        # Customer type distribution
        customer_type_dist = customer_data['customer_type'].value_counts()
        size_category_dist = customer_data['size_category'].value_counts()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Customer Type Distribution', 'Size Category Distribution'),
            specs=[[{"type": "pie"}, {"type": "pie"}]]
        )
        
        # Customer type pie chart
        fig.add_trace(
            go.Pie(labels=customer_type_dist.index, 
                   values=customer_type_dist.values,
                   name="Customer Type"),
            row=1, col=1
        )
        
        # Size category pie chart
        fig.add_trace(
            go.Pie(labels=size_category_dist.index, 
                   values=size_category_dist.values,
                   name="Size Category"),
            row=1, col=2
        )
        
        fig.update_layout(
            title=title,
            height=500
        )
        
        return fig
    
    def create_forecast_chart(self, historical_data, forecast_data, title="Market Forecast"):
        """Create forecasting visualization"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['year'],
            y=historical_data['market_value_million_usd'],
            mode='lines+markers',
            name='Historical',
            line=dict(color=self.colors['primary'][0], width=3)
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=forecast_data['year'],
            y=forecast_data['market_value_forecast'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color=self.colors['primary'][1], width=3, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title='Market Value (Million USD)',
            height=500
        )
        
        return fig
    
    def create_technology_adoption_chart(self, tech_data, title="Technology Adoption"):
        """Create technology adoption visualization"""
        fig = px.bar(
            tech_data,
            x='technology',
            y=['current_share', 'forecast_2030'],
            title=title,
            barmode='group',
            color_discrete_sequence=self.colors['primary']
        )
        
        fig.update_layout(height=500)
        return fig
    
    def create_risk_analysis_chart(self, risk_data, title="Risk Analysis"):
        """Create risk analysis visualization"""
        fig = px.bar(
            risk_data,
            x='risk_score',
            y='risk_factor',
            orientation='h',
            title=title,
            color='risk_score',
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=400)
        return fig
    
    def save_chart(self, fig, filename, format='html'):
        """Save chart to file"""
        try:
            if format == 'html':
                fig.write_html(filename)
            elif format == 'png':
                fig.write_image(filename)
            elif format == 'pdf':
                fig.write_image(filename)
            print(f"Chart saved: {filename}")
        except Exception as e:
            print(f"Error saving chart: {e}")

def main():
    """Example usage of the chart generator"""
    try:
        import sys
        import os
        # Add the parent directory to the path to import data_loader
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_processing'))
        from data_loader import HydroDataLoader
        
        # Load data
        loader = HydroDataLoader()
        market_data = loader.load_market_data()
        competitor_data = loader.load_competitor_data()
        customer_data = loader.load_customer_data()
        
        # Create chart generator
        chart_gen = HydroChartGenerator()
        
        if market_data is not None:
            # Generate market summary
            market_summary = loader.get_market_summary(market_data)
            
            # Create charts
            trends_chart = chart_gen.create_market_trends_chart(market_summary)
            regional_chart = chart_gen.create_regional_analysis_chart(
                loader.get_regional_analysis(market_data)
            )
            
            # Save charts
            chart_gen.save_chart(trends_chart, "market_trends.html")
            chart_gen.save_chart(regional_chart, "regional_analysis.html")
            
            print("Charts generated successfully!")
        else:
            print("No market data available. Please check data files.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required packages are installed and data files exist.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 