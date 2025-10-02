{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red111\green14\blue195;\red236\green241\blue247;\red0\green0\blue0;
\red77\green80\blue85;\red24\green112\blue43;\red164\green69\blue11;}
{\*\expandedcolortbl;;\cssrgb\c51765\c18824\c80784;\cssrgb\c94118\c95686\c97647;\cssrgb\c0\c0\c0;
\cssrgb\c37255\c38824\c40784;\cssrgb\c9412\c50196\c21961;\cssrgb\c70980\c34902\c3137;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf0 \strokec4  streamlit \cf2 \strokec2 as\cf0 \strokec4  st\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  requests\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  json\cb1 \
\cf2 \cb3 \strokec2 from\cf0 \strokec4  datetime \cf2 \strokec2 import\cf0 \strokec4  datetime\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Page Configuration ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.set_page_config(\cb1 \
\cb3     page_title=\cf6 \strokec6 "Topic Generator"\cf0 \strokec4 ,\cb1 \
\cb3     layout=\cf6 \strokec6 "wide"\cf0 \cb1 \strokec4 \
\cb3 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- UI Display ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.title(\cf6 \strokec6 "Topic Generator"\cf0 \strokec4 )\cb1 \
\cb3 st.markdown(\cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6 This AI tool generates topic ideas based on the marketing funnel concepts from \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 [SEMRush](https://www.semrush.com/blog/content-marketing-funnel/) and \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 [Search Engine Land](https://searchengineland.com/how-to-drive-the-funnel-through-content-marketing-and-link-building-374343), \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 tailored to the client details provided.\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 """\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.header(\cf6 \strokec6 "Client Details"\cf0 \strokec4 )\cb1 \
\cb3 st.sidebar.info(\cf6 \strokec6 "Fill out the fields below. For the most accurate results, paste the full copywriting guidelines into field 5."\cf0 \strokec4 )\cb1 \
\
\cb3 industry = st.sidebar.text_input(\cf6 \strokec6 "1. Client Industry/Niche (Optional)"\cf0 \strokec4 , placeholder=\cf6 \strokec6 "e.g., B2B SaaS for project management"\cf0 \strokec4 )\cb1 \
\cb3 tone = st.sidebar.text_input(\cf6 \strokec6 "2. Branding Tone/Voice (Optional)"\cf0 \strokec4 , placeholder=\cf6 \strokec6 "e.g., Authoritative, yet approachable"\cf0 \strokec4 )\cb1 \
\cb3 audience_input = st.sidebar.text_area(\cf6 \strokec6 "3. Target Audience (Optional)"\cf0 \strokec4 , placeholder=\cf6 \strokec6 "e.g., Marketing managers in tech startups, Freelance project managers"\cf0 \strokec4 )\cb1 \
\cb3 product_input = st.sidebar.text_area(\cf6 \strokec6 "4. Product/Service to Highlight (Optional)"\cf0 \strokec4 , placeholder=\cf6 \strokec6 "e.g., https://my-saas.com/ai-feature OR Annual conference"\cf0 \strokec4 )\cb1 \
\cb3 guidelines = st.sidebar.text_area(\cf6 \strokec6 "5. Full Copywriting Guidelines / Additional Context"\cf0 \strokec4 , placeholder=\cf6 \strokec6 "Paste the full copywriting guidelines document here..."\cf0 \strokec4 )\cb1 \
\
\cb3 generate_btn = st.sidebar.button(\cf6 \strokec6 "Generate Topics"\cf0 \strokec4 , \cf2 \strokec2 type\cf0 \strokec4 =\cf6 \strokec6 "primary"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Functions for API Call and Display ---\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  fetch_with_retry(url, options, retries=\cf7 \strokec7 3\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf6 \strokec6 """Simple retry logic for the API call."""\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  i \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (retries):\cb1 \
\cb3         \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3             response = requests.post(url, headers=options[\cf6 \strokec6 'headers'\cf0 \strokec4 ], data=options[\cf6 \strokec6 'body'\cf0 \strokec4 ])\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  response.status_code == \cf7 \strokec7 200\cf0 \strokec4 :\cb1 \
\cb3                 \cf2 \strokec2 return\cf0 \strokec4  response\cb1 \
\cb3         \cf2 \strokec2 except\cf0 \strokec4  requests.exceptions.RequestException \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  i == retries - \cf7 \strokec7 1\cf0 \strokec4 :\cb1 \
\cb3                 st.error(\cf6 \strokec6 f"Request failed after \cf0 \strokec4 \{retries\}\cf6 \strokec6  retries: \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 return\cf0 \strokec4  \cf2 \strokec2 None\cf0 \cb1 \strokec4 \
\cb3     st.error(\cf6 \strokec6 f"API request failed with status code: \cf0 \strokec4 \{response.status_code\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  \cf2 \strokec2 None\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  create_topic_group(group_name, funnels, group_label):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf6 \strokec6 """Renders a single group of topics (for a product or event)."""\cf0 \cb1 \strokec4 \
\cb3     st.header(\cf6 \strokec6 f"\cf0 \strokec4 \{group_label\}\cf6 \strokec6 : \cf0 \strokec4 \{group_name\}\cf6 \strokec6 "\cf0 \strokec4 , divider=\cf6 \strokec6 "gray"\cf0 \strokec4 )\cb1 \
\cb3     \cb1 \
\cb3     funnel_map = \{\cb1 \
\cb3         \cf6 \strokec6 "ToFu"\cf0 \strokec4 : (\cf6 \strokec6 "ToFu (Awareness)"\cf0 \strokec4 , \cf6 \strokec6 "blue"\cf0 \strokec4 ),\cb1 \
\cb3         \cf6 \strokec6 "MoFu"\cf0 \strokec4 : (\cf6 \strokec6 "MoFu (Consideration)"\cf0 \strokec4 , \cf6 \strokec6 "green"\cf0 \strokec4 ),\cb1 \
\cb3         \cf6 \strokec6 "BoFu"\cf0 \strokec4 : (\cf6 \strokec6 "BoFu (Decision)"\cf0 \strokec4 , \cf6 \strokec6 "red"\cf0 \strokec4 )\cb1 \
\cb3     \}\cb1 \
\cb3     stage_order = \{ \cf6 \strokec6 'ToFu'\cf0 \strokec4 : \cf7 \strokec7 1\cf0 \strokec4 , \cf6 \strokec6 'MoFu'\cf0 \strokec4 : \cf7 \strokec7 2\cf0 \strokec4 , \cf6 \strokec6 'BoFu'\cf0 \strokec4 : \cf7 \strokec7 3\cf0 \strokec4  \}\cb1 \
\cb3     \cb1 \
\cb3     sorted_funnels = \cf2 \strokec2 sorted\cf0 \strokec4 (funnels, key=\cf2 \strokec2 lambda\cf0 \strokec4  f: stage_order.get(f.get(\cf6 \strokec6 'funnelStage'\cf0 \strokec4 , \cf6 \strokec6 ''\cf0 \strokec4 ), \cf7 \strokec7 0\cf0 \strokec4 ))\cb1 \
\
\cb3     \cf2 \strokec2 for\cf0 \strokec4  funnel \cf2 \strokec2 in\cf0 \strokec4  sorted_funnels:\cb1 \
\cb3         stage = funnel.get(\cf6 \strokec6 'funnelStage'\cf0 \strokec4 )\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  stage \cf2 \strokec2 in\cf0 \strokec4  funnel_map:\cb1 \
\cb3             name, color = funnel_map[stage]\cb1 \
\cb3             \cf2 \strokec2 with\cf0 \strokec4  st.container(border=\cf2 \strokec2 True\cf0 \strokec4 ):\cb1 \
\cb3                 st.subheader(\cf6 \strokec6 f":\cf0 \strokec4 \{color\}\cf6 \strokec6 [\cf0 \strokec4 \{name\}\cf6 \strokec6 ]"\cf0 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 for\cf0 \strokec4  audience \cf2 \strokec2 in\cf0 \strokec4  funnel.get(\cf6 \strokec6 'audiences'\cf0 \strokec4 , []):\cb1 \
\cb3                     st.markdown(\cf6 \strokec6 f"**Target Audience:** \cf0 \strokec4 \{audience.get('audienceName', 'N/A')\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3                     \cf2 \strokec2 for\cf0 \strokec4  pub \cf2 \strokec2 in\cf0 \strokec4  audience.get(\cf6 \strokec6 'publications'\cf0 \strokec4 , []):\cb1 \
\cb3                         \cf2 \strokec2 with\cf0 \strokec4  st.expander(\cf6 \strokec6 f"Publication Niche: \cf0 \strokec4 \{pub.get('publicationNiche', 'N/A')\}\cf6 \strokec6 "\cf0 \strokec4 ):\cb1 \
\cb3                             \cf2 \strokec2 for\cf0 \strokec4  topic \cf2 \strokec2 in\cf0 \strokec4  pub.get(\cf6 \strokec6 'topics'\cf0 \strokec4 , []):\cb1 \
\cb3                                 st.markdown(\cf6 \strokec6 f"**Title:** \cf0 \strokec4 \{topic.get('title', 'No Title')\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3                                 st.caption(\cf6 \strokec6 f"Rationale: \cf0 \strokec4 \{topic.get('rationale', 'No Rationale')\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3                                 st.markdown(\cf6 \strokec6 "---"\cf0 \strokec4 )\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- Main Logic ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  generate_btn:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  guidelines:\cb1 \
\cb3         st.sidebar.error(\cf6 \strokec6 "Please paste the copywriting guidelines into field 5 for analysis."\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3         \cf2 \strokec2 with\cf0 \strokec4  st.spinner(\cf6 \strokec6 "Generating topics... Please wait."\cf0 \strokec4 ):\cb1 \
\cb3             current_date = datetime.now().strftime(\cf6 \strokec6 '%B %d, %Y'\cf0 \strokec4 )\cb1 \
\cb3             \cb1 \
\cb3             system_prompt = \cf6 \strokec6 """You are a strategic content and marketing analyst. Your task is to generate two distinct sets of guest post topics based on the provided client guidelines and the current date. The topic generation must be guided by the marketing funnel principles (ToFu, MoFu, BoFu).\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6             First, analyze the 'Full Copywriting Guidelines' to extract the client's industry, tone, target audiences, and products/services. Use the optional fields (1-4) to supplement or clarify this information if provided.\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6             Second, generate two sets of topics:\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             1.  **Product-Based Topics:** Ideas directly related to the client's products/services you identified.\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6             2.  **Timely & Event-Based Topics:** Based on the 'Current Date' and the client's industry, identify relevant upcoming holidays, industry events, or seasonal business milestones and create topics for them.\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6             The final output must be a single JSON object with two top-level keys: `productBasedTopics` and `timelyTopics`, adhering to the provided schema. For each topic, create a title and rationale."""\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3             user_query = \cf6 \strokec6 f"Current Date: \cf0 \strokec4 \{current_date\}\cf6 \strokec6 \\n\\nFull Copywriting Guidelines:\\n---\\n\cf0 \strokec4 \{guidelines\}\cf6 \strokec6 \\n---\\n"\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             optional_inputs = \{\cb1 \
\cb3                 \cf6 \strokec6 "Specific Industry/Niche"\cf0 \strokec4 : industry,\cb1 \
\cb3                 \cf6 \strokec6 "Specific Branding Tone/Voice"\cf0 \strokec4 : tone,\cb1 \
\cb3                 \cf6 \strokec6 "Specific Target Audiences"\cf0 \strokec4 : audience_input,\cb1 \
\cb3                 \cf6 \strokec6 "Specific Products/Services"\cf0 \strokec4 : product_input\cb1 \
\cb3             \}\cb1 \
\
\cb3             optional_details = \cf6 \strokec6 "\\n"\cf0 \strokec4 .join([\cf6 \strokec6 f"- \cf0 \strokec4 \{key\}\cf6 \strokec6 : \cf0 \strokec4 \{value\}\cf6 \strokec6 "\cf0 \strokec4  \cf2 \strokec2 for\cf0 \strokec4  key, value \cf2 \strokec2 in\cf0 \strokec4  optional_inputs.items() \cf2 \strokec2 if\cf0 \strokec4  value])\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  optional_details:\cb1 \
\cb3                 user_query += \cf6 \strokec6 f"\\nSupplemental Details from Optional Fields:\\n\cf0 \strokec4 \{optional_details\}\cf6 \strokec6 "\cf0 \cb1 \strokec4 \
\
\cb3             schema = \{\cb1 \
\cb3                 \cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 ,\cb1 \
\cb3                 \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cb1 \
\cb3                     \cf6 \strokec6 "productBasedTopics"\cf0 \strokec4 : \{\cb1 \
\cb3                         \cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 ,\cb1 \
\cb3                         \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cb1 \
\cb3                             \cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "productName"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "funnels"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "funnelStage"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 , \cf6 \strokec6 "enum"\cf0 \strokec4 : [\cf6 \strokec6 "ToFu"\cf0 \strokec4 , \cf6 \strokec6 "MoFu"\cf0 \strokec4 , \cf6 \strokec6 "BoFu"\cf0 \strokec4 ]\}, \cf6 \strokec6 "audiences"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "audienceName"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "publications"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "publicationNiche"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "topics"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "title"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "rationale"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "title"\cf0 \strokec4 , \cf6 \strokec6 "rationale"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "publicationNiche"\cf0 \strokec4 , \cf6 \strokec6 "topics"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "audienceName"\cf0 \strokec4 , \cf6 \strokec6 "publications"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "funnelStage"\cf0 \strokec4 , \cf6 \strokec6 "audiences"\cf0 \strokec4 ]\}\}\}\cb1 \
\cb3                         \}\cb1 \
\cb3                     \},\cb1 \
\cb3                     \cf6 \strokec6 "timelyTopics"\cf0 \strokec4 : \{\cb1 \
\cb3                         \cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 ,\cb1 \
\cb3                         \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cb1 \
\cb3                             \cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "eventName"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "funnels"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "funnelStage"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 , \cf6 \strokec6 "enum"\cf0 \strokec4 : [\cf6 \strokec6 "ToFu"\cf0 \strokec4 , \cf6 \strokec6 "MoFu"\cf0 \strokec4 , \cf6 \strokec6 "BoFu"\cf0 \strokec4 ]\}, \cf6 \strokec6 "audiences"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "audienceName"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "publications"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "publicationNiche"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "topics"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "ARRAY"\cf0 \strokec4 , \cf6 \strokec6 "items"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "OBJECT"\cf0 \strokec4 , \cf6 \strokec6 "properties"\cf0 \strokec4 : \{\cf6 \strokec6 "title"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}, \cf6 \strokec6 "rationale"\cf0 \strokec4 : \{\cf6 \strokec6 "type"\cf0 \strokec4 : \cf6 \strokec6 "STRING"\cf0 \strokec4 \}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "title"\cf0 \strokec4 , \cf6 \strokec6 "rationale"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "publicationNiche"\cf0 \strokec4 , \cf6 \strokec6 "topics"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "audienceName"\cf0 \strokec4 , \cf6 \strokec6 "publications"\cf0 \strokec4 ]\}\}\}, \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "funnelStage"\cf0 \strokec4 , \cf6 \strokec6 "audiences"\cf0 \strokec4 ]\}\}\}\cb1 \
\cb3                         \}\cb1 \
\cb3                     \}\cb1 \
\cb3                 \},\cb1 \
\cb3                 \cf6 \strokec6 "required"\cf0 \strokec4 : [\cf6 \strokec6 "productBasedTopics"\cf0 \strokec4 , \cf6 \strokec6 "timelyTopics"\cf0 \strokec4 ]\cb1 \
\cb3             \}\cb1 \
\
\cb3             api_key = \cf6 \strokec6 ""\cf0 \strokec4  \cf5 \strokec5 # API key is handled by the environment\cf0 \cb1 \strokec4 \
\cb3             api_url = \cf6 \strokec6 f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=\cf0 \strokec4 \{api_key\}\cf6 \strokec6 "\cf0 \cb1 \strokec4 \
\
\cb3             payload = \{\cb1 \
\cb3                 \cf6 \strokec6 "contents"\cf0 \strokec4 : [\{\cf6 \strokec6 "parts"\cf0 \strokec4 : [\{\cf6 \strokec6 "text"\cf0 \strokec4 : user_query\}]\}],\cb1 \
\cb3                 \cf6 \strokec6 "systemInstruction"\cf0 \strokec4 : \{\cf6 \strokec6 "parts"\cf0 \strokec4 : [\{\cf6 \strokec6 "text"\cf0 \strokec4 : system_prompt\}]\},\cb1 \
\cb3                 \cf6 \strokec6 "generationConfig"\cf0 \strokec4 : \{\cf6 \strokec6 "responseMimeType"\cf0 \strokec4 : \cf6 \strokec6 "application/json"\cf0 \strokec4 , \cf6 \strokec6 "responseSchema"\cf0 \strokec4 : schema\}\cb1 \
\cb3             \}\cb1 \
\cb3             \cb1 \
\cb3             options = \{\cb1 \
\cb3                 \cf6 \strokec6 'headers'\cf0 \strokec4 : \{\cf6 \strokec6 'Content-Type'\cf0 \strokec4 : \cf6 \strokec6 'application/json'\cf0 \strokec4 \},\cb1 \
\cb3                 \cf6 \strokec6 'body'\cf0 \strokec4 : json.dumps(payload)\cb1 \
\cb3             \}\cb1 \
\cb3             \cb1 \
\cb3             response = fetch_with_retry(api_url, options)\cb1 \
\cb3             \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  response:\cb1 \
\cb3                 \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3                     result = response.json()\cb1 \
\cb3                     text_content = result.get(\cf6 \strokec6 'candidates'\cf0 \strokec4 , [\{\}])[\cf7 \strokec7 0\cf0 \strokec4 ].get(\cf6 \strokec6 'content'\cf0 \strokec4 , \{\}).get(\cf6 \strokec6 'parts'\cf0 \strokec4 , [\{\}])[\cf7 \strokec7 0\cf0 \strokec4 ].get(\cf6 \strokec6 'text'\cf0 \strokec4 , \cf6 \strokec6 ''\cf0 \strokec4 )\cb1 \
\cb3                     \cb1 \
\cb3                     \cf2 \strokec2 if\cf0 \strokec4  text_content:\cb1 \
\cb3                         data = json.loads(text_content)\cb1 \
\cb3                         st.header(\cf6 \strokec6 "Generated Topics"\cf0 \strokec4 , divider=\cf6 \strokec6 "rainbow"\cf0 \strokec4 )\cb1 \
\cb3                         \cb1 \
\cb3                         \cf2 \strokec2 if\cf0 \strokec4  data.get(\cf6 \strokec6 "productBasedTopics"\cf0 \strokec4 ):\cb1 \
\cb3                             st.subheader(\cf6 \strokec6 "1. Product/Service Topics"\cf0 \strokec4 )\cb1 \
\cb3                             \cf2 \strokec2 for\cf0 \strokec4  product_data \cf2 \strokec2 in\cf0 \strokec4  data[\cf6 \strokec6 "productBasedTopics"\cf0 \strokec4 ]:\cb1 \
\cb3                                 create_topic_group(product_data.get(\cf6 \strokec6 'productName'\cf0 \strokec4 ), product_data.get(\cf6 \strokec6 'funnels'\cf0 \strokec4 , []), \cf6 \strokec6 'Product/Service'\cf0 \strokec4 )\cb1 \
\cb3                         \cb1 \
\cb3                         \cf2 \strokec2 if\cf0 \strokec4  data.get(\cf6 \strokec6 "timelyTopics"\cf0 \strokec4 ):\cb1 \
\cb3                             st.subheader(\cf6 \strokec6 "2. Timely & Event-Based Topics"\cf0 \strokec4 )\cb1 \
\cb3                             \cf2 \strokec2 for\cf0 \strokec4  event_data \cf2 \strokec2 in\cf0 \strokec4  data[\cf6 \strokec6 "timelyTopics"\cf0 \strokec4 ]:\cb1 \
\cb3                                 create_topic_group(event_data.get(\cf6 \strokec6 'eventName'\cf0 \strokec4 ), event_data.get(\cf6 \strokec6 'funnels'\cf0 \strokec4 , []), \cf6 \strokec6 'Event/Holiday'\cf0 \strokec4 )\cb1 \
\cb3                     \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3                         st.error(\cf6 \strokec6 "No content received from the API. The model may not have been able to generate a valid response."\cf0 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 except\cf0 \strokec4  (json.JSONDecodeError, IndexError, KeyError) \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3                     st.error(\cf6 \strokec6 f"Failed to parse the API response. Please try again. Error: \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3                  st.error(\cf6 \strokec6 "The request to the AI model failed. Please check the details and try again."\cf0 \strokec4 )\cb1 \
\
}