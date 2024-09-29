import streamlit as st
from typing import Generator
from groq import Groq

# Set up Streamlit page configuration
st.set_page_config(layout="wide", page_title="Welcome to my chatbot!")

# Display app title
st.subheader ("InquAIre", anchor=False)

# Define path for API key file
api_key_file_path = "enter your file path"

# Read API key from file
try:
    with open(api_key_file_path, "r") as file:
        api_key = file.read().strip()
except FileNotFoundError:
    st.error("API key file not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

if not api_key:
    st.error("API key is not set. Please ensure the key is in the file.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize chat history and model selections for each column
default_models = ["mixtral-8x7b-32768", "llama3-70b-8192", "llama3-8b-8192", "gemma-7b-it"]
model_keys = ["selected_model_col1", "selected_model_col2", "selected_model_col3", "selected_model_col4"]

# Set default values for session state if not already set
for key in ["messages"] + model_keys:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "messages" else default_models[model_keys.index(key)]

# Define chatbot models with their details
models = {
    "mixtral-8x7b-32768": {"name": "ChatGPT", "tokens": 32768, "developer": "Mistral"},
    "llama3-70b-8192": {"name": "Copilot", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "Meta AI", "tokens": 8192, "developer": "Meta"},
    "gemma-7b-it": {"name": "Gemini AI", "tokens": 8192, "developer": "Google"},
}

# Function to select a chatbot model for a given column
def select_chatbot(column, column_name, default_index):
    with column:
        return st.selectbox(
            f"Choose a chatbot for {column_name}:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=default_index
        )

# Create four columns for chatbots
col1, col2, col3, col4 = st.columns(4)

# Get selected models for each column
model_option_col1 = select_chatbot(col1, "Column 1", 0)
model_option_col2 = select_chatbot(col2, "Column 2", 1)
model_option_col3 = select_chatbot(col3, "Column 3", 2)
model_option_col4 = select_chatbot(col4, "Column 4", 3)

# Function to detect and handle model changes
def detect_model_change(model_option, column_key):
    if st.session_state.get(column_key) != model_option:
        st.session_state.messages = []
        st.session_state[column_key] = model_option

# Detect model changes for all columns
model_options = [model_option_col1, model_option_col2, model_option_col3, model_option_col4]
column_keys = model_keys
for model_option, column_key in zip(model_options, column_keys):
    detect_model_change(model_option, column_key)

# Display previous messages from chat history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input area for user prompt (moved below the chat replies)
prompt = st.text_input("Enter your prompt here...", "")

# Function to generate chat responses from API
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Function to create chat completion for a given model
    def create_chat_completion(model_option):
        return client.chat.completions.create(
            model=model_option,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=models[model_option]["tokens"],
            stream=True
        )

    # Create chat completions for all four models
    chat_completions = {
        "col1": create_chat_completion(model_option_col1),
        "col2": create_chat_completion(model_option_col2),
        "col3": create_chat_completion(model_option_col3),
        "col4": create_chat_completion(model_option_col4)
    }

    # Function to handle response display and update chat history
    def display_chat_response(column, model_option, chat_completion, column_key):
        with column:
            st.write(f"Response from {models[model_option]['name']}")
            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)

            # Update chat history based on response type
            if isinstance(full_response, str):
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                combined_response = "\n".join(str(item) for item in full_response)
                st.session_state.messages.append({"role": "assistant", "content": combined_response})

    # Create a container to organize chat responses in columns
    response_container = st.container()
    with response_container:
        response_col1, response_col2, response_col3, response_col4 = st.columns(4)
        response_columns = [(response_col1, model_option_col1, chat_completions["col1"]),
                            (response_col2, model_option_col2, chat_completions["col2"]),
                            (response_col3, model_option_col3, chat_completions["col3"]),
                            (response_col4, model_option_col4, chat_completions["col4"])]

        for column, model_option, chat_completion in response_columns:
            display_chat_response(column, model_option, chat_completion, model_keys[response_columns.index((column, model_option, chat_completion))])