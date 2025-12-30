# Talking with an Image Web Application

# Import necessary libraries
import os
import streamlit as st
import google.generativeai as genai


def ask_and_get_answer(prompt, image):
    """Function to get an answer from the Generative AI model based on a prompt and an image."""
    model = genai.GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content([prompt, image])
    
    return response.text

def st_image_to_pil(image_file):
    """Convert a Streamlit uploaded image file to a PIL image."""
    from PIL import Image
    import io
    
    image_data = image_file.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

answer = ''

if __name__ == "__main__":
    # Configure the Generative AI API with the API key from environment variables
    genai.configure(api_key=st.secrets["GENAI_API_KEY"])
    
    # Set up the Streamlit web application
    st.image("gemini.png")
    st.subheader("Talking with an Image")
    
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if img:
        st.image(img, caption='Talk with this image.')
        
        prompt = st.text_area('Ask a question about this image: ')
        if prompt:
            pil_image = st_image_to_pil(img)
            with st.spinner('Generating answer...'):
                answer = ask_and_get_answer(prompt, pil_image)
                st.text_area('Gemini:', value=answer, height=200)
            
            st.divider()
        
        if 'history' not in st.session_state:
            st.session_state['history'] = []
            
        value = f'Q: {prompt}\nA: {answer}'
        st.session_state.history = f'{value} \n\n {"-"*100} \n\n {st.session_state.history}'
        
        h = st.session_state.history
        st.text_area(label='Conversation History:', value=h, height=400, key='history')
        