import streamlit as st
import requests
import json
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Topic Generator",
    layout="wide"
)

# Hide Streamlit's default menu and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


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

    **4. Review and Understand the Output**
    The generated topics are organized into two main sections:
    - **Section 1: Product/Service Topics:** Contains ideas directly related to the client's offerings.
    - **Section 2: Timely & Event-Based Topics:** Provides ideas relevant to the current date, including upcoming holidays, seasons, or important industry events.
    
    Each section follows a clear structure:
    - **Main Subject:** The specific Product, Service, or Event.
    - **Marketing Funnel:** Topics are grouped under ToFu, MoFu, or BoFu.
    - **Target Audience:** The audience persona the topics are for.
    - **Target Publication:** The suggested niche for guest posting.
    
    Within each publication niche, there will be at least three topic suggestions, each with three parts:
    - **Topic:** A short, concise title (max 60 characters) designed for quick pitches. It frames the product as a solution.
    - **Suggested Headline:** A longer, more engaging headline ready for an article.
    - **Rationale:** A brief explanation of why the topic is valuable and relevant to the target audience.

    **Tips for Best Results**
    - **Prioritize Field 5:** Always try to use a comprehensive document in the main guidelines field for the most context-aware suggestions.
    - **Check for Specificity:** If the generated topics seem too general, add more specific details to the optional fields to help guide the AI.
    - **Use as a Starting Point:** The generated ideas are a strong starting point. They should be reviewed by a strategist to ensure perfect alignment with the client's goals before outreach.
    """)

with st.expander("How to Get a Google AI API Key"):
    st.markdown("""
    Follow these steps to generate a free API key from Google AI Studio, which is required to run the Topic Generator.

    **1. Visit Google AI Studio**
    - Open a web browser and go to the Google AI Studio website: [aistudio.google.com](https://aistudio.google.com)

    **2. Get API Key**
    - Sign in with a Google account.
    - Once logged in, click on the **"Get API key"** option on the left-hand menu.

    **3. Create API Key**
    - If this is the first time creating a key, a prompt will appear to create a new project. Name the project `topic-generation-tool-[Name]` (replacing `[Name]` with the user's name or initials) and continue.
    - Click the **"Create API key in new project"** button.
    - The new key will appear in the list on https://aistudio.google.com/api-keys.

    **4. Copy and Use the Key**
    - Find the new key in the list and click the copy icon next to the long string of letters and numbers to copy it to the clipboard.
    - Paste this key into the **"Enter Google API Key"** field in the Topic Generator's sidebar.
    """)

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter Google API Key", type="password", help="Get a key using the instructions in the main panel.")
st.sidebar.divider()

st.sidebar.header("Client Details")
st.sidebar.info("Fill out field 5 OR fields 1-4 for the best results.")

industry = st.sidebar.text_input("1. Client Industry/Niche (Optional)", placeholder="e.g., B2B SaaS for project management")
tone = st.sidebar.text_input("2. Branding Tone/Voice (Optional)", placeholder="e.g., Authoritative, yet approachable")
audience_input = st.sidebar.text_area("3. Target Audience (Optional)", placeholder="e.g., Marketing managers in tech startups, Freelance project managers")
product_input = st.sidebar.text_area("4. Product/Service to Highlight (Optional)", placeholder="e.g., https://my-saas.com/ai-feature OR Annual conference")
guidelines = st.sidebar.text_area("5. Full Copywriting Guidelines / Additional Context", placeholder="Paste the full copywriting guidelines document here...")

generate_btn = st.sidebar.button("Generate Topics", type="primary")

# --- Functions for API Call and Display ---

def fetch_with_retry(url, options, retries=3):
    """Retry logic for the API call with a timeout. Returns (response, error_message)."""
    for i in range(retries):
        try:
            response = requests.post(url, headers=options['headers'], data=options['body'], timeout=60)
            if response.status_code < 500:  # Success or client error
                return response, None
            # If server error (>=500), the loop will continue and retry
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                # Last retry failed, return the error
                error_msg = f"A network error occurred after multiple retries: {e}. This might be a temporary issue with the connection. Please try again in a few moments."
                return None, error_msg
    # This part is reached if all retries on a 5xx error fail
    error_msg = f"The server responded with an error (Status {response.status_code}) after multiple retries. Please try again later."
    return None, error_msg


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
                                st.markdown(f"**Topic:** {topic.get('topic', 'No Topic')}")
                                st.markdown(f"**Suggested Headline:** {topic.get('suggestedHeadline', 'No Headline')}")
                                st.caption(f"Rationale: {topic.get('rationale', 'No Rationale')}")
                                st.markdown("---")


# --- Main Logic ---
if generate_btn:
    api_key = api_key_input or st.secrets.get("GOOGLE_API_KEY")

    if not api_key:
        st.error("Google API Key not found. Please enter it in the sidebar or add it to your Streamlit secrets for deployed apps.")
    else:
        has_guidelines = bool(guidelines)
        has_other_details = bool(industry or tone or audience_input or product_input)

        if not has_guidelines and not has_other_details:
            st.sidebar.error("Please provide client details in field 5, or in fields 1-4.")
        else:
            with st.spinner("Generating topics... This may take up to a minute."):
                current_date = datetime.now().strftime('%B %d, %Y')
                
                system_prompt = """You are a strategic content and marketing analyst. Your task is to generate two distinct sets of guest post topics based on the provided client details and the current date. The topic generation must be guided by the marketing funnel principles (ToFu, MoFu, BoFu).

                First, analyze the provided text (which may be copywriting guidelines or a collection of details) to extract the client's industry, tone, target audiences, and products/services. When you identify a product, service, or event, summarize it into a short, clear name (e.g., "AI Security Solution" or "Annual Tech Conference") for the `productName` or `eventName` field. Do not use the entire descriptive text from the input.

                Second, generate two sets of topics ensuring there are at least 3 topics per funnel stage for each audience and product/event:
                1.  **Product-Based Topics:** Ideas directly related to the client's products/services.
                2.  **Timely & Event-Based Topics:** Based on the 'Current Date' and the client's industry, identify relevant upcoming holidays, industry events, or seasonal business milestones and create topics for them.

                For each generated topic, you must provide three elements:
                - 'topic': A short, concise title (MAXIMUM 60 characters) that frames the product/service as a solution to a problem relevant to the funnel stage.
                - 'suggestedHeadline': A longer, more engaging headline suitable for a full article.
                - 'rationale': A brief explanation of the topic's value and relevance.
                
                The final output must be a single JSON object with two top-level keys: `productBasedTopics` and `timelyTopics`, adhering to the provided schema.
                """

                user_query = f"Current Date: {current_date}\n\n"

                if has_guidelines:
                    user_query += f"Full Copywriting Guidelines:\n---\n{guidelines}\n---\n"
                    # Add supplemental details if they exist
                    optional_inputs = {
                        "Specific Industry/Niche": industry,
                        "Specific Branding Tone/Voice": tone,
                        "Specific Target Audiences": audience_input,
                        "Specific Products/Services": product_input
                    }
                    optional_details = "\n".join([f"- {key}: {value}" for key, value in optional_inputs.items() if value])
                    if optional_details:
                        user_query += f"\nSupplemental Details from Optional Fields:\n{optional_details}"
                else: # No guidelines, use the other fields as the primary source
                    user_query += "Client Details:\n"
                    primary_inputs = {
                        "Industry/Niche": industry,
                        "Branding Tone/Voice": tone,
                        "Target Audiences": audience_input,
                        "Products/Services to Highlight": product_input
                    }
                    primary_details = "\n".join([f"- {key}: {value}" for key, value in primary_inputs.items() if value])
                    user_query += primary_details


                schema = {
                    "type": "OBJECT",
                    "properties": {
                        "productBasedTopics": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "productName": {
                                        "type": "STRING",
                                        "description": "A short, summarized name for the product/service (e.g., 'AI Security Solution'). Do not use the full descriptive text from the input."
                                    },
                                    "funnels": {
                                        "type": "ARRAY",
                                        "items": {
                                            "type": "OBJECT",
                                            "properties": {
                                                "funnelStage": {"type": "STRING", "enum": ["ToFu", "MoFu", "BoFu"]},
                                                "audiences": {
                                                    "type": "ARRAY",
                                                    "items": {
                                                        "type": "OBJECT",
                                                        "properties": {
                                                            "audienceName": {"type": "STRING"},
                                                            "publications": {
                                                                "type": "ARRAY",
                                                                "items": {
                                                                    "type": "OBJECT",
                                                                    "properties": {
                                                                        "publicationNiche": {"type": "STRING"},
                                                                        "topics": {
                                                                            "type": "ARRAY",
                                                                            "items": {
                                                                                "type": "OBJECT",
                                                                                "properties": {
                                                                                    "topic": {"type": "STRING"},
                                                                                    "suggestedHeadline": {"type": "STRING"},
                                                                                    "rationale": {"type": "STRING"}
                                                                                },
                                                                                "required": ["topic", "suggestedHeadline", "rationale"]
                                                                            }
                                                                        }
                                                                    },
                                                                    "required": ["publicationNiche", "topics"]
                                                                }
                                                            }
                                                        },
                                                        "required": ["audienceName", "publications"]
                                                    }
                                                }
                                            },
                                            "required": ["funnelStage", "audiences"]
                                        }
                                    }
                                },
                                "required": ["productName", "funnels"]
                            }
                        },
                        "timelyTopics": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "eventName": {
                                        "type": "STRING",
                                        "description": "A short, summarized name for the event or holiday (e.g., 'Q4 Sales Kickoff' or 'Cyber Monday')."
                                    },
                                    "funnels": {
                                        "type": "ARRAY",
                                        "items": {
                                            "type": "OBJECT",
                                            "properties": {
                                                "funnelStage": {"type": "STRING", "enum": ["ToFu", "MoFu", "BoFu"]},
                                                "audiences": {
                                                    "type": "ARRAY",
                                                    "items": {
                                                        "type": "OBJECT",
                                                        "properties": {
                                                            "audienceName": {"type": "STRING"},
                                                            "publications": {
                                                                "type": "ARRAY",
                                                                "items": {
                                                                    "type": "OBJECT",
                                                                    "properties": {
                                                                        "publicationNiche": {"type": "STRING"},
                                                                        "topics": {
                                                                            "type": "ARRAY",
                                                                            "items": {
                                                                                "type": "OBJECT",
                                                                                "properties": {
                                                                                    "topic": {"type": "STRING"},
                                                                                    "suggestedHeadline": {"type": "STRING"},
                                                                                    "rationale": {"type": "STRING"}
                                                                                },
                                                                                "required": ["topic", "suggestedHeadline", "rationale"]
                                                                            }
                                                                        }
                                                                    },
                                                                    "required": ["publicationNiche", "topics"]
                                                                }
                                                            }
                                                        },
                                                        "required": ["audienceName", "publications"]
                                                    }
                                                }
                                            },
                                            "required": ["funnelStage", "audiences"]
                                        }
                                    }
                                },
                                "required": ["eventName", "funnels"]
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
                
                response, error_msg = fetch_with_retry(api_url, options)

                if error_msg:
                    st.error(error_msg)
                elif response and response.status_code == 200:
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
                     # Display the detailed error message from the API
                     try:
                         error_details = response.json()
                         st.error(f"API request failed with status code: {response.status_code}.")
                         st.json(error_details)
                     except json.JSONDecodeError:
                         st.error(f"API request failed with status code: {response.status_code} and could not parse the error response.")

