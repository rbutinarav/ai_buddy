# AI Buddy

Welcome to AI Buddy, a chatbot built with OpenAI, Python, and Streamlit. AI Buddy can interact with you using different personas, including historical figures like Leonardo Da Vinci, Albert Einstein, and Nelson Mandela. The chatbot is also able to remember past conversations and speak with its own voice. 

## Features

- Implement a chatbot with OpenAI
- Different personas can be selected to change the chatbot's personality
- Conversations can be saved to a remote blob storage
- Answers can be directly converted to speech using Azure Cognitive Services (experimental, currently only working locally for deployment issues)

## On the way

- Full text-to-speech and speech-to-text integration
- Advanced context and personalization of personas for a personalized experience
- Memory of previous conversations
- Document search capabilities on local storage

## Future implementation

- Web search (using langchain)
- Emailing/texting/social posting capabilities
- User authentication (for limited public release)

## Usage

1. Clone the repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run the application using `streamlit run app.py`
4. Select a persona and start chatting with AI Buddy

## Contributing

Contributions are welcome! If you have any suggestions or want to report a bug, please open an issue or a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.