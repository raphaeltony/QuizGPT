import openai
import pdfplumber

openai.api_key = "<your-api-key>"
N = 5

# splitting the pdf data to smaller chunks
def chunk_string(text, max_chunk_size):
    chunks = []
    start_index = 0
    next_space_index = 0
    while start_index < len(text):
        end_index = start_index + max_chunk_size
        if end_index >= len(text):
            chunk = text[start_index:]
            chunks.append(chunk.strip())
            break
        else:
            next_space_index = text.rfind(" ", start_index, end_index)
            if next_space_index == -1 or next_space_index == start_index:
                next_space_index = end_index
            chunk = text[start_index:next_space_index]
        chunks.append(chunk.strip())
        start_index = next_space_index + 1
    return chunks


def generate_questions(input_chunks):
    for chunk in input_chunks:
        prompt_text = \
            f'''
            You conduct quizzes for the user. Based on the input that is fed to you, you test the user in the form of a Multiple Choice Question quiz. You reveal the answer only after the user has responded. In case the user makes an error, you show the correct answer to the user. You do not ask the same question again. All the questions are in multiple-choice format and only one choice is correct. There should be a minimum of 5 questions and a maximum of 20. You are truthful and friendly.
            INPUT:
            ```
            {chunk}
            ```
            '''
        msgs = [
                {"role": "system", "content": prompt_text },
                {"role": "user", "content": "Start the quiz"}
            ]
        
        for i in range(N):
            
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgs
            )
            question = ''
            for choice in response.choices:
                question += choice.message.content
            if(i==N-1):
                print("Last question in the chunk")
            print(question)
            resp = input()      #user response
            msgs.append({"role": "assistant", "content": f"{question}"})
            msgs.append({"role": "user", "content": f"{resp}"})


def get_pdf_data(filename):
    pdf = pdfplumber.open(filename)
    texts = []
    for page in pdf.pages:
        text = page.extract_text()
        texts.append(text)
    pdf.close()

    # Join all the texts in the list with a newline character
    text = "\n".join(texts)
    return text



pdf_data = get_pdf_data("Module 5.pdf")
chunked = chunk_string(pdf_data,1000)
generate_questions(chunked)





