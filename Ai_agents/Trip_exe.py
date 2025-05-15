from multi_agent import mood_finder,IDENTIFIER_PROMPT
from chat import Rag_chat,Agent_response
from Trip_search import Trip_searching
import streamlit as st
from PIL import Image
import base64



icon = Image.open("Travel_icon.png")
st.set_page_config(page_title="Tripify", page_icon=icon)

if 'history' not in st.session_state:
    st.session_state.history = []
    


def main():

    identifier = mood_finder(IDENTIFIER_PROMPT.format(user_input=user_input))
  

    if identifier.is_search:
        return Rag_chat(user_input)

    if identifier.is_Tripplan:
        Trip_response = Trip_searching(user_input)

        Agent_output = "".join(Agent_response(question=user_input, Agent=Trip_response))
        full_output = f"  🏨 Hotel, 🥪 Restaurants Recommendations And 🙋‍♂️ Etiquitte Manners:\n\n {Trip_response} \n\n---\n\n{Agent_output}"
        return full_output
        

   
if __name__ == "__main__":



    # --- Convert image to base64 string ---
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    image_base64 = get_base64_image("Travel_icon.png")
    
    #Animation CSS Inside streamlit.markdown():
    
       

    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
            background-size: 400% 400%;
            animation: fadeBackground 15s ease infinite;
        }

        @keyframes fadeBackground {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # --- Custom CSS for layout and components ---
    st.markdown("""
        <style>
            .main > div:first-child {
                padding-top: 0.5rem !important;
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            .response-box {
                background-color: #f0f0f0;
                border: 4px solid #555;
                border-radius: 30px;
                padding: 40px;
                min-height: 600px;
                overflow-y: auto;
                margin-bottom: 30px;
                width: 900px;
            }
            .message {
                margin-bottom: 10px;
                font-size: 16px;
            }
        
            .input-text {
                flex: 1;
                border: none;
                outline: none;
                font-size: 16px;
                padding: 8px;
                border-radius: 20px;
            }

            }
            .send-button:hover {
                background-color: #929292;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Header: Logo and Title ---
    col1, col2 = st.columns([1.12, 6])
    with col1:
        st.image("Travel_icon.png")

    with col2:
        st.markdown("""
            <div style='display: flex; align-items: center; height: 100%;'>
                <h1 style='margin: 0; font-size: 50px;'>Tripify</h1>
            </div>
        """, unsafe_allow_html=True)


        
    # --- Chat Input ---

    user_input = st.chat_input("Ask Tripify...") 
  
    # --- Session state for history ---
    
    if "history" not in st.session_state:
        st.session_state.history = []

    # --- Display user input and bot response ---

    if user_input:
        with st.chat_message("user",avatar="Trip_user_icon.png"):
            st.write(user_input)
        st.info("✍🏻  Planning Your Trip Please Wait...")

        with st.chat_message("Tripify",avatar="Travel_icon.png"):
           with st.spinner("🔍 Finding Best Recommendations..."):
              placeholder = st.empty()
              final_output = main()

              # Render final output in response box
              placeholder.markdown(final_output)

              # Save to history
              st.session_state.history.append((user_input, final_output))

    # --- Sidebar Recent Trips ---

    if st.session_state.history:
            st.sidebar.title("✈️ Recent Trips")
            for q, a in reversed(st.session_state.history[-5:]):
                with st.sidebar.expander(f"{q}"):
                    st.write(a)
