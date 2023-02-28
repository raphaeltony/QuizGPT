import openai
import pdfplumber

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

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
            You are a chatbot that creates quizzes for the human. Based on the input that is fed to you, you test the human in an interactive way. You reveal the answer only after the human has responded. In case the human makes an error, you show the correct answer to the human. You do not ask the same question again. All the questions are in multiple-choice format and only one choice is correct. There should be a minimum of 5 questions and a maximum of 20. Wait for the human to answer before moving on to the next question.  You are truthful and friendly.
            ```
            INPUT:
            Neil Armstrong, Buzz Aldrin, Michael Collins, and Yuri Gagarin were all astronauts. On July 20, 1969, Neil Armstrong was the first to step onto the moon followed by Buzz Aldrin.
            \nThe skin is the biggest organ in the body.
            {chunk}
            ```
            Human: Hi, can you test me based on the input given above ?
            AI: Sure ! Let's start the test.
            
            AI: Question: Who was the first man to walk on the moon?
            A) Neil Armstrong
            B) Buzz Aldrin
            C) Michael Collins
            D) Yuri Gagarin

            Please select your answer by typing the letter corresponding to the correct answer (e.g. A, B, C or D) below:
            Human: a

            AI: Your answer is: A
            Correct! Neil Armstrong was the first man to walk on the moon on July 20, 1969. 

            Here's another question:

            AI: Question: What is the largest organ in the human body?
            A) Liver
            B) Heart
            C) Skin
            D) Lungs

            Please select your answer by typing the letter corresponding to the correct answer (e.g. A, B, C or D) below:
            Human: b

            AI: Your answer is: B
            Incorrect! Skin is the largest organ in the human body

            Here's another question:
            '''
        
        for i in range(10):
            
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_text,
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.5,
            stop=["Human:"]
            )
            question = response.choices[0].text.strip()
            print(question)
            resp = input()      #user response
            prompt_text = prompt_text +question + "\nHuman: "+resp + "\nAI: "   #appending question and response to prompt for future context


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





