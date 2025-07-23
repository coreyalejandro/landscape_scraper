# South Florida Property Scraper

A comprehensive web scraping tool for collecting contact information from HOAs and Property Management companies in South Florida (Broward, Miami-Dade, and Miami counties).

## 🌟 Features

### Core Scraper

- **Multi-source data collection**: Google Maps, Yelp, business directories
- **Intelligent entity classification**: Automatically identifies HOAs vs Property Management companies
- **Contact extraction**: Names, addresses, phone numbers, websites
- **Anti-detection**: Stealth browsing, user agent rotation, randomized delays
- **Export formats**: JSON, CSV
- **Progress tracking**: Real-time logging and progress saving

### Web Interface (Streamlit App)

- **📊 Dashboard**: Overview of scraped data with metrics and charts
- **🚀 Run Scraper**: Start and monitor scraping jobs with live output
- **⚙️ Configuration**: View and manage scraper settings
- **📈 Data Analysis**: Advanced filtering and visualization
- **📤 Export Data**: Download results in multiple formats

## 🚀 Quick Start

### Option 1: Command Line

```bash
# Install dependencies
npm install

# Run the scraper
node scraper.js
```

### Option 2: Web Interface

```bash
# Install Python dependencies
pip install streamlit pandas plotly

# Start the web app
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## 📁 Project Structure

landscape_scraper/
├── app.py              # Streamlit web interface
├── scraper.js          # Main scraper orchestrator
├── config.js           # Configuration settings
├── helpers.js          # Utility functions
├── scrapers.js         # Scraping implementations
├── dataSources.js      # Data source definitions
├── results/            # Output files
│   ├── data.json      # Scraped data
│   ├── data.csv       # CSV export
│   └── summary.json   # Statistics
├── logs/              # Log files
└── temp_data/         # Progress tracking

## 🎯 Data Sources

### Currently Enabled

- ✅ **Google Maps**: Most reliable source for business listings
- ✅ **Yelp**: Business directory with reviews
- ✅ **Third-party directories**: Property management sites
- ✅ **General directories**: CAI and other industry directories

### Available (Disabled)

- ❌ **Property Appraisers**: County government databases
- ❌ **DBPR**: Florida state licensing databases
- ❌ **Sunbiz**: Florida corporation records
- ❌ **Real Estate Boards**: Professional associations
- ❌ **Chambers of Commerce**: Local business directories

## 📊 Sample Results

The scraper finds businesses like:

- **Association Services of Florida** (Property Management)
- **Country Walk Homeowner Association** (HOA)
- **Harbor Islands** (Property Owners Association)
- **Latitude Key** (Vacation Property Management)

Each record includes:

- Business name
- Full address
- Phone number
- Website URL
- Entity type classification
- Data source

## ⚙️ Configuration

### Regions

- `broward`: Broward County
- `dade`: Miami-Dade County
- `miami`: Miami City

### Entity Types

- `hoa`: Homeowners Associations
- `propertyManagement`: Property Management Companies

### Performance Settings

- `browserInstances`: Number of parallel browsers (default: 2)
- `requestDelay`: Delay between requests in ms (default: 2000)
- `headless`: Run browsers in background (default: true)

## 🔧 Advanced Usage

### Enabling Disabled Sources

To enable more data sources, you need to update their selectors:

1. **Inspect the target website** to find current CSS selectors
2. **Update `dataSources.js`** with correct selectors
3. **Enable in `config.js`** by setting the source to `true`
4. **Test with small batches** to verify functionality

### Customizing Search Terms

Edit the `searchTerms` arrays in `dataSources.js` to target specific:

- Geographic areas
- Business types
- Keywords

### Scaling Performance

- Increase `browserInstances` for faster scraping
- Adjust `requestDelay` to balance speed vs detection
- Enable more sources once their selectors are updated

## 🐛 Troubleshooting

### Common Issues

Selector not found

- Website has changed structure
- Update selectors in `dataSources.js`

No results found

- Search terms may be too specific
- Try broader keywords
- Check if source website is accessible

Browser timeout

- Increase timeout values
- Check internet connection
- Verify Node.js/Puppeteer installation

### Debugging

Check log files:

- `logs/scraper_log.txt` - General activity
- `logs/error_log.txt` - Error details
- `temp_data/progress.json` - Current progress

## 📈 Results Analysis

### Entity Classification

The scraper automatically classifies businesses:

- **HOA**: Contains "homeowners association", "hoa", "condominium association"
- **Property Management**: Contains "property management", "rental management"
- **Both**: Contains indicators for both types
- **Unknown**: No clear classification

### Data Quality Metrics

- **Complete Records**: Have name and address
- **Valid Phone Numbers**: Not placeholder text
- **With Websites**: Have valid URLs
- **Classified Entities**: Successfully categorized

## 🤝 Contributing

To improve the scraper:

1. **Add new data sources** in `dataSources.js`
2. **Implement specialized scrapers** in `scrapers.js`
3. **Enhance entity classification** in `helpers.js`
4. **Improve the web interface** in `app.py`

## 📄 License

See LICENSE file for details.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review log files for errors
3. Test with simplified configuration
4. Update selectors for failing sources

---

**Happy scraping!** 🏠✨
