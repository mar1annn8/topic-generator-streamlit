import streamlit as st
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import io
from urllib.parse import urljoin, urlparse
import os
import re
from collections import Counter
import nltk

# --- Download NLTK data ---
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords

# --- Page Configuration ---
st.set_page_config(
    page_title="Topic Generator",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Reduce top padding */
        .block-container {
            padding-top: 1rem;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .status-tag {
            display: inline-block;
            padding: 0.3em 0.8em;
            margin: 0.2em;
            font-size: 0.9em;
            font-weight: bold;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
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
        div.stButton > button {
            width: 100%;
        }
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
st.markdown("<p style='font-size: 1px;'>&nbsp;</p>", unsafe_allow_html=True) # Spacer to push title down
st.markdown("<h1 style='background-color: #FFF9C4; padding: 10px; border-radius: 10px;'>Topic Generator</h1>", unsafe_allow_html=True)
st.markdown("""
This AI tool generates topic ideas based on the marketing funnel concepts from 
[SEMRush](https://www.semrush.com/blog/content-marketing-funnel/), 
[Search Engine Land](https://searchengineland.com/how-to-drive-the-funnel-through-content-marketing-and-link-building-374343), and
Google's guidelines on creating [helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) and [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).
This approach ensures topics are valuable to the target audience by emphasizing expertise, authoritativeness, and trustworthiness (E-E-A-T).
""")

with st.expander("Instructions"):
    with st.expander("How to Use This Tool"):
        st.markdown("""
        How to Use the Topic Generator Tool for Strategic Content Ideas

        This guide explains how to use the Topic Generator tool to create strong, pitch-ready content topics. These ideas can be used for articles, videos, infographics, or any format that fits your strategy.

        **1. Understand the Tool**

        The Topic Generator is an AI tool that suggests relevant, high-quality content ideas. It analyzes your business information and organizes topics by stage of the marketing funnel:

        - Top of Funnel (ToFu): Builds awareness
        - Middle of Funnel (MoFu): Encourages consideration
        - Bottom of Funnel (BoFu): Supports decision-making

        The tool follows proven content strategy methods used by experts at SEMRush and Search Engine Land.

        **2. Add Business Information**

        The tool works best when it has full context. Start by filling out the labeled fields:

        - Business Industry/Niche: Describe the industry or market your business operates in
        - Branding Tone/Voice: Share the preferred tone or style of your brand’s communication
        - Target Audience: Define the audience personas or customer segments you want to reach
        - Product/Service to Highlight: Mention the specific offering you want the content to focus on
        - Full Copywriting Guidelines: Paste your complete brand guidelines or any detailed document that explains your tone, audience, products, and positioning. This field is the most important—use it to give the AI full context.

        You can skip the first four fields if your copywriting guidelines already include that information. But if the output feels too general, adding details to those fields can help improve the results.

        **3. Generate Topic Ideas**

        Once the fields are filled out, click the “Generate Topics” button. The tool will take a few moments to process your request.

        **4. View and Understand the Output**

        The results will appear in the main window, just below the “Generate Topics” button. The output includes three parts:

        **Table 1: Business Analysis Summary**
        This section gives a quick overview of the business, including Website URL, Target Location, Identified Industry, Target Audience and Pain Points. It also includes a detailed breakdown of:
        - Business Services and/or Products
        - Associated Industry
        - Associated Audience
        - Associated Pain Point

        **Table 2: Available Pages for Linking**
        A table listing all available, crawlable pages from the analyzed website. This table includes:
        - URL
        - Page Title
        - Meta Description
        - Content Summary

        **Table 3: Topics**
        This section contains the suggested content ideas, organized in a table with the following columns: Category, Group Name, Target Audience, Publication Niche, Funnel Stage, Topic, Suggested Headline, Rationale, Anchor text, Destination Page, Focus Keyword

        Each row in the table represents a content idea. The AI groups topics by product, service, or event, and aligns them with the right funnel stage and audience.

        **Tips for Better Results**

        - Prioritize the Guidelines Field: Use a complete document in the “Full Copywriting Guidelines” field for the most accurate suggestions
        - Add Specifics When Needed: If the topics feel too broad, use the other fields to guide the AI
        - Treat as a Starting Point: Review and refine the output before pitching or publishing. A strategist should ensure the ideas match your goals
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
        
try:
    mod_time = os.path.getmtime(__file__)
    last_updated_date = datetime.fromtimestamp(mod_time).strftime('%m/%d/%Y')
except Exception:
    last_updated_date = "N/A" # Fallback if file path is not accessible
    
st.markdown(f"<div style='text-align: right; font-size: 0.8em; color: grey;'>Last Updated: {last_updated_date}</div>", unsafe_allow_html=True)


# --- Initialize Session State ---
if 'api_key' not in st.session_state: st.session_state.api_key = ""
if 'industry' not in st.session_state: st.session_state.industry = ""
if 'tone' not in st.session_state: st.session_state.tone = ""
if 'audience_input' not in st.session_state: st.session_state.audience_input = ""
if 'product_input' not in st.session_state: st.session_state.product_input = ""
if 'guidelines' not in st.session_state: st.session_state.guidelines = ""
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = None
if 'analyzed_url' not in st.session_state: st.session_state.analyzed_url = ""
if 'scraped_links' not in st.session_state: st.session_state.scraped_links = []
if 'generated_data' not in st.session_state: st.session_state.generated_data = None
if 'analyze_btn_clicked' not in st.session_state: st.session_state.analyze_btn_clicked = False
if 'dataframe' not in st.session_state: st.session_state.dataframe = pd.DataFrame()
if 'available_pages_df' not in st.session_state: st.session_state.available_pages_df = pd.DataFrame()


# --- Functions ---
STOPWORDS = set(stopwords.words("english"))

def validate_api_key(api_key):
    """Checks if the API key is valid by making a simple request."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def summarize_text(text, sentence_count=1):
    """Simple extractive summary."""
    text = re.sub(r'\s+', ' ', text) # Normalize whitespace
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s for s in sentences if len(s.split()) > 5] # Filter short sentences
    if not sentences:
        return "No summary available."
    return " ".join(sentences[:sentence_count])

def scrape_page_details(url, headers):
    """Scrapes details from a single page."""
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string.strip() if soup.title else "No Title"
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        meta = meta_tag['content'].strip() if meta_tag and meta_tag.get('content') else "No Meta Description"
        
        for script in soup(["script", "style"]):
            script.extract()
        content = soup.get_text(separator=' ', strip=True)
        
        summary = summarize_text(content)

        return {'URL': url, 'Page Title': title, 'Meta Description': meta, 'Content Summary': summary}
    except requests.RequestException:
        return None


def scrape_website(url):
    """Scrapes the main page and extracts internal links and their details."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        main_text = soup.get_text(separator='\n', strip=True)

        links = set()
        base_netloc = urlparse(url).netloc
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == base_netloc:
                clean_url = urljoin(full_url, urlparse(full_url).path)
                links.add(clean_url)
        
        pages = []
        homepage_details = scrape_page_details(url, headers)
        if homepage_details:
            pages.append(homepage_details)
        
        for link in list(links)[:19]: # Limit total crawl to 20 pages
             if link != url:
                details = scrape_page_details(link, headers)
                if details:
                    pages.append(details)
        
        unique_pages = list({p['URL']: p for p in pages}.values())
        
        return main_text[:15000], unique_pages, None
    except requests.RequestException as e:
        return None, [], f"Failed to fetch website content: {e}"

def analyze_scraped_text(api_key, text):
    """Uses AI to analyze scraped text and extract business details."""
    industry_database = """
- Adult Products: Products related to adult entertainment and intimacy (e.g., Adult toys, lingerie, sexual wellness products)
- Agriculture & Environment: Farming, natural resource management, sustainability (e.g., Crop production, livestock, forestry, conservation)
- Performing Arts & Cultural Experiences: Creative expression, entertainment (e.g., Theater, dance, concerts, museums)
- Visual Arts & Entertainment: Creative expression, entertainment (e.g., Visual arts, film, television, gaming)
- Autos & Vehicles: Design, manufacturing, and sales of vehicles (e.g., Cars, trucks, motorcycles, RVs)
- Beauty & Fitness: Personal care, appearance, physical well-being (e.g., Cosmetics, skincare, gyms, personal training)
- Business & Industrial: Commercial activities, manufacturing, professional services (e.g., Manufacturing, construction, logistics, B2B services)
- Computers & Electronics: Technology and electronic devices (e.g., Hardware, software, IT services, consumer electronics)
- Fashion: Clothing, footwear, accessories, and style (e.g., Apparel design, manufacturing, retail)
- Finance: Money management, investments, banking (e.g., Banking, insurance, financial planning, accounting)
- Firearms & Weapons: Firearms, ammunition, and related equipment (e.g., Guns, rifles, hunting gear)
- Food & Beverage: Production and sale of food and drinks (e.g., Restaurants, cafes, food manufacturing, grocery stores)
- Gifts & Shopping: Retail, e-commerce, and consumer goods (e.g., Gift shops, department stores, online retailers)
- Health & Wellness: Healthcare, personal well-being (e.g., Hospitals, clinics, pharmacies, mental health services, supplements)
- Hobbies & Leisure: Recreational activities and pastimes (e.g., Arts and crafts, gaming, sports, travel)
- Home & Garden: Home improvement, décor, gardening (e.g., Furniture, appliances, home décor, landscaping)
- Hospitality & Travel: Accommodation, tourism, and travel services (e.g., Hotels, resorts, airlines, travel agencies)
- Internet & Telecommunications: Digital communication and online services (e.g., ISPs, social media platforms)
- Jobs & Education: Employment, training, and education (e.g., Recruitment, schools, universities, online learning)
- Kids & Family: Products and services for children and families (e.g., Toys, childcare, parenting resources)
- Law & Government: Legal services, public administration (e.g., Law firms, government agencies, courts)
- Lifestyle: Personal interests, values, and way of living (e.g., Fashion, beauty, travel, food)
- Logistics & Transportation: Movement of goods and people (e.g., Shipping, trucking, warehousing, airlines)
- Marketing: Promoting products, services, or ideas (e.g., Market research, advertising, digital marketing)
- Media & Communications: Information dissemination, journalism (e.g., Journalism, publishing, broadcasting)
- Medical Cannabis: Cannabis for medical use (e.g., Dispensaries, cultivation, medical marijuana products)
- News: Current events and information (e.g., Newspapers, online news portals)
- Not For Profit: Charitable organizations and social causes (e.g., Charities, foundations, NGOs)
- People & Society: Social issues, community, and culture (e.g., Social services, advocacy groups)
- Pets & Animals: Pet care and animal welfare (e.g., Pet food, veterinary services, animal shelters)
- Real Estate: Property, land, and buildings (e.g., Residential, commercial, real estate brokerage)
- Recreational Cannabis: Cannabis for recreational use (where legal) (e.g., Dispensaries, cannabis products)
- Science: Research, discovery, and innovation (e.g., Scientific research institutions, laboratories)
- Specialty Products: Unique, niche, or regulated goods (e.g., Antiques, collectibles, luxury goods)
- Vices & Adult Entertainment: Activities and products considered taboo (e.g., Gambling, pornography, tobacco, alcohol)
- Other: Any industry not explicitly categorized above.
"""
    
    system_prompt = f"""You are an expert marketing analyst. Analyze the provided website text and extract the following information. Be concise and summarize the findings.

Industry Database:
{industry_database}

Your Tasks:
1.  Analyze the website text to determine its primary industry (e.g., "AI-based logistics").
2.  Compare this identified industry against the 'Industry Database' provided above.
3.  Format the 'identified_industry' output:
    - If a clear match is found, return the category name (e.g., "Health & Wellness").
    - If no clear match is found, return "Not found (Identified as: [Industry you found])".
4.  Extract all other required information.
5.  For 'business_services_products', identify each distinct service or product. For each one, find its most relevant industry, target audience, and the specific pain point it solves.

- **target_audience_pain_points:** The *overall* target audience and their main problems.
- **business_services_products:** A list of objects, where each object contains:
    - 'service_or_product' (string)
    - 'associated_industry' (string)
    - 'associated_audience' (string)
    - 'associated_pain_point' (string)
- **target_location:** The primary geographical market (e.g., USA, California, Global).
- **identified_industry:** [Your formatted output from step 3]
- **branding_tone_voice:** The style and personality of the business's communication.
- **branding_guidelines_summary:** Summarize any core messaging or branding principles evident from the text."""
    
    schema = {
        "type": "OBJECT",
        "properties": {
            "target_audience_pain_points": {"type": "STRING"},
            "business_services_products": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "service_or_product": {"type": "STRING"},
                        "associated_industry": {"type": "STRING"},
                        "associated_audience": {"type": "STRING"},
                        "associated_pain_point": {"type": "STRING"}
                    },
                    "required": ["service_or_product", "associated_industry", "associated_audience", "associated_pain_point"]
                }
            },
            "target_location": {"type": "STRING"},
            "identified_industry": {"type": "STRING", "description": "The industry, formatted as specified in the prompt."},
            "branding_tone_voice": {"type": "STRING"},
            "branding_guidelines_summary": {"type": "STRING"}
        },
        "required": ["target_audience_pain_points", "business_services_products", "target_location", "identified_industry", "branding_tone_voice", "branding_guidelines_summary"]
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
            response = requests.post(url, headers=options['headers'], data=options['body'], timeout=120)
            if response.status_code < 500:
                return response, None
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                error_msg = f"A network error occurred: {e}. Please check the connection and try again."
                return None, error_msg
    error_msg = f"The server responded with an error (Status {response.status_code}) after multiple retries."
    return None, error_msg

def convert_df_to_csv(topics_df, available_pages_df, analysis_data, analyzed_url):
    """Prepares data for CSV export with all three tables."""
    output = io.StringIO()

    # Table 1: Business Analysis Summary
    if analysis_data:
        output.write("Table 1: Business Analysis Summary\n")
        summary_df = pd.DataFrame([
            ["Website URL:", analyzed_url],
            ["Target Location:", analysis_data.get('target_location', 'Not found')],
            ["Identified Industry:", analysis_data.get('identified_industry', 'Not found')],
            ["Target Audience and Pain Points:", analysis_data.get('target_audience_pain_points', 'Not found')]
        ])
        summary_df.to_csv(output, header=False, index=False)
        output.write("\n")
        
        output.write("Business Services and/or Products\n")
        products_df = pd.DataFrame(analysis_data.get('business_services_products', []))
        # Rename columns for clarity in CSV
        if not products_df.empty:
            products_df.columns = ["Service/Product", "Associated Industry", "Associated Audience", "Associated Pain Point"]
        products_df.to_csv(output, index=False)
        output.write("\n")


    # Table 2: Available Pages for Linking
    if not available_pages_df.empty:
        output.write("Table 2: Available Pages for Linking\n")
        available_pages_df.to_csv(output, index=False)
        output.write("\n")

    # Table 3: Topics
    output.write("Table 3: Topics\n")
    topics_df.to_csv(output, index=False)
    
    return output.getvalue().encode('utf-8')

def prepare_dataframe(data):
    """Flattens the nested topic data into a DataFrame."""
    rows = []
    header = ["Category", "Group Name", "Target Audience", "Publication Niche", "Funnel Stage", "Topic", "Suggested Headline", "Rationale", "Anchor text", "Destination Page", "Focus Keyword"]
    
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
                                "Rationale": topic.get('rationale'),
                                "Anchor text": topic.get('anchorText'),
                                "Destination Page": topic.get('destinationPage'),
                                "Focus Keyword": topic.get('focusKeyword')
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
            scraped_text, scraped_pages, error = scrape_website(website_url)
            if error:
                st.error(error)
            else:
                analysis, error = analyze_scraped_text(api_key, scraped_text)
                if error:
                    st.error(error)
                else:
                    st.session_state.analysis_results = analysis
                    st.session_state.analyzed_url = website_url
                    st.session_state.scraped_links = scraped_pages
                    st.session_state.available_pages_df = pd.DataFrame(scraped_pages)
                    st.session_state.industry = analysis.get('identified_industry', '')
                    st.session_state.tone = analysis.get('branding_tone_voice', '')
                    st.session_state.audience_input = analysis.get('target_audience_pain_points', '')
                    
                    # Convert services list to a string for the text area
                    products_list = analysis.get('business_services_products', [])
                    products_str = "\n".join([f"- {p.get('service_or_product')}" for p in products_list])
                    st.session_state.product_input = products_str
                    
                    st.session_state.guidelines = analysis.get('branding_guidelines_summary', '')
                    st.success("Website analyzed!")
                    st.rerun()

with st.sidebar:
    st.markdown("<h2 style='font-weight: bold;'>Settings</h2>", unsafe_allow_html=True)

    with st.expander("1. Google API Key", expanded=True):
        st.text_input("Enter Google API Key", type="password", help="Your key is saved for the current session.", key="api_key_input", on_change=lambda: st.session_state.update(api_key=st.session_state.api_key_input))
        
        if st.button("Validate"):
            if st.session_state.api_key and validate_api_key(st.session_state.api_key):
                st.success("Valid!")
            else:
                st.error("Invalid!")

    with st.expander("2. Business Details", expanded=True):
        st.subheader("Website Analysis")
        st.info("Enter a website URL to auto-populate the fields below.")
        st.text_input("Enter Website URL", key="website_url_input")
        if st.button("Analyze Website"):
            st.session_state.analyze_btn_clicked = True
            st.rerun()
        
        st.divider()
        st.info("Or enter/edit the details manually.")
        st.text_input("Business Industry/Niche", key="industry")
        st.text_input("Branding Tone/Voice", key="tone")
        st.text_area("Target Audience", key="audience_input")
        st.text_area("Product/Service to Highlight", key="product_input")
        st.text_area("Full Copywriting Guidelines", key="guidelines")


# --- Main Window Button and Topic Generation Logic ---
st.divider()

api_key_ready = bool(st.session_state.api_key)
details_ready = bool(st.session_state.guidelines or (st.session_state.industry and st.session_state.tone and st.session_state.audience_input and st.session_state.product_input))
is_ready = api_key_ready and details_ready

# Apply green color to button if ready
if is_ready:
    st.markdown('<style>div.stButton > button {background-color: #4CAF50; color: white; border-color: #4CAF50;}</style>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    generate_btn = st.button("Generate Topics", type="primary")

with col2:
    api_tag = '<span class="status-tag tag-green">API Key</span>' if api_key_ready else '<span class="status-tag tag-red">API Key</span>'
    details_tag = '<span class="status-tag tag-green">Business Details</span>' if details_ready else '<span class.status-tag tag-red">Business Details</span>'
    st.markdown(f"""
    <div style="display: flex; align-items: center; height: 100%;">
        <h6 style='margin: 0; padding-right: 10px; font-weight: normal; font-size: 0.9em;'>Requirements to Run App:</h6>
        {api_tag}
        <span style='margin: 0 10px; font-weight: bold; vertical-align: middle;'>+</span>
        {details_tag}
    </div>
    """, unsafe_allow_html=True)


if generate_btn:
    if not is_ready:
        st.error("Action Required: Please provide a valid API key and sufficient business details in the sidebar.")
    else:
        with st.spinner("Generating topics... This may take up to a minute."):
            current_date = datetime.now().strftime('%B %d, %Y')
            
            system_prompt = """You are a strategic content and marketing analyst. Your task is to generate two distinct sets of guest post topics based on the provided business details and the current date. The topic generation must be guided by the marketing funnel principles (ToFu, MoFu, BoFu) and a diverse anchor text strategy.

            First, analyze the provided text (which may be copywriting guidelines or a collection of details) to extract the business's industry, tone, target audiences, and products/services. When you identify a product, service, or event, summarize it into a short, clear name (e.g., "AI Security Solution" or "Annual Tech Conference") for the `productName` or `eventName` field.

            Second, generate topics for two categories: "Product-Based" and "Timely & Event-Based." Ensure a diverse mix of anchor text types across all generated topics, guided by these ideal proportions: Branded (50%), Naked URL (20%), Page Title (20%), Generic/Random (2-5%), Exact Match (2-5%), Partial Match (2-5%).

            For each generated topic, you must provide six elements:
            - 'topic': A short, concise title (MAXIMUM 60 characters) that frames the product/service as a solution.
            - 'suggestedHeadline': A longer, more engaging headline for an article.
            - 'rationale': A brief explanation of the topic's value.
            - 'anchorText': A descriptive, concise, and relevant anchor text for an internal link. VARY the type of anchor text according to the proportions above.
            - 'destinationPage': You MUST select the single most relevant URL from the `List of Available URLs` provided. Your selection must be an exact match from that list. Follow this strict priority order: 1. A dedicated product/service page. 2. A relevant blog post. 3. Any other contextually relevant page. If no good match is found, use the `Base Website URL` as the fallback. Do not invent or use placeholder URLs.
            - 'focusKeyword': Based on the topic and headline, suggest a primary focus keyword for the content.
            
            The final output must be a single JSON object with two top-level keys: `productBasedTopics` and `timelyTopics`, adhering to the provided schema.
            """

            user_query = f"Current Date: {current_date}\n\n"
            if st.session_state.analyzed_url:
                 user_query += f"Base Website URL for Destination Pages: {st.session_state.analyzed_url}\n"
                 if st.session_state.scraped_links:
                     user_query += "List of Available URLs to choose from for the 'destinationPage' (with their anchor text for context):\n"
                     for page in st.session_state.scraped_links:
                         user_query += f"- {page['URL']} (Context: {page['Page Title']})\n"
                     user_query += "\n"


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

            topic_properties = {"type": "OBJECT", "properties": {"topic": {"type": "STRING"}, "suggestedHeadline": {"type": "STRING"}, "rationale": {"type": "STRING"}, "anchorText": {"type": "STRING"}, "destinationPage": {"type": "STRING"}, "focusKeyword": {"type": "STRING"}}, "required": ["topic", "suggestedHeadline", "rationale", "anchorText", "destinationPage", "focusKeyword"]}
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
        st.subheader("Table 1: Website Analysis Summary")
        analysis = st.session_state.analysis_results
        
        summary_data = {
            "Metric": [
                "Website URL", 
                "Target Location", 
                "Identified Industry", 
                "Target Audience and Pain Points"
            ],
            "Details": [
                st.session_state.get('analyzed_url', 'N/A'),
                analysis.get('target_location', 'Not found'),
                analysis.get('identified_industry', 'Not found'),
                analysis.get('target_audience_pain_points', 'Not found')
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, hide_index=True, use_container_width=True)

        st.markdown("**Business Services and/or Products:**")
        products_list = analysis.get('business_services_products', [])
        if products_list:
            products_df = pd.DataFrame(products_list)
            products_df.columns = ["Service/Product", "Associated Industry", "Associated Audience", "Associated Pain Point"]
            st.dataframe(products_df, hide_index=True, use_container_width=True)
        else:
            st.text("No specific services or products were identified.")

    
    if not st.session_state.available_pages_df.empty:
        st.subheader("Table 2: Available Pages for Linking")
        st.dataframe(st.session_state.available_pages_df, use_container_width=True)

    st.subheader("Table 3: Topics")
    
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
    
    # Use a single download button for the combined CSV
    combined_csv = convert_df_to_csv(filtered_df, st.session_state.available_pages_df, st.session_state.analysis_results, st.session_state.analyzed_url)
    st.download_button(
        label="Download All Results as CSV",
        data=combined_csv,
        file_name=f"topic_generator_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
    )

