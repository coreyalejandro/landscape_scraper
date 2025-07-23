import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import subprocess
import time
import threading
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="South Florida Property Scraper",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-running {
        color: #ff6347;
        font-weight: bold;
    }
    .status-complete {
        color: #32cd32;
        font-weight: bold;
    }
    .section-header {
        color: #1f77b4;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def load_config():
    """Load current configuration"""
    try:
        with open('config.js', 'r') as f:
            # Simple parsing since it's a JS module.exports
            content = f.read()
            # Extract the configuration object (this is a simplified approach)
            import re
            # For now, return default config - could be enhanced to parse actual JS
            return {
                "regions": {"broward": True, "dade": True, "miami": True},
                "entityTypes": {"hoa": True, "propertyManagement": True},
                "sources": {
                    "propertyAppraisers": False,
                    "dbpr": False,
                    "directories": True,
                    "sunbiz": False,
                    "googleMaps": True,
                    "yelpPages": True,
                    "thirdParty": True,
                    "realEstateBoards": False,
                    "chamberOfCommerce": False
                },
                "requestDelay": 2000,
                "browserInstances": 2
            }
    except:
        return {}

def load_results():
    """Load scraping results"""
    try:
        with open('results/data.json', 'r') as f:
            return json.load(f)
    except:
        return []

def load_summary():
    """Load scraping summary"""
    try:
        with open('results/summary.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def is_scraper_running():
    """Check if scraper is currently running"""
    return st.session_state.get('scraper_running', False)

def run_scraper():
    """Run the scraper in background"""
    def scraper_thread():
        try:
            st.session_state.scraper_running = True
            st.session_state.scraper_output = "Starting scraper...\n"
            
            # Run the scraper
            process = subprocess.Popen(
                ['node', 'scraper.js'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            output_lines = []
            for line in process.stdout:
                output_lines.append(line)
                st.session_state.scraper_output = "".join(output_lines)
            
            process.wait()
            st.session_state.scraper_running = False
            st.session_state.scraper_finished = True
            
        except Exception as e:
            st.session_state.scraper_running = False
            st.session_state.scraper_error = str(e)
    
    # Start the scraper in a separate thread
    thread = threading.Thread(target=scraper_thread)
    thread.daemon = True
    thread.start()

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 South Florida Property Scraper</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Dashboard", 
        "Run Scraper", 
        "Configuration", 
        "Data Analysis",
        "Export Data"
    ])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Run Scraper":
        show_scraper_interface()
    elif page == "Configuration":
        show_configuration()
    elif page == "Data Analysis":
        show_data_analysis()
    elif page == "Export Data":
        show_export_data()

def show_dashboard():
    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    # Load current data
    results = load_results()
    summary = load_summary()
    
    if not results:
        st.info("No scraping results found. Run the scraper to see data here!")
        return
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entities", len(results))
    
    with col2:
        hoa_count = len([r for r in results if r.get('entityType') == 'hoa'])
        st.metric("HOAs Found", hoa_count)
    
    with col3:
        pm_count = len([r for r in results if r.get('entityType') == 'propertyManagement'])
        st.metric("Property Managers", pm_count)
    
    with col4:
        with_websites = len([r for r in results if r.get('website')])
        st.metric("With Websites", with_websites)
    
    # Recent results
    st.markdown('<div class="section-header">🔍 Recent Results</div>', unsafe_allow_html=True)
    
    if results:
        df = pd.DataFrame(results)
        
        # Display recent results table
        st.dataframe(
            df[['name', 'entityType', 'address', 'phone', 'website']].head(10),
            use_container_width=True
        )
        
        # Entity type distribution chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Entity Types")
            entity_counts = df['entityType'].value_counts()
            fig = px.pie(values=entity_counts.values, names=entity_counts.index, 
                        title="Distribution of Entity Types")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Sources")
            source_counts = df['source'].value_counts()
            fig = px.bar(x=source_counts.index, y=source_counts.values,
                        title="Results by Source")
            st.plotly_chart(fig, use_container_width=True)

def show_scraper_interface():
    st.markdown('<div class="section-header">🚀 Run Scraper</div>', unsafe_allow_html=True)
    
    # Current status
    if is_scraper_running():
        st.markdown('<p class="status-running">🔄 Scraper is currently running...</p>', 
                   unsafe_allow_html=True)
        
        # Show progress if available
        if 'scraper_output' in st.session_state:
            st.text_area("Live Output", st.session_state.scraper_output, height=400)
        
        # Auto-refresh
        time.sleep(2)
        st.rerun()
        
    elif st.session_state.get('scraper_finished', False):
        st.markdown('<p class="status-complete">✅ Scraper completed successfully!</p>', 
                   unsafe_allow_html=True)
        
        # Show final output
        if 'scraper_output' in st.session_state:
            st.text_area("Final Output", st.session_state.scraper_output, height=400)
        
        # Reset button
        if st.button("Reset Status"):
            st.session_state.scraper_finished = False
            st.session_state.scraper_output = ""
            st.rerun()
    
    else:
        st.info("Click the button below to start scraping South Florida properties!")
        
        # Configuration preview
        config = load_config()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Current Settings")
            enabled_sources = [k for k, v in config.get('sources', {}).items() if v]
            st.write(f"**Enabled Sources:** {', '.join(enabled_sources)}")
            st.write(f"**Browser Instances:** {config.get('browserInstances', 2)}")
            st.write(f"**Request Delay:** {config.get('requestDelay', 2000)}ms")
        
        with col2:
            st.subheader("Expected Results")
            st.write("🗺️ Google Maps businesses")
            st.write("🏢 Property management companies")
            st.write("🏘️ HOA organizations")
            st.write("📞 Contact information")
        
        # Start button
        if st.button("🚀 Start Scraping", type="primary", use_container_width=True):
            run_scraper()
            st.rerun()

def show_configuration():
    st.markdown('<div class="section-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    config = load_config()
    
    st.warning("⚠️ Configuration editing via web interface coming soon! For now, edit config.js directly.")
    
    # Display current configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Regions")
        for region, enabled in config.get('regions', {}).items():
            st.checkbox(region.title(), value=enabled, disabled=True)
        
        st.subheader("Entity Types")
        for entity_type, enabled in config.get('entityTypes', {}).items():
            st.checkbox(entity_type.replace('propertyManagement', 'Property Management').title(), 
                       value=enabled, disabled=True)
    
    with col2:
        st.subheader("Data Sources")
        for source, enabled in config.get('sources', {}).items():
            icon = "✅" if enabled else "❌"
            st.write(f"{icon} {source.replace('propertyAppraisers', 'Property Appraisers').replace('googleMaps', 'Google Maps').title()}")
        
        st.subheader("Performance Settings")
        st.write(f"**Browser Instances:** {config.get('browserInstances', 2)}")
        st.write(f"**Request Delay:** {config.get('requestDelay', 2000)}ms")

def show_data_analysis():
    st.markdown('<div class="section-header">📈 Data Analysis</div>', unsafe_allow_html=True)
    
    results = load_results()
    
    if not results:
        st.info("No data available for analysis. Run the scraper first!")
        return
    
    df = pd.DataFrame(results)
    
    # Data quality metrics
    st.subheader("Data Quality Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        complete_records = len(df.dropna(subset=['name', 'address']))
        st.metric("Complete Records", f"{complete_records}/{len(df)}")
    
    with col2:
        with_phone = len(df[df['phone'].notna() & (df['phone'] != 'Send to phone')])
        st.metric("Valid Phone Numbers", f"{with_phone}/{len(df)}")
    
    with col3:
        with_website = len(df[df['website'].notna()])
        st.metric("With Websites", f"{with_website}/{len(df)}")
    
    with col4:
        classified = len(df[df['entityType'] != 'unknown'])
        st.metric("Classified Entities", f"{classified}/{len(df)}")
    
    # Geographic distribution
    st.subheader("Geographic Distribution")
    
    # Extract cities from addresses
    df['city'] = df['address'].str.extract(r', ([^,]+), FL')
    city_counts = df['city'].value_counts().head(10)
    
    if not city_counts.empty:
        fig = px.bar(x=city_counts.values, y=city_counts.index, orientation='h',
                    title="Top 10 Cities by Business Count")
        st.plotly_chart(fig, use_container_width=True)
    
    # Entity classification analysis
    st.subheader("Entity Classification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entity_dist = df['entityType'].value_counts()
        fig = px.pie(values=entity_dist.values, names=entity_dist.index,
                    title="Entity Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        source_perf = df.groupby('source').size().sort_values(ascending=True)
        fig = px.bar(x=source_perf.values, y=source_perf.index, orientation='h',
                    title="Results by Data Source")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed data table
    st.subheader("Detailed Results")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        entity_filter = st.selectbox("Filter by Entity Type", 
                                   ['All'] + list(df['entityType'].unique()))
    
    with col2:
        source_filter = st.selectbox("Filter by Source",
                                   ['All'] + list(df['source'].unique()))
    
    with col3:
        city_filter = st.selectbox("Filter by City",
                                 ['All'] + list(df['city'].dropna().unique()))
    
    # Apply filters
    filtered_df = df.copy()
    
    if entity_filter != 'All':
        filtered_df = filtered_df[filtered_df['entityType'] == entity_filter]
    
    if source_filter != 'All':
        filtered_df = filtered_df[filtered_df['source'] == source_filter]
    
    if city_filter != 'All':
        filtered_df = filtered_df[filtered_df['city'] == city_filter]
    
    # Display filtered results
    st.dataframe(
        filtered_df[['name', 'entityType', 'address', 'phone', 'website', 'source']],
        use_container_width=True
    )

def show_export_data():
    st.markdown('<div class="section-header">📤 Export Data</div>', unsafe_allow_html=True)
    
    results = load_results()
    
    if not results:
        st.info("No data available for export. Run the scraper first!")
        return
    
    df = pd.DataFrame(results)
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Downloads")
        
        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Download as CSV",
            data=csv,
            file_name=f"scraped_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # JSON download
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📋 Download as JSON",
            data=json_str,
            file_name=f"scraped_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.subheader("Export Statistics")
        st.write(f"**Total Records:** {len(df)}")
        st.write(f"**Data Fields:** {len(df.columns)}")
        st.write(f"**File Size (CSV):** ~{len(csv.encode('utf-8')) // 1024} KB")
        st.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Export preview
    st.subheader("Export Preview")
    st.dataframe(df.head(), use_container_width=True)

# Initialize session state
if 'scraper_running' not in st.session_state:
    st.session_state.scraper_running = False

if 'scraper_finished' not in st.session_state:
    st.session_state.scraper_finished = False

if __name__ == "__main__":
    main() 