```markdown
# InquAIre Chatbot

Welcome to the **InquAIre** chatbot project! This application leverages the Groq API to compare responses from multiple AI models in real time, enabling users to interact with and evaluate different models simultaneously.

## Features

- **Real-time Chat**: Users can input prompts and receive immediate responses from multiple AI models.
- **Model Selection**: Choose from four different AI models for comparison.
- **Multithreading Support**: Simultaneous handling of requests for efficient response streaming.
- **User-Friendly Interface**: Streamlit provides an interactive web interface for easy usage.

## Getting Started

### Prerequisites

- Python 3.x
- Streamlit
- Groq API access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inquaire-chatbot.git
   cd inquaire-chatbot
   ```

2. Install the required packages:
   ```bash
   pip install streamlit groq
   ```

3. Set up your API key:
   - Create a text file containing your Groq API key and provide the file path in the `api_key_file_path` variable in the code.

### Running the Chatbot

Run the following command to start the Streamlit app:
```bash
streamlit run app.py
```

### Usage

1. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).
2. Select your desired AI models from the dropdown menus.
3. Enter your prompt in the text input field and view the responses from the selected models in real time.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Groq](https://www.groq.com) for providing the AI model API.
- [Streamlit](https://streamlit.io) for the interactive web framework.
```
