"""
Data Loader Module for Brazil Hydro Energy Sector Analysis
Provides utilities for loading, cleaning, and processing datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class HydroDataLoader:
    """Data loader class for hydro energy sector analysis"""
    
    def __init__(self, data_path=None):
        """
        Initialize data loader
        
        Args:
            data_path (str): Path to data directory (optional)
        """
        if data_path is None:
            # Try to find the data directory relative to the project root
            current_dir = Path(__file__).parent
            # Go up to src, then up to project root, then to data
            project_root = current_dir.parent.parent
            data_path = project_root / "data"
        
        self.data_path = Path(data_path)
        self.raw_path = self.data_path / "raw"
        self.processed_path = self.data_path / "processed"
        
    def load_market_data(self):
        """Load Brazil hydro energy market data"""
        try:
            df = pd.read_csv(self.raw_path / "brazil_hydro_data.csv")
            print(f"Loaded market data: {df.shape[0]} records, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            print("Market data file not found")
            return None
    
    def load_competitor_data(self):
        """Load competitor analysis data"""
        try:
            df = pd.read_csv(self.raw_path / "competitor_data.csv")
            print(f"Loaded competitor data: {df.shape[0]} records, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            print("Competitor data file not found")
            return None
    
    def load_customer_data(self):
        """Load customer segmentation data"""
        try:
            df = pd.read_csv(self.raw_path / "customer_data.csv")
            print(f"Loaded customer data: {df.shape[0]} records, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            print("Customer data file not found")
            return None
    
    def get_market_summary(self, df=None):
        """Generate market summary statistics"""
        if df is None:
            df = self.load_market_data()
        
        if df is not None:
            summary = df.groupby('year').agg({
                'installed_capacity_mw': 'sum',
                'generation_gwh': 'sum',
                'market_value_million_usd': 'sum',
                'investment_million_usd': 'sum',
                'number_of_plants': 'sum'
            }).reset_index()
            
            # Calculate growth rates
            for col in ['installed_capacity_mw', 'generation_gwh', 'market_value_million_usd', 'investment_million_usd']:
                summary[f'{col}_growth_pct'] = summary[col].pct_change() * 100
            
            return summary
        return None
    
    def get_regional_analysis(self, df=None):
        """Generate regional market analysis"""
        if df is None:
            df = self.load_market_data()
        
        if df is not None:
            latest_year = df['year'].max()
            regional_analysis = df[df['year'] == latest_year].copy()
            
            # Calculate market shares
            total_capacity = regional_analysis['installed_capacity_mw'].sum()
            total_value = regional_analysis['market_value_million_usd'].sum()
            
            regional_analysis['capacity_share_pct'] = (regional_analysis['installed_capacity_mw'] / total_capacity) * 100
            regional_analysis['value_share_pct'] = (regional_analysis['market_value_million_usd'] / total_value) * 100
            
            return regional_analysis
        return None
    
    def save_processed_data(self, data, filename):
        """Save processed data to processed directory"""
        try:
            output_path = self.processed_path / filename
            data.to_csv(output_path, index=False)
            print(f"Saved processed data: {output_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

def main():
    """Example usage of the data loader"""
    loader = HydroDataLoader()
    
    # Load all datasets
    market_data = loader.load_market_data()
    competitor_data = loader.load_competitor_data()
    customer_data = loader.load_customer_data()
    
    # Generate summaries
    if market_data is not None:
        market_summary = loader.get_market_summary(market_data)
        regional_analysis = loader.get_regional_analysis(market_data)
        
        # Save processed data
        loader.save_processed_data(market_summary, "market_summary.csv")
        loader.save_processed_data(regional_analysis, "regional_analysis.csv")
        
        print("\nMarket Summary:")
        print(market_summary)
        
        print("\nRegional Analysis:")
        if regional_analysis is not None:
            print(regional_analysis[['region', 'market_value_million_usd', 'value_share_pct']])
        else:
            print("No regional analysis data available")

if __name__ == "__main__":
    main() 