#!/bin/bash

echo "🚀 Starting South Florida Property Expert - PRODUCTION MODE"
echo "================================================================"
echo ""

# PRODUCTION: Set secure environment variables
export SECRET_KEY="sf-property-expert-2024-prod-$(date +%s)-${RANDOM}"
export FLASK_ENV="production"
export NODE_ENV="production"

# Ensure required directories exist
mkdir -p results logs temp_data templates

echo "📁 Created required directories"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."

# Check Python dependencies
if ! python -c "import flask, flask_socketio, pandas" 2>/dev/null; then
    echo "❌ Missing Python dependencies. Installing..."
    pip install -r requirements.txt
fi

# Check Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "❌ Missing Node.js dependencies. Installing..."
    npm install
fi

echo "✅ Dependencies verified"
echo ""

# Start services
echo "🚀 Starting services..."
echo ""

# Option to start all services or specific ones
if [ "$1" = "all" ]; then
    echo "Starting ALL services..."
    
    # Start Streamlit Dashboard in background
    echo "📊 Starting Streamlit Dashboard on port 8501..."
    streamlit run app.py --server.address 0.0.0.0 --server.port 8501 &
    STREAMLIT_PID=$!
    
    # Start Advanced Flask Chatbot in background  
    echo "🤖 Starting Advanced Chatbot on port 5000..."
    python chatbot_app.py &
    ADVANCED_PID=$!
    
    # Start Simple Flask Chatbot
    echo "🔧 Starting Simple Chatbot on port 5001..."
    python chatbot_app_simple.py &
    SIMPLE_PID=$!
    
    echo ""
    echo "✅ All services started!"
    echo "📊 Streamlit Dashboard: http://localhost:8501"
    echo "🤖 Advanced Chatbot: http://localhost:5000"
    echo "🔧 Simple Chatbot: http://localhost:5001"
    echo "🔍 Node.js Scraper: Available via command line"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Wait for interrupt
    trap "kill $STREAMLIT_PID $ADVANCED_PID $SIMPLE_PID; exit" SIGINT
    wait
    
elif [ "$1" = "chatbot" ]; then
    echo "🤖 Starting Advanced Chatbot only..."
    python chatbot_app.py
    
elif [ "$1" = "simple" ]; then
    echo "🔧 Starting Simple Chatbot only..."
    python chatbot_app_simple.py
    
elif [ "$1" = "dashboard" ]; then
    echo "📊 Starting Streamlit Dashboard only..."
    streamlit run app.py --server.address 0.0.0.0 --server.port 8501
    
else
    echo "Usage: $0 [all|chatbot|simple|dashboard]"
    echo ""
    echo "Options:"
    echo "  all        - Start all services (dashboard, chatbot, simple)"
    echo "  chatbot    - Start advanced chatbot only (port 5000)"
    echo "  simple     - Start simple chatbot only (port 5001)" 
    echo "  dashboard  - Start Streamlit dashboard only (port 8501)"
    echo ""
    echo "For client demo, recommend: $0 chatbot"
    exit 1
fi 