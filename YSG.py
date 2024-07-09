import streamlit as st
import requests
import os

# Get the API key from the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Set up the Streamlit app
st.title('YouTube Script Generator')
st.write('Create High-Quality YouTube Scripts Quickly and Easily!')

# Custom CSS for button styling
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #1f3a93;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
    }
    .stButton > button:hover {
        background-color: #3c6382;
        color: white;
    }
    .stButton > button:active {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input fields
user_input = st.text_area('Enter your idea:', height=80)
minutes = st.number_input('Select video length (minutes):', min_value=0, max_value=120, value=0, step=1)
seconds = st.number_input('Select video length (seconds):', min_value=0, max_value=59, value=0, step=1)

# Generate script button and spinner
if st.button('Generate Script'):
    if user_input:
        with st.spinner('Generating script...'):
            video_length = f"{minutes} minutes and {seconds} seconds"
            prompt = f"""As an expert copywriter specialized in YouTube script writing, your task is to create an engaging and informative script for a YouTube video. The video will cover the topic of {user_input}. The script should be for a video length of {video_length}. The output must be only the generated script."""

            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    candidates = response_data.get('candidates', [])

                    script_list = []
                    for candidate in candidates:
                        content = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
                        script_list.append(content)

                    # Display script
                    script_placeholder = st.empty()
                    script_placeholder.markdown('\n\n'.join(script_list))

                except Exception as e:
                    st.error('Error parsing response. Please try again.')
            else:
                st.error(f'Error generating script: {response.status_code} - {response.text}')
    else:
        st.warning('Please enter your idea.')
