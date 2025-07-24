#!/bin/bash

echo "🤖 Starting South Florida Property Expert Chatbot..."
echo "🌐 Advanced Chatbot: http://localhost:5000"
echo "🌐 Simple Chatbot: http://localhost:5001"
echo "🌐 Streamlit Dashboard: http://localhost:8501"
echo "💡 Features: HOA & Property Management expertise, real-time scraping, market insights"
echo ""

# Ensure required directories exist
mkdir -p results logs temp_data templates

# PRODUCTION: Set environment variables
export SECRET_KEY="sf-property-expert-2024-prod-${RANDOM}"
export FLASK_ENV="production"

# Start the chatbot server (production mode)
echo "Starting ADVANCED chatbot (Flask + Socket.IO)..."
python chatbot_app.py 