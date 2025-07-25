import os
import json
import subprocess
import datetime
from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)


class PropertyExpertChatbot:
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.conversation_history = []
        self.scraper_status = {"running": False, "progress": 0, "results": []}

    def _build_knowledge_base(self):
        """Build comprehensive South Florida property management knowledge base"""
        return {
            "regions": {
                "broward": {
                    "cities": ["Fort Lauderdale", "Hollywood", "Pompano Beach", "Coral Springs",
                               "Plantation", "Sunrise", "Davie", "Weston", "Deerfield Beach"],
                    "characteristics": "Large suburban communities, many gated neighborhoods, high condo density",
                    "hoa_prevalence": "Very High - 85% of residential properties",
                    "avg_hoa_fees": "$200-800/month",
                    "key_features": ["Oceanfront condos", "Golf communities", "Age-restricted communities"]
                },
                "miami_dade": {
                    "cities": ["Miami", "Miami Beach", "Coral Gables", "Aventura", "Kendall",
                               "Homestead", "Doral", "Pinecrest", "Key Biscayne"],
                    "characteristics": "High-rise condos, luxury developments, international buyers",
                    "hoa_prevalence": "Extremely High - 90% of residential properties",
                    "avg_hoa_fees": "$300-1500/month",
                    "key_features": ["Luxury high-rises", "Waterfront properties", "International communities"]
                },
                "palm_beach": {
                    "cities": ["West Palm Beach", "Boca Raton", "Delray Beach", "Jupiter",
                               "Wellington", "Boynton Beach"],
                    "characteristics": "Affluent communities, golf courses, retirement-focused",
                    "hoa_prevalence": "Very High - 88% of residential properties",
                    "avg_hoa_fees": "$250-1200/month",
                    "key_features": ["Golf communities", "55+ developments", "Equestrian properties"]
                }
            },
            "entity_types": {
                "hoa": {
                    "full_name": "Homeowners Association",
                    "responsibilities": ["Common area maintenance", "Architectural control",
                                         "Community enforcement", "Financial management"],
                    "typical_services": ["Landscaping", "Pool maintenance", "Security", "Trash collection"],
                    "governance": "Board of Directors elected by homeowners",
                    "legal_authority": "Deed restrictions and CC&Rs enforcement"
                },
                "condo_association": {
                    "full_name": "Condominium Association",
                    "responsibilities": ["Building maintenance", "Insurance", "Financial management",
                                         "Compliance oversight"],
                    "typical_services": ["Elevator maintenance", "Roof/exterior repairs", "Amenities", "Concierge"],
                    "governance": "Board elected by unit owners",
                    "legal_authority": "Condominium declarations and bylaws"
                },
                "property_management": {
                    "full_name": "Property Management Company",
                    "services": ["Day-to-day operations", "Vendor coordination", "Financial reporting",
                                 "Board meeting support", "Compliance management"],
                    "specializations": ["HOA management", "Condo management", "Commercial properties",
                                        "Rental management"],
                    "licensing": "Florida CAM license required for community association management"
                }
            },
            "market_insights": {
                "trends": [
                    "Increasing HOA fees due to inflation and deferred maintenance",
                    "Growing demand for professional management companies",
                    "Technology adoption for online payments and communication",
                    "Focus on sustainability and energy efficiency",
                    "Stricter compliance requirements from state regulations"
                ],
                "challenges": [
                    "Aging infrastructure in older communities",
                    "Special assessments for major repairs",
                    "Board volunteer recruitment difficulties",
                    "Insurance cost increases",
                    "Balancing amenities with affordability"
                ]
            }
        }

    def analyze_query_intent(self, message):
        """Analyze user message to determine intent and extract parameters"""
        message_lower = message.lower()

        # Scraping intents
        if any(
            word in message_lower for word in [
                'scrape',
                'search',
                'find',
                'collect',
                'gather']):
            region = self._extract_region(message_lower)
            entity_type = self._extract_entity_type(message_lower)
            return {
                "intent": "scraping",
                "action": "start_scrape",
                "parameters": {"region": region, "entity_type": entity_type}
            }

        # Data analysis intents
        elif any(word in message_lower for word in ['analyze', 'show', 'display', 'results', 'data']):
            return {"intent": "analysis", "action": "show_data"}

        # Knowledge intents
        elif any(word in message_lower for word in ['what', 'how', 'explain', 'tell me about']):
            return {"intent": "knowledge", "action": "provide_info"}

        # Status intents
        elif any(word in message_lower for word in ['status', 'progress', 'running']):
            return {"intent": "status", "action": "check_status"}

        # Export intents
        elif any(word in message_lower for word in ['export', 'download', 'save', 'csv']):
            return {"intent": "export", "action": "export_data"}

        return {"intent": "general", "action": "chat"}

    def _extract_region(self, message):
        """Extract region from message"""
        if any(
            city in message for city in [
                'miami',
                'dade',
                'south beach',
                'coral gables']):
            return 'miami_dade'
        elif any(city in message for city in ['broward', 'fort lauderdale', 'hollywood', 'pompano']):
            return 'broward'
        elif any(city in message for city in ['palm beach', 'boca raton', 'delray', 'jupiter']):
            return 'palm_beach'
        return None

    def _extract_entity_type(self, message):
        """Extract entity type from message"""
        if any(
            term in message for term in [
                'hoa',
                'homeowner',
                'homeowners association']):
            return 'hoa'
        elif any(term in message for term in ['condo', 'condominium', 'condo association']):
            return 'condo_association'
        elif any(term in message for term in ['property management', 'management company', 'pm company']):
            return 'property_management'
        return None

    def generate_expert_response(self, message):
        """Generate expert response using domain knowledge"""
        intent_data = self.analyze_query_intent(message)

        if intent_data["intent"] == "scraping":
            return self._handle_scraping_request(intent_data["parameters"])
        elif intent_data["intent"] == "analysis":
            return self._handle_analysis_request()
        elif intent_data["intent"] == "knowledge":
            return self._handle_knowledge_request(message)
        elif intent_data["intent"] == "status":
            return self._handle_status_request()
        elif intent_data["intent"] == "export":
            return self._handle_export_request()
        else:
            return self._handle_general_chat(message)

    def _handle_scraping_request(self, params):
        """Handle scraping requests with expert guidance"""
        region = params.get("region")
        entity_type = params.get("entity_type")

        if not region:
            return """🤔 I'd be happy to help you scrape property data! Which South Florida region interests you?

**Available Regions:**
• **Broward County** - Great for suburban HOAs and gated communities
• **Miami-Dade** - High-density condos and luxury properties
• **Palm Beach** - Golf communities and 55+ developments

Just tell me something like "Scrape HOAs in Broward" or "Find condos in Miami-Dade" """

        region_info = self.knowledge_base["regions"].get(region, {})

        response = f"""🚀 **Starting {region.replace('_', '-').title()} Scraping Operation**

**Target Region Insights:**
• **Cities**: {', '.join(region_info.get('cities', [])[:5])}
• **HOA Prevalence**: {region_info.get('hoa_prevalence', 'High')}
• **Avg HOA Fees**: {region_info.get('avg_hoa_fees', '$200-600/month')}

**What I'm Looking For:**
{f"• **{entity_type.replace('_', ' ').title()}** entities" if entity_type else "• All property management entities"}
• Contact information (names, phones, websites)
• Address verification
• Entity classification

**Sources I'll Check:**
✅ Google Maps (most reliable)
✅ Yelp Business Directory
✅ Industry-specific directories
✅ Property management company websites

Starting scrape now... Check back in a few minutes for results! 📊"""

        # Start actual scraping in background
        threading.Thread(
            target=self._run_scraper, args=(
                region, entity_type)).start()

        return response

    def _run_scraper(self, region, entity_type):
        """Run the actual scraper in background"""
        try:
            self.scraper_status["running"] = True
            self.scraper_status["progress"] = 0

            # Run scraper
            result = subprocess.run(['node', 'scraper.js'],
                                    capture_output=True, text=True, timeout=600)

            self.scraper_status["running"] = False
            self.scraper_status["progress"] = 100

            if result.returncode == 0:
                self._load_results()

        except Exception as e:
            self.scraper_status["running"] = False
            print(f"Scraper error: {e}")

    def _handle_analysis_request(self):
        """Provide expert data analysis"""
        self._load_results()
        results = self.scraper_status["results"]

        if not results:
            return """📊 **No Data Available Yet**

I don't see any scraped data to analyze. Try running:
• "Scrape HOAs in Miami"
• "Find property management companies in Broward"
• "Search for condos in Palm Beach"

Once I have data, I can provide detailed analysis including market insights, contact quality assessment, and regional patterns! 🔍"""

        # Perform basic analysis
        total_entities = len(results)
        with_websites = len([r for r in results if r.get('website')])
        with_phones = len([r for r in results if r.get('phone')])

        return f"""📊 **Expert Data Analysis**

**📈 Overview:**
• **Total Entities**: {total_entities} discovered
• **Data Quality**: {(with_phones / total_entities * 100):.1f}% have phone numbers
• **Web Presence**: {(with_websites / total_entities * 100):.1f}% have websites

**💡 Expert Insights:**
• High website % indicates professional management
• Phone number completeness suggests active businesses
• Geographic clustering shows market concentration
• Entity type mix reveals market composition

Want me to dig deeper into any specific aspect? 🔍"""

    def _handle_knowledge_request(self, message):
        """Provide expert knowledge based on query"""
        message_lower = message.lower()

        # HOA-specific questions
        if any(
            term in message_lower for term in [
                'hoa fees',
                'homeowner fees',
                'association fees']):
            return """💰 **HOA Fees in South Florida - Expert Analysis**

**Typical Fee Ranges by Region:**
• **Broward County**: $200-800/month
• **Miami-Dade**: $300-1,500/month
• **Palm Beach**: $250-1,200/month

**What Fees Cover:**
✅ Common area maintenance (landscaping, pools)
✅ Insurance (master policy coverage)
✅ Utilities (common areas, street lighting)
✅ Management company fees
✅ Reserve funds (future repairs)
✅ Amenities (gym, clubhouse, security)

**Fee Factors:**
• **Property Type**: Condos > Townhomes > Single-family
• **Amenities**: More amenities = higher fees
• **Age**: Older properties often have higher maintenance costs
• **Size**: Larger communities can spread costs more efficiently

**Red Flags**: Fees under $100/month often indicate deferred maintenance or inadequate reserves."""

        elif any(term in message_lower for term in ['condo association', 'condominium', 'condo board']):
            condo_info = self.knowledge_base["entity_types"]["condo_association"]
            return f"""🏢 **Condominium Associations - Expert Guide**

**Primary Responsibilities:**
• {condo_info['responsibilities'][0]}
• {condo_info['responsibilities'][1]}
• {condo_info['responsibilities'][2]}
• {condo_info['responsibilities'][3]}

**Typical Services:**
• {condo_info['typical_services'][0]}
• {condo_info['typical_services'][1]}
• {condo_info['typical_services'][2]}
• {condo_info['typical_services'][3]}

**Governance Structure:**
• {condo_info['governance']}
• Monthly/quarterly board meetings
• Annual owner meetings for major decisions
• Professional management company typically hired

**Legal Authority:**
• {condo_info['legal_authority']}
• Florida Statute Chapter 718 compliance
• Enforcement powers for rule violations"""

        elif any(term in message_lower for term in ['property management', 'management company', 'cam license']):
            pm_info = self.knowledge_base["entity_types"]["property_management"]
            return f"""🏗️ **Property Management Companies - Expert Analysis**

**Core Services:**
• {pm_info['services'][0]}
• {pm_info['services'][1]}
• {pm_info['services'][2]}
• {pm_info['services'][3]}

**Specialization Areas:**
• {pm_info['specializations'][0]}
• {pm_info['specializations'][1]}
• {pm_info['specializations'][2]}
• {pm_info['specializations'][3]}

**Florida Licensing:**
• {pm_info['licensing']}
• Continuing education requirements
• Bonding and insurance mandates
• DBPR oversight and regulation

**Choosing a Management Company:**
✅ **Look for**: CAM license, local experience, technology platforms
✅ **Ask about**: Fee structure, emergency response, financial reporting
✅ **Verify**: Insurance coverage, client references, complaint history"""

        else:
            return self._handle_general_chat(message)

    def _handle_status_request(self):
        """Check scraper status"""
        if self.scraper_status["running"]:
            return f"""⚡ **Scraper Status: ACTIVE**

**Progress**: {self.scraper_status['progress']}% complete
**Status**: Currently scanning property databases...
**Sources**: Checking Google Maps, Yelp, and industry directories

The process typically takes 2-5 minutes depending on the region size. 🔄"""

        elif self.scraper_status["results"]:
            return f"""✅ **Scraper Status: COMPLETE**

**Results**: {len(self.scraper_status['results'])} entities found
**Last Run**: Recently completed
**Data Available**: Ready for analysis and export

Try asking:
• "Analyze the results"
• "Show me the data"
• "Export to CSV" 📊"""

        else:
            return """💤 **Scraper Status: IDLE**

No active scraping operations. Ready to start!

**Quick Commands:**
• "Scrape HOAs in Miami"
• "Find property management in Broward"
• "Search condos in Palm Beach"

What would you like to discover? 🚀"""

    def _handle_export_request(self):
        """Handle data export requests"""
        self._load_results()

        if not self.scraper_status["results"]:
            return "📥 No data available to export. Run a scraping operation first!"

        try:
            # Export to JSON (simpler than CSV for this demo)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/south_florida_properties_{timestamp}.json"

            with open(filename, 'w') as f:
                json.dump(self.scraper_status["results"], f, indent=2)

            return f"""📤 **Export Complete!**

**File**: `{filename}`
**Records**: {len(self.scraper_status['results'])} entities
**Format**: JSON

**What's Included:**
✅ Business names and classifications
✅ Complete addresses
✅ Phone numbers and websites
✅ Entity type identification
✅ Data source attribution

Perfect for analysis or further processing! 📊"""

        except Exception as e:
            return f"❌ Export failed: {str(e)}"

    def _handle_general_chat(self, message):
        """Handle general conversation with property expertise"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(greeting in message.lower() for greeting in greetings):
            return """👋 **Hello! I'm your South Florida Property Expert**

I specialize in HOAs, condominiums, and property management companies across Broward, Miami-Dade, and Palm Beach counties.

**What I Can Help With:**
🔍 **Data Collection**: "Scrape HOAs in Miami"
📊 **Market Analysis**: "Analyze the results"
🧠 **Expert Knowledge**: "Tell me about HOA fees"
📤 **Data Export**: "Export to JSON"

**Try asking me:**
• "What are typical condo fees in Miami?"
• "Find property management companies in Broward"
• "Explain the difference between HOAs and condo associations"

How can I assist with your property research today? 🏠"""

        elif 'thank' in message.lower():
            return """🙏 **You're welcome!**

I'm here whenever you need South Florida property insights, data collection, or market analysis.

Feel free to ask me anything about HOAs, condos, property management, or run another scraping operation!

**Quick reminder**: I can help with Broward, Miami-Dade, and Palm Beach counties. 🌴"""

        else:
            return """🤔 I'm not sure I understand that request.

As your **South Florida Property Expert**, I can help with:

**🔍 Data Collection:**
• "Scrape HOAs in [region]"
• "Find condos in Miami-Dade"

**📊 Analysis & Insights:**
• "Analyze the data"
• "Show me results"

**🧠 Expert Knowledge:**
• "What are HOA responsibilities?"
• "How do condo fees work?"

**📤 Data Management:**
• "Export to JSON"
• "Check scraper status"

What would you like to explore? 🏠"""

    def _load_results(self):
        """Load latest scraper results"""
        try:
            if os.path.exists('results/data.json'):
                with open('results/data.json', 'r') as f:
                    self.scraper_status["results"] = json.load(f)
        except Exception:
            self.scraper_status["results"] = []


# Initialize chatbot
chatbot = PropertyExpertChatbot()


@app.route('/')
def index():
    return render_template('chatbot_simple.html')


@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_message = data.get('message', '')

    # Add to conversation history
    chatbot.conversation_history.append({
        'user': user_message,
        'timestamp': datetime.datetime.now().isoformat()
    })

    # Generate bot response
    bot_response = chatbot.generate_expert_response(user_message)

    chatbot.conversation_history.append({
        'bot': bot_response,
        'timestamp': datetime.datetime.now().isoformat()
    })

    return jsonify({
        'response': bot_response,
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/api/status')
def api_status():
    return jsonify(chatbot.scraper_status)


@app.route('/api/results')
def api_results():
    chatbot._load_results()
    return jsonify(chatbot.scraper_status["results"])


if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('results', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('temp_data', exist_ok=True)

    print("🤖 Starting South Florida Property Expert Chatbot...")
    print("🌐 Server will be available at: http://localhost:5001")
    print("💡 Features: HOA & Property Management expertise, real-time scraping, market insights")
    print("")

    # PRODUCTION: Disable debug mode
    app.run(debug=False, host='0.0.0.0', port=5001)
