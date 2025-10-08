import streamlit as st
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Topic Generator",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .status-tag {
            display: inline-block;
            padding: 0.3em 0.8em;
            margin: 0.2em;
            font-size: 0.9em;
            font-weight: bold;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            color: white;
        }
        .tag-red {
            background-color: #D32F2F; /* Red */
        }
        .tag-green {
            background-color: #388E3C; /* Green */
        }
        
        /* CSS for the green button when ready */
        div.stButton > button.ready {
            background-color: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }
        div.stButton > button.ready:hover {
            background-color: #45a049;
            color: white;
            border-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)


# --- UI Display ---
st.markdown("<h1 style='background-color: #FFF9C4; padding: 10px; border-radius: 10px;'>Topic Generator</h1>", unsafe_allow_html=True)
st.markdown("""
This AI tool generates topic ideas based on the marketing funnel concepts from 
[SEMRush](https://www.semrush.com/blog/content-marketing-funnel/) and 
[Search Engine Land](https://searchengineland.com/how-to-drive-the-funnel-through-content-marketing-and-link-building-374343), 
tailored to the business details provided.
""")

with st.expander("How to Start"):
    st.markdown("""
    **Option 1: Analyze a Website (Recommended)**
    1.  Enter a business's website URL in the sidebar.
    2.  Click "Analyze Website".
    3.  The tool will auto-fill the business details for you.

    **Option 2: Enter Details Manually**
    - Skip the website analysis and fill in the business details in the sidebar directly. Use field 5 for complete guidelines.
    """)


with st.expander("How to Use This Tool"):
    st.markdown("""
    **This document provides a step-by-step guide on how to effectively use the Topic Generator tool to create strategic guest post topics for link-building outreach.**

    **1. Understand the Tool's Purpose**
    The Topic Generator is an AI-powered tool designed to produce relevant, high-quality topic ideas. It analyzes business information and aligns suggestions with the marketing funnel stages:
    - **Top of the Funnel (ToFu):** Building awareness.
    - **Middle of the Funnel (MoFu):** Encouraging consideration.
    - **Bottom of the Funnel (BoFu):** Driving decisions.

    The methodology is based on content strategy principles from leading industry resources like SEMRush and Search Engine Land.

    **2. Provide Business Details**
    The tool works by analyzing text to understand the business's needs. For the best results, follow this primary step:
    - **Paste Full Guidelines into Field 5:** The most effective way to use the generator is to paste the business's complete copywriting guidelines or any other detailed brand document into the text box labeled **"5. Full Copywriting Guidelines / Additional Context."** The AI will analyze this entire document to extract the industry, tone, audiences, and products.

    The other fields (1-4) are optional and can be used to add specific details or clarify information if the main document in field 5 is incomplete.

    **3. Generate the Topics**
    Once the business information is entered, click the **"Generate Topics"** button. A loader will appear while the AI processes the request. This may take a few moments.

    **4. Review and Understand the Output**
    The generated topics are organized into two main sections:
    - **Section 1: Product/Service Topics:** Contains ideas directly related to the business's offerings.
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
    - **Use as a Starting Point:** The generated ideas are a strong starting point. They should be reviewed by a strategist to ensure perfect alignment with the business's goals before outreach.
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

# --- Initialize Session State ---
if 'api_key' not in st.session_state: st.session_state.api_key = ""
if 'industry' not in st.session_state: st.session_state.industry = ""
if 'tone' not in st.session_state: st.session_state.tone = ""
if 'audience_input' not in st.session_state: st.session_state.audience_input = ""
if 'product_input' not in st.session_state: st.session_state.product_input = ""
if 'guidelines' not in st.session_state: st.session_state.guidelines = ""
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = None
if 'analyzed_url' not in st.session_state: st.session_state.analyzed_url = ""
if 'generated_data' not in st.session_state: st.session_state.generated_data = None
if 'analyze_btn_clicked' not in st.session_state: st.session_state.analyze_btn_clicked = False
if 'dataframe' not in st.session_state: st.session_state.dataframe = pd.DataFrame()


# --- Functions ---

def validate_api_key(api_key):
    """Checks if the API key is valid by making a simple request."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def scrape_website(url):
    """Scrapes the text content from a given URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator='\n', strip=True)
        return text[:15000], None
    except requests.RequestException as e:
        return None, f"Failed to fetch website content: {e}"

def analyze_scraped_text(api_key, text):
    """Uses AI to analyze scraped text and extract business details."""
    system_prompt = """You are an expert marketing analyst. Analyze the provided website text and extract the following information. Be concise and summarize the findings. If information isn't present, state 'Not found'.
    - **Target Audience and Pain Points:** The specific groups of people the business wants to reach and the problems they face.
    - **Business Services and/or Products:** The specific offerings that solve the audience's pain points.
    - **Target Location:** The primary geographical market (e.g., USA, California, Global).
    - **Industry/Niche:** The specific market the business operates in.
    - **Branding Tone/Voice:** The style and personality of the business's communication.
    - **Branding Guidelines Summary:** Summarize any core messaging or branding principles evident from the text."""
    
    schema = {
        "type": "OBJECT",
        "properties": {
            "target_audience_pain_points": {"type": "STRING"},
            "services_and_products": {"type": "STRING"},
            "target_location": {"type": "STRING"},
            "industry": {"type": "STRING"},
            "tone": {"type": "STRING"},
            "guidelines": {"type": "STRING"}
        },
        "required": ["target_audience_pain_points", "services_and_products", "target_location", "industry", "tone", "guidelines"]
    }
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}
    }
    options = {'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(payload)}
    
    response, error = fetch_with_retry(api_url, options)

    if error:
        return None, error
    if response.status_code == 200:
        try:
            result = response.json()
            analysis = json.loads(result['candidates'][0]['content']['parts'][0]['text'])
            return analysis, None
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            return None, f"Failed to parse analysis from AI: {e}"
    else:
        try:
            error_details = response.json()
            return None, f"AI analysis failed with status {response.status_code}: {json.dumps(error_details)}"
        except json.JSONDecodeError:
            return None, f"AI analysis failed with status {response.status_code}: {response.text}"


def fetch_with_retry(url, options, retries=3):
    """Retry logic for the API call with a timeout. Returns (response, error_message)."""
    for i in range(retries):
        try:
            response = requests.post(url, headers=options['headers'], data=options['body'], timeout=60)
            if response.status_code < 500:
                return response, None
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                error_msg = f"A network error occurred: {e}. Please check the connection and try again."
                return None, error_msg
    error_msg = f"The server responded with an error (Status {response.status_code}) after multiple retries."
    return None, error_msg

def convert_df_to_csv(df):
   return df.to_csv(index=False).encode('utf-8')

def prepare_dataframe(data):
    """Flattens the nested topic data into a DataFrame."""
    rows = []
    header = ["Category", "Group Name", "Target Audience", "Publication Niche", "Funnel Stage", "Topic", "Suggested Headline", "Rationale"]
    
    def process_group(group_data, category, group_key, label):
        for item in group_data.get(group_key, []):
            group_name = item.get(label)
            for funnel in item.get('funnels', []):
                for audience in funnel.get('audiences', []):
                    for pub in audience.get('publications', []):
                        for topic in pub.get('topics', []):
                            rows.append({
                                "Category": category,
                                "Group Name": group_name,
                                "Target Audience": audience.get('audienceName'),
                                "Publication Niche": pub.get('publicationNiche'),
                                "Funnel Stage": funnel.get('funnelStage'),
                                "Topic": topic.get('topic'),
                                "Suggested Headline": topic.get('suggestedHeadline'),
                                "Rationale": topic.get('rationale')
                            })

    process_group(data, 'Product/Service', 'productBasedTopics', 'productName')
    process_group(data, 'Timely/Event', 'timelyTopics', 'eventName')

    return pd.DataFrame(rows, columns=header)


# --- Sidebar Logic ---
if st.session_state.get('analyze_btn_clicked', False):
    st.session_state.analyze_btn_clicked = False # Reset flag
    api_key = st.session_state.get("api_key")
    website_url = st.session_state.get("website_url_input")
    if not api_key:
        st.error("Please enter your Google API Key first.")
    elif not website_url:
        st.error("Please enter a website URL.")
    else:
        with st.spinner("Scraping and analyzing website..."):
            scraped_text, error = scrape_website(website_url)
            if error:
                st.error(error)
            else:
                analysis, error = analyze_scraped_text(api_key, scraped_text)
                if error:
                    st.error(error)
                else:
                    st.session_state.analysis_results = analysis
                    st.session_state.analyzed_url = website_url
                    st.session_state.industry = analysis.get('industry', '')
                    st.session_state.tone = analysis.get('tone', '')
                    st.session_state.audience_input = analysis.get('target_audience_pain_points', '')
                    st.session_state.product_input = analysis.get('services_and_products', '')
                    st.session_state.guidelines = analysis.get('guidelines', '')
                    st.success("Website analyzed!")
                    st.rerun()


with st.sidebar:
    with st.expander("1. Google API Key", expanded=True):
        api_key_val = st.text_input("Enter Google API Key", type="password", help="Your key is saved for the current session.", value=st.session_state.api_key)
        st.session_state.api_key = api_key_val
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Validate"):
                if st.session_state.api_key and validate_api_key(st.session_state.api_key):
                    st.success("Valid!")
                else:
                    st.error("Invalid!")
        with col2:
            if st.button("Clear", key="clear_api_key"):
                st.session_state.api_key = ""
                st.rerun()

    with st.expander("2. Website Analysis", expanded=True):
        website_url_val = st.text_input("Enter Website URL", value=st.session_state.get("website_url_input", ""))
        st.session_state.website_url_input = website_url_val
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Analyze Website"):
                st.session_state.analyze_btn_clicked = True
                st.rerun()
        with col2:
            if st.button("Clear", key="clear_url"):
                st.session_state.website_url_input = ""
                st.rerun()

    with st.expander("3. Business Details", expanded=True):
        st.info("Review or edit the details below.")
        st.text_input("Business Industry/Niche", key="industry")
        st.text_input("Branding Tone/Voice", key="tone")
        st.text_area("Target Audience", key="audience_input")
        st.text_area("Product/Service to Highlight", key="product_input")
        st.text_area("Full Copywriting Guidelines", key="guidelines")
        if st.button("Clear All Details"):
            st.session_state.industry = ""
            st.session_state.tone = ""
            st.session_state.audience_input = ""
            st.session_state.product_input = ""
            st.session_state.guidelines = ""
            st.rerun()


# --- Main Window Button and Topic Generation Logic ---
st.divider()
api_key_ready = bool(st.session_state.api_key)
details_ready = bool(st.session_state.guidelines or (st.session_state.industry and st.session_state.tone and st.session_state.audience_input and st.session_state.product_input))
is_ready = api_key_ready and details_ready

tags_html = ""
if api_key_ready: tags_html += '<span class="status-tag tag-green">API Key Provided</span>'
else: tags_html += '<span class="status-tag tag-red">API Key Missing</span>'

if details_ready: tags_html += '<span class="status-tag tag-green">Business Details Provided</span>'
else: tags_html += '<span class="status-tag tag-red">Business Details Missing</span>'
st.markdown(tags_html, unsafe_allow_html=True)

if is_ready: st.markdown('<style>div.stButton > button {background-color: #4CAF50; color: white; border-color: #4CAF50;}</style>', unsafe_allow_html=True)

if st.button("Generate Topics", type="primary"):
    if not is_ready:
        st.error("Action Required: Please provide a valid API key and sufficient business details in the sidebar.")
    else:
        with st.spinner("Generating topics... This may take up to a minute."):
            current_date = datetime.now().strftime('%B %d, %Y')
            
            system_prompt = """You are a strategic content and marketing analyst. Your task is to generate two distinct sets of guest post topics based on the provided business details and the current date. The topic generation must be guided by the marketing funnel principles (ToFu, MoFu, BoFu).

            First, analyze the provided text (which may be copywriting guidelines or a collection of details) to extract the business's industry, tone, target audiences, and products/services. When you identify a product, service, or event, summarize it into a short, clear name (e.g., "AI Security Solution" or "Annual Tech Conference") for the `productName` or `eventName` field. Do not use the entire descriptive text from the input.

            Second, generate two sets of topics ensuring there are at least 3 topics per funnel stage for each audience and product/event:
            1.  **Product-Based Topics:** Ideas directly related to the business's products/services.
            2.  **Timely & Event-Based Topics:** Based on the 'Current Date' and the business's industry, identify relevant upcoming holidays, industry events, or seasonal business milestones and create topics for them.

            For each generated topic, you must provide three elements:
            - 'topic': A short, concise title (MAXIMUM 60 characters) that frames the product/service as a solution to a problem relevant to the funnel stage.
            - 'suggestedHeadline': A longer, more engaging headline suitable for a full article.
            - 'rationale': A brief explanation of the topic's value and relevance.
            
            The final output must be a single JSON object with two top-level keys: `productBasedTopics` and `timelyTopics`, adhering to the provided schema.
            """

            user_query = f"Current Date: {current_date}\n\n"
            if st.session_state.guidelines:
                user_query += f"Full Copywriting Guidelines:\n---\n{st.session_state.guidelines}\n---\n"
                optional_inputs = {"Specific Industry/Niche": st.session_state.industry, "Specific Branding Tone/Voice": st.session_state.tone, "Specific Target Audiences": st.session_state.audience_input, "Specific Products/Services": st.session_state.product_input}
                if st.session_state.analysis_results:
                    optional_details = "\n".join([f"- {key}: {value}" for key, value in optional_inputs.items() if value and value != st.session_state.analysis_results.get(key.lower().replace('specific ', '').replace(' ', '_'))])
                else:
                    optional_details = "\n".join([f"- {key}: {value}" for key, value in optional_inputs.items() if value])
                if optional_details: user_query += f"\nSupplemental Details from Optional Fields:\n{optional_details}"
            else: 
                user_query += "Business Details:\n"
                primary_inputs = {"Industry/Niche": st.session_state.industry, "Branding Tone/Voice": st.session_state.tone, "Target Audiences": st.session_state.audience_input, "Products/Services to Highlight": st.session_state.product_input}
                primary_details = "\n".join([f"- {key}: {value}" for key, value in primary_inputs.items() if value])
                user_query += primary_details

            topic_properties = {"type": "OBJECT", "properties": {"topic": {"type": "STRING"}, "suggestedHeadline": {"type": "STRING"}, "rationale": {"type": "STRING"}}, "required": ["topic", "suggestedHeadline", "rationale"]}
            publication_properties = {"type": "OBJECT", "properties": {"publicationNiche": {"type": "STRING"}, "topics": {"type": "ARRAY", "items": topic_properties}}, "required": ["publicationNiche", "topics"]}
            audience_properties = {"type": "OBJECT", "properties": {"audienceName": {"type": "STRING"}, "publications": {"type": "ARRAY", "items": publication_properties}}, "required": ["audienceName", "publications"]}
            funnel_properties = {"type": "OBJECT", "properties": {"funnelStage": {"type": "STRING", "enum": ["ToFu", "MoFu", "BoFu"]}, "audiences": {"type": "ARRAY", "items": audience_properties}}, "required": ["funnelStage", "audiences"]}
            product_based_topics_properties = {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"productName": {"type": "STRING", "description": "A short, summarized name for the product/service (e.g., 'AI Security Solution')."}, "funnels": {"type": "ARRAY", "items": funnel_properties}}, "required": ["productName", "funnels"]}}
            timely_topics_properties = {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"eventName": {"type": "STRING", "description": "A short, summarized name for the event or holiday (e.g., 'Q4 Sales Kickoff')."}, "funnels": {"type": "ARRAY", "items": funnel_properties}}, "required": ["eventName", "funnels"]}}
            schema = {"type": "OBJECT", "properties": {"productBasedTopics": product_based_topics_properties, "timelyTopics": timely_topics_properties}, "required": ["productBasedTopics", "timelyTopics"]}

            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={st.session_state.api_key}"
            payload = {"contents": [{"parts": [{"text": user_query}]}], "systemInstruction": {"parts": [{"text": system_prompt}]}, "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}
            options = {'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(payload)}
            
            response, error_msg = fetch_with_retry(api_url, options)
            
            if error_msg:
                st.error(error_msg)
            elif response and response.status_code == 200:
                try:
                    result = response.json()
                    text_content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    if text_content:
                        data = json.loads(text_content)
                        st.session_state.generated_data = data
                        st.session_state.dataframe = prepare_dataframe(data)
                    else:
                        st.error("No content received from API.")
                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    st.error(f"Failed to parse API response: {e}")
            elif response:
                 try:
                     error_details = response.json()
                     st.error(f"API request failed with status code: {response.status_code}.")
                     st.json(error_details)
                 except json.JSONDecodeError:
                     st.error(f"API request failed with status code: {response.status_code}.")

# --- Display Results ---
if not st.session_state.dataframe.empty:
    st.header("Generated Topics", divider="rainbow")
    
    if st.session_state.get('analysis_results'):
        st.subheader("Website Analysis Summary")
        with st.container(border=True):
            analysis = st.session_state.analysis_results
            st.markdown(f"**Website URL:** {st.session_state.get('analyzed_url', 'N/A')}")
            st.markdown(f"**Target Audience and Pain Points:** {analysis.get('target_audience_pain_points', 'Not found')}")
            st.markdown(f"**Business Services and/or Products:** {analysis.get('services_and_products', 'Not found')}")
            st.markdown(f"**Target Location:** {analysis.get('target_location', 'Not found')}")
    
    st.subheader("Filter and Search Topics")
    
    df_to_display = st.session_state.dataframe.copy()

    # Search bar
    search_query = st.text_input("Search topics...")
    if search_query:
        df_to_display = df_to_display[df_to_display.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    # Filter dropdowns
    col1, col2, col3 = st.columns(3)
    with col1:
        categories = df_to_display['Category'].unique()
        selected_categories = st.multiselect("Filter by Category", categories, default=categories)
    with col2:
        funnels = df_to_display['Funnel Stage'].unique()
        selected_funnels = st.multiselect("Filter by Funnel Stage", funnels, default=funnels)
    with col3:
        audiences = df_to_display['Target Audience'].unique()
        selected_audiences = st.multiselect("Filter by Target Audience", audiences, default=audiences)
    
    # Apply filters
    filtered_df = df_to_display[
        df_to_display['Category'].isin(selected_categories) &
        df_to_display['Funnel Stage'].isin(selected_funnels) &
        df_to_display['Target Audience'].isin(selected_audiences)
    ]

    st.dataframe(filtered_df, use_container_width=True)

    st.divider()
    csv_data = convert_df_to_csv(filtered_df)
    st.download_button(
        label="Download Displayed Topics as CSV",
        data=csv_data,
        file_name=f"topic_generator_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
    )

