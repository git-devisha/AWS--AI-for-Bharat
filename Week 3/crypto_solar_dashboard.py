#!/usr/bin/env python3
"""
Crypto vs Solar Activity Dashboard
"I hate not knowing if solar flares crash Bitcoin, so I built this."

Correlates Bitcoin price movements with solar flare activity.
Because the universe might be more connected than we think! 🌞₿
"""

import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
import numpy as np
from scipy.stats import pearsonr
import time


class CryptoSolarDashboard:
    def __init__(self):
        self.bitcoin_data = None
        self.solar_data = None
        
    def fetch_bitcoin_data(self, days=30):
        """Fetch Bitcoin price data from CoinGecko API"""
        try:
            url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Convert to DataFrame
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.drop('timestamp', axis=1)
            
            return df
            
        except Exception as e:
            st.error(f"Error fetching Bitcoin data: {e}")
            return None
    
    def fetch_solar_data(self, days=30):
        """Fetch solar flare data from NOAA Space Weather API"""
        try:
            # NOAA Space Weather Prediction Center API
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Using NOAA's solar event data
            url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Convert to DataFrame
            if len(data) > 1:  # Skip header row
                df = pd.DataFrame(data[1:], columns=data[0])
                df['time_tag'] = pd.to_datetime(df['time_tag'])
                df['date'] = df['time_tag'].dt.date
                
                # Convert numeric columns
                numeric_cols = ['density', 'speed', 'temperature']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Group by date and get daily averages
                daily_solar = df.groupby('date').agg({
                    'density': 'mean',
                    'speed': 'mean', 
                    'temperature': 'mean'
                }).reset_index()
                
                daily_solar['date'] = pd.to_datetime(daily_solar['date'])
                return daily_solar
            
            return None
            
        except Exception as e:
            st.error(f"Error fetching solar data: {e}")
            # Return mock data for demo
            return self.generate_mock_solar_data(days)
    
    def generate_mock_solar_data(self, days=30):
        """Generate realistic mock solar data for demo purposes"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate realistic solar wind data
        np.random.seed(42)  # For reproducible results
        
        solar_data = pd.DataFrame({
            'date': dates,
            'density': np.random.normal(8, 3, days),  # particles/cm³
            'speed': np.random.normal(400, 100, days),  # km/s
            'temperature': np.random.normal(100000, 50000, days)  # Kelvin
        })
        
        # Add some correlation spikes
        for i in range(0, days, 7):
            if i < days:
                solar_data.loc[i, 'speed'] += np.random.normal(200, 50)
                solar_data.loc[i, 'density'] += np.random.normal(5, 2)
        
        return solar_data
    
    def calculate_correlations(self):
        """Calculate correlations between Bitcoin and solar activity"""
        if self.bitcoin_data is None or self.solar_data is None:
            return {}
        
        # Merge data on date
        merged = pd.merge(self.bitcoin_data, self.solar_data, on='date', how='inner')
        
        if len(merged) < 2:
            return {}
        
        correlations = {}
        solar_metrics = ['density', 'speed', 'temperature']
        
        for metric in solar_metrics:
            if metric in merged.columns:
                corr, p_value = pearsonr(merged['price'], merged[metric])
                correlations[metric] = {
                    'correlation': corr,
                    'p_value': p_value,
                    'strength': self.interpret_correlation(abs(corr))
                }
        
        return correlations
    
    def interpret_correlation(self, corr):
        """Interpret correlation strength"""
        if corr >= 0.7:
            return "Strong"
        elif corr >= 0.3:
            return "Moderate"
        elif corr >= 0.1:
            return "Weak"
        else:
            return "Very Weak"
    
    def create_dashboard(self):
        """Create the Streamlit dashboard"""
        st.set_page_config(
            page_title="🌞₿ Crypto vs Solar Activity",
            page_icon="🌞",
            layout="wide"
        )
        
        st.title("🌞₿ Bitcoin vs Solar Activity Dashboard")
        st.markdown("*Exploring the cosmic connection between cryptocurrency and space weather*")
        
        # Sidebar controls
        st.sidebar.header("⚙️ Settings")
        days = st.sidebar.slider("Days of data", 7, 90, 30)
        
        if st.sidebar.button("🔄 Refresh Data"):
            st.cache_data.clear()
        
        # Fetch data
        with st.spinner("Fetching Bitcoin data..."):
            self.bitcoin_data = self.fetch_bitcoin_data(days)
        
        with st.spinner("Fetching solar activity data..."):
            self.solar_data = self.fetch_solar_data(days)
        
        if self.bitcoin_data is None or self.solar_data is None:
            st.error("Failed to fetch data. Please try again.")
            return
        
        # Calculate correlations
        correlations = self.calculate_correlations()
        
        # Main dashboard layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.create_price_chart()
            self.create_correlation_chart()
        
        with col2:
            self.create_metrics_panel(correlations)
            self.create_solar_activity_gauge()
        
        # Bottom section
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            self.create_correlation_table(correlations)
        
        with col4:
            self.create_insights_panel(correlations)
    
    def create_price_chart(self):
        """Create Bitcoin price chart"""
        st.subheader("📈 Bitcoin Price Movement")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.bitcoin_data['date'],
            y=self.bitcoin_data['price'],
            mode='lines',
            name='Bitcoin Price',
            line=dict(color='#f7931a', width=2)
        ))
        
        fig.update_layout(
            title="Bitcoin Price (USD)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_correlation_chart(self):
        """Create correlation visualization"""
        st.subheader("🌊 Solar Wind vs Bitcoin Price")
        
        # Merge data for plotting
        merged = pd.merge(self.bitcoin_data, self.solar_data, on='date', how='inner')
        
        if len(merged) == 0:
            st.warning("No overlapping data found")
            return
        
        # Create subplot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Bitcoin price
        fig.add_trace(
            go.Scatter(
                x=merged['date'],
                y=merged['price'],
                name="Bitcoin Price",
                line=dict(color='#f7931a')
            ),
            secondary_y=False,
        )
        
        # Solar wind speed
        fig.add_trace(
            go.Scatter(
                x=merged['date'],
                y=merged['speed'],
                name="Solar Wind Speed",
                line=dict(color='#ff6b6b')
            ),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Bitcoin Price (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Solar Wind Speed (km/s)", secondary_y=True)
        
        fig.update_layout(height=400, title="Bitcoin Price vs Solar Wind Speed")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_metrics_panel(self, correlations):
        """Create metrics panel"""
        st.subheader("📊 Key Metrics")
        
        if self.bitcoin_data is not None and len(self.bitcoin_data) > 1:
            current_price = self.bitcoin_data['price'].iloc[-1]
            price_change = ((current_price - self.bitcoin_data['price'].iloc[-2]) / 
                          self.bitcoin_data['price'].iloc[-2] * 100)
            
            st.metric(
                "Bitcoin Price",
                f"${current_price:,.2f}",
                f"{price_change:+.2f}%"
            )
        
        if self.solar_data is not None and len(self.solar_data) > 0:
            latest_solar = self.solar_data.iloc[-1]
            
            st.metric(
                "Solar Wind Speed",
                f"{latest_solar['speed']:.0f} km/s"
            )
            
            st.metric(
                "Solar Wind Density",
                f"{latest_solar['density']:.1f} p/cm³"
            )
    
    def create_solar_activity_gauge(self):
        """Create solar activity gauge"""
        st.subheader("🌞 Solar Activity Level")
        
        if self.solar_data is not None and len(self.solar_data) > 0:
            latest_speed = self.solar_data['speed'].iloc[-1]
            
            # Determine activity level
            if latest_speed > 600:
                level = "High"
                color = "red"
            elif latest_speed > 450:
                level = "Moderate"
                color = "orange"
            else:
                level = "Low"
                color = "green"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; 
                        background-color: {color}20; border: 2px solid {color};">
                <h2 style="color: {color}; margin: 0;">{level}</h2>
                <p style="margin: 5px 0;">Solar Wind: {latest_speed:.0f} km/s</p>
            </div>
            """, unsafe_allow_html=True)
    
    def create_correlation_table(self, correlations):
        """Create correlation results table"""
        st.subheader("🔗 Correlation Analysis")
        
        if not correlations:
            st.info("Not enough data for correlation analysis")
            return
        
        corr_data = []
        for metric, data in correlations.items():
            corr_data.append({
                'Solar Metric': metric.title(),
                'Correlation': f"{data['correlation']:.3f}",
                'Strength': data['strength'],
                'P-Value': f"{data['p_value']:.3f}"
            })
        
        df = pd.DataFrame(corr_data)
        st.dataframe(df, use_container_width=True)
    
    def create_insights_panel(self, correlations):
        """Create insights panel"""
        st.subheader("🧠 AI Insights")
        
        insights = []
        
        if correlations:
            strongest_corr = max(correlations.items(), 
                               key=lambda x: abs(x[1]['correlation']))
            
            metric, data = strongest_corr
            corr_val = data['correlation']
            
            if abs(corr_val) > 0.3:
                direction = "positive" if corr_val > 0 else "negative"
                insights.append(f"📈 Strongest correlation found with {metric} "
                              f"({direction}, r={corr_val:.3f})")
            else:
                insights.append("📊 No strong correlations detected")
        
        # Add some fun insights
        insights.extend([
            "🌞 Solar wind speed varies from 300-800 km/s normally",
            "₿ Bitcoin volatility might be more earthly than cosmic",
            "🔬 Correlation ≠ causation (but it's fun to explore!)"
        ])
        
        for insight in insights:
            st.info(insight)


def main():
    dashboard = CryptoSolarDashboard()
    dashboard.create_dashboard()


if __name__ == "__main__":
    main()