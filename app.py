import streamlit as st
import requests
import json
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Topic Generator",
    layout="wide"
)

# --- UI Display ---
st.title("Topic Generator")
st.markdown("""
This AI tool generates topic ideas based on the marketing funnel concepts from 
[SEMRush](https://www.semrush.com/blog/content-marketing-funnel/) and 
[Search Engine Land](https://searchengineland.com/how-to-drive-the-funnel-through-content-marketing-and-link-building-374343), 
tailored to the client details provided.
""")

with st.expander("How to Use This Tool"):
    st.markdown("""
    **This document provides a step-by-step guide on how to effectively use the Topic Generator tool to create strategic guest post topics for link-building outreach.**

    **1. Understand the Tool's Purpose**
    The Topic Generator is an AI-powered tool designed to produce relevant, high-quality topic ideas. It analyzes client information and aligns suggestions with the marketing funnel stages:
    - **Top of the Funnel (ToFu):** Building awareness.
    - **Middle of the Funnel (MoFu):** Encouraging consideration.
    - **Bottom of the Funnel (BoFu):** Driving decisions.
    
    The methodology is based on content strategy principles from leading industry resources like SEMRush and Search Engine Land.

    **2. Provide Client Details**
    The tool works by analyzing text to understand the client's needs. For the best results, follow this primary step:
    - **Paste Full Guidelines into Field 5:** The most effective way to use the generator is to paste the client's complete copywriting guidelines or any other detailed brand document into the text box labeled **"5. Full Copywriting Guidelines / Additional Context."** The AI will analyze this entire document to extract the industry, tone, audiences, and products.
    
    The other fields (1-4) are optional and can be used to add specific details or clarify information if the main document in field 5 is incomplete.

    **3. Generate the Topics**
    Once the client information is entered, click the **"Generate Topics"** button. A loader will appear while the AI processes the request. This may take a few moments.

    **4. Review the Output**
    The generated topics are organized into two main sections:
    - **Section 1: Product/Service Topics:** This section contains ideas directly related to the client's offerings that were identified from the provided text.
    - **Section 2: Timely & Event-Based Topics:** This section provides ideas relevant to the current date, including upcoming holidays, seasons, or important industry events.
    
    Each section follows a clear structure:
    - **Main Subject:** Starts with the specific Product, Service, or Event.
    - **Marketing Funnel:** Topics are grouped under ToFu, MoFu, or BoFu.
    - **Target Audience:** Specifies the audience persona the topics are for.
    - **Target Publication:** Suggests the niche or type of publication where the topic would fit.
    - **Topics:** Lists at least three topic ideas, each with a title and a short rationale.

    **Tips for Best Results**
    - **Prioritize Field 5:** Always try to use a comprehensive document in the main guidelines field for the most context-aware suggestions.
    - **Check for Specificity:** If the generated topics seem too general, add more specific details to the optional fields to help guide the AI.
    - **Use as a Starting Point:** The generated ideas are a strong starting point. They should be reviewed by a strategist to ensure perfect alignment with the client's goals before outreach.
    """)

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter Google API Key", type="password", help="Your key is not stored. It is used only for this session.")
st.sidebar.markdown("Refer to the `how-to-get-api-key.md` guide for instructions on getting a key.")
st.sidebar.divider()

st.sidebar.header("Client Details")
st.sidebar.info("Fill out the fields below. For the most accurate results, paste the full copywriting guidelines into field 5.")

industry = st.sidebar.text_input("1. Client Industry/Niche (Optional)", placeholder="e.g., B2B SaaS for project management")
tone = st.sidebar.text_input("2. Branding Tone/Voice (Optional)", placeholder="e.g., Authoritative, yet approachable")
audience_input = st.sidebar.text_area("3. Target Audience (Optional)", placeholder="e.g., Marketing managers in tech startups, Freelance project managers")
product_input = st.sidebar.text_area("4. Product/Service to Highlight (Optional)", placeholder="e.g., https://my-saas.com/ai-feature OR Annual conference")
guidelines = st.sidebar.text_area("5. Full Copywriting Guidelines / Additional Context", placeholder="Paste the full copywriting guidelines document here...")

generate_btn = st.sidebar.button("Generate Topics", type="primary")

# --- Functions for API Call and Display ---

def fetch_with_retry(url, options, retries=3):
    """Simple retry logic for the API call."""
    for i in range(retries):
        try:
            response = requests.post(url, headers=options['headers'], data=options['body'])
            # Don't retry on 4xx client errors like 403 Forbidden
            if response.status_code < 500:
                return response
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                st.error(f"Request failed after {retries} retries: {e}")
                return None
    st.error(f"API request failed with status code: {response.status_code}")
    return response # Return the failed response to inspect the status code

def create_topic_group(group_name, funnels, group_label):
    """Renders a single group of topics (for a product or event)."""
    st.header(f"{group_label}: {group_name}", divider="gray")
    
    funnel_map = {
        "ToFu": ("ToFu (Awareness)", "blue"),
        "MoFu": ("MoFu (Consideration)", "green"),
        "BoFu": ("BoFu (Decision)", "red")
    }
    stage_order = { 'ToFu': 1, 'MoFu': 2, 'BoFu': 3 }
    
    sorted_funnels = sorted(funnels, key=lambda f: stage_order.get(f.get('funnelStage', ''), 0))

    for funnel in sorted_funnels:
        stage = funnel.get('funnelStage')
        if stage in funnel_map:
            name, color = funnel_map[stage]
            with st.container(border=True):
                st.subheader(f":{color}[{name}]")
                for audience in funnel.get('audiences', []):
                    st.markdown(f"**Target Audience:** {audience.get('audienceName', 'N/A')}")
                    for pub in audience.get('publications', []):
                        with st.expander(f"Publication Niche: {pub.get('publicationNiche', 'N/A')}"):
                            for topic in pub.get('topics', []):
                                st.markdown(f"**Title:** {topic.get('title', 'No Title')}")
                                st.caption(f"Rationale: {topic.get('rationale', 'No Rationale')}")
                                st.markdown("---")


# --- Main Logic ---
if generate_btn:
    # Prioritize user-input key, fall back to secrets for deployed apps
    api_key = api_key_input or st.secrets.get("GOOGLE_API_KEY")

    if not api_key:
        st.error("Google API Key not found. Please enter it in the sidebar or add it to your Streamlit secrets for deployed apps.")
    elif not guidelines:
        st.sidebar.error("Please paste the copywriting guidelines into field 5 for analysis.")
    else:
        with st.spinner("Generating topics... Please wait."):
            current_date = datetime.now().strftime('%B %d, %Y')
            
            system_prompt = """You are a strategic content and marketing analyst. Your task is to generate two distinct sets of guest post topics based on the provided client guidelines and the current date. The topic generation must be guided by the marketing funnel principles (ToFu, MoFu, BoFu).

            First, analyze the 'Full Copywriting Guidelines' to extract the client's industry, tone, target audiences, and products/services. Use the optional fields (1-4) to supplement or clarify this information if provided.

            Second, generate two sets of topics:
            1.  **Product-Based Topics:** Ideas directly related to the client's products/services you identified.
            2.  **Timely & Event-Based Topics:** Based on the 'Current Date' and the client's industry, identify relevant upcoming holidays, industry events, or seasonal business milestones and create topics for them.

            The final output must be a single JSON object with two top-level keys: `productBasedTopics` and `timelyTopics`, adhering to the provided schema. For each topic, create a title and rationale."""

            user_query = f"Current Date: {current_date}\n\nFull Copywriting Guidelines:\n---\n{guidelines}\n---\n"
            
            optional_inputs = {
                "Specific Industry/Niche": industry,
                "Specific Branding Tone/Voice": tone,
                "Specific Target Audiences": audience_input,
                "Specific Products/Services": product_input
            }

            optional_details = "\n".join([f"- {key}: {value}" for key, value in optional_inputs.items() if value])
            if optional_details:
                user_query += f"\nSupplemental Details from Optional Fields:\n{optional_details}"

            schema = {
                "type": "OBJECT",
                "properties": {
                    "productBasedTopics": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT", "properties": {"productName": {"type": "STRING"}, "funnels": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"funnelStage": {"type": "STRING", "enum": ["ToFu", "MoFu", "BoFu"]}, "audiences": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"audienceName": {"type": "STRING"}, "publications": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"publicationNiche": {"type": "STRING"}, "topics": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"title": {"type": "STRING"}, "rationale": {"type": "STRING"}}, "required": ["title", "rationale"]}}}, "required": ["publicationNiche", "topics"]}}}, "required": ["audienceName", "publications"]}}}, "required": ["funnelStage", "audiences"]}}}
                        }
                    },
                    "timelyTopics": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT", "properties": {"eventName": {"type": "STRING"}, "funnels": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"funnelStage": {"type": "STRING", "enum": ["ToFu", "MoFu", "BoFu"]}, "audiences": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"audienceName": {"type": "STRING"}, "publications": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"publicationNiche": {"type": "STRING"}, "topics": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"title": {"type": "STRING"}, "rationale": {"type": "STRING"}}, "required": ["title", "rationale"]}}}, "required": ["publicationNiche", "topics"]}}}, "required": ["audienceName", "publications"]}}}, "required": ["funnelStage", "audiences"]}}}
                        }
                    }
                },
                "required": ["productBasedTopics", "timelyTopics"]
            }

            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

            payload = {
                "contents": [{"parts": [{"text": user_query}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}
            }
            
            options = {
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(payload)
            }
            
            response = fetch_with_retry(api_url, options)
            
            if response and response.status_code == 200:
                try:
                    result = response.json()
                    text_content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    
                    if text_content:
                        data = json.loads(text_content)
                        st.header("Generated Topics", divider="rainbow")
                        
                        if data.get("productBasedTopics"):
                            st.subheader("1. Product/Service Topics")
                            for product_data in data["productBasedTopics"]:
                                create_topic_group(product_data.get('productName'), product_data.get('funnels', []), 'Product/Service')
                        
                        if data.get("timelyTopics"):
                            st.subheader("2. Timely & Event-Based Topics")
                            for event_data in data["timelyTopics"]:
                                create_topic_group(event_data.get('eventName'), event_data.get('funnels', []), 'Event/Holiday')
                    else:
                        st.error("No content received from the API. The model may not have been able to generate a valid response.")
                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    st.error(f"Failed to parse the API response. Please try again. Error: {e}")
            elif response:
                 st.error(f"API request failed with status code: {response.status_code}. This may be an issue with the API key or permissions.")
            else:
                 st.error("The request to the AI model failed. Please check the details and try again.")

