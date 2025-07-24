# 🚀 Client Setup Instructions

## Step 1: Fork the Repository

1. **Go to:** https://github.com/coreyalejandro/landscape_scraper
2. **Click the "Fork" button** (top-right corner)
3. **Click "Create fork"**
4. **Wait for GitHub to copy the repository**

---

## Step 2: Clone Your Fork

1. **Copy your fork's URL** from the green "Code" button
2. **Open Terminal** (Mac/Linux) or **Command Prompt** (Windows)
3. **Run this command** (replace `YOUR_USERNAME` with your GitHub username):

```bash
git clone https://github.com/YOUR_USERNAME/landscape_scraper.git
```

4. **Enter the directory:**

```bash
cd landscape_scraper
```

---

## Step 3: Install Dependencies

### Install Node.js Dependencies
```bash
npm install
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

**If you get permission errors, try:**
```bash
pip install --user -r requirements.txt
```

---

## Step 4: Launch Applications

### 🎯 **RECOMMENDED: Advanced Chatbot (Best for Demo)**

```bash
./start_production.sh chatbot
```

**Open in browser:** http://localhost:5000

**Features:**
- Real-time AI chat interface
- Integrated scraping capabilities
- Professional Socket.IO interface
- Expert property knowledge

---

### 📊 **Alternative 1: Dashboard Interface**

```bash
./start_production.sh dashboard
```

**Open in browser:** http://localhost:8501

**Features:**
- Data visualization dashboard
- Analytics and charts
- Export capabilities
- Progress monitoring

---

### 🔧 **Alternative 2: Simple Chatbot**

```bash
./start_production.sh simple
```

**Open in browser:** http://localhost:5001

**Features:**
- Lightweight chat interface
- Basic AI responses
- Simple scraper integration

---

### 🔍 **Alternative 3: Command Line Scraper**

```bash
node scraper.js
```

**Features:**
- Direct scraping without web interface
- Results saved to `results/` folder
- Fastest data collection

---

### 🚀 **Alternative 4: All Services at Once**

```bash
./start_production.sh all
```

**Access all interfaces:**
- Dashboard: http://localhost:8501
- Advanced Chat: http://localhost:5000
- Simple Chat: http://localhost:5001

---

## Step 5: Test the System

### Try These Commands in the Chatbot:

1. **"Find HOAs in Miami-Dade"** - Tests AI knowledge
2. **"Scrape property management companies in Broward"** - Tests scraping
3. **"Analyze the results"** - Tests data analysis
4. **"Export to CSV"** - Tests export functionality

---

## 📁 What You'll See

### Generated Files:
- `results/data.json` - Scraped property data
- `results/data.csv` - Spreadsheet format
- `results/summary.json` - Statistics
- `logs/scraper_log.txt` - Operation logs

---

## 🔧 Troubleshooting

### If Python commands fail:
```bash
python3 -m pip install -r requirements.txt
python3 chatbot_app.py
```

### If Node.js commands fail:
```bash
npm install --force
```

### If permissions are denied:
```bash
chmod +x start_production.sh
```

### If ports are busy:
- Close other applications using ports 5000, 5001, or 8501
- Or change ports in the Python files

---

## ✅ Success Indicators

**You'll know it's working when:**

1. ✅ **Browser opens** to the specified URL
2. ✅ **Chat interface loads** with welcome message
3. ✅ **AI responds** to your messages
4. ✅ **Scraper runs** when you request data collection
5. ✅ **Files appear** in the `results/` folder

---

## 🎯 Recommended Demo Flow

1. **Start with:** `./start_production.sh chatbot`
2. **Open:** http://localhost:5000
3. **Type:** "What can you help me with?"
4. **Then try:** "Scrape HOAs in Miami"
5. **Watch:** Real-time scraping in action
6. **Finally:** "Export the results to CSV"

**This demonstrates the full AI + scraping + analysis pipeline!**

---

## 📞 Support

If you encounter issues:
1. Check that all dependencies installed successfully
2. Ensure ports 5000, 5001, and 8501 are available
3. Try running individual components to isolate problems
4. Check log files in the `logs/` directory 