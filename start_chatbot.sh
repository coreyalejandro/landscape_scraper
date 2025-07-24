#!/bin/bash

echo "🤖 Starting South Florida Property Expert Chatbot..."
echo "🌐 Server will be available at: http://localhost:5000"
echo "💡 Features: HOA & Property Management expertise, real-time scraping, market insights"
echo ""

# Ensure required directories exist
mkdir -p results logs temp_data templates

# Start the chatbot server
python chatbot_app.py 