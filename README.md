# QuizGPT

A CLI chatbot that creates an interactive quiz based on the contents of the PDF document you pass to it. It runs on Python and uses GPT-3 and the OpenAI API.

> The program is prone to hallucinate and may not always give 100% accurate answers. Use it for educational and entertainment purposes only.
> The same has been implemented using the ChatGPT API. Switch to branch `chatgptapi`
## How the program works

- The Python program fetches the data from a pdf you choose.
- Then it uses a predefined prompt to interact with GPT-3 using the OpenAI API
- The responses are shown to the user in the format of an MCQ quiz
- The user's answers are appended to the prompt and the API is used again to fetch a response

## Pre-requisites
- Personal OpenAI API keys. Sign up [here](https://platform.openai.com/account/api-keys). Click on View API Keys and paste the key in the `main.py` file

- Python

- Necessary packages (openai and pdfplumber) :

```
pip install -r requirements.txt

```

## Running the program
- Clone the repository and navigate to the folder
- Install the required python packages (Check previous section)
- Place your pdf file in the same directory as your repository
- Add your pdf filename and OpenAI API keys to `main.py` 
- Run `main.py`
