import openai
import pdfplumber

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

# pdf_data = \
# '''
# Advantages of Microcontrollers
# ● Due to the integration of all functional blocks in a single chip microcontroller IC,
# the size of the control board and power consumption are reduced, system
# reliability increased and provides more flexibility.
# ● The microcontroller is able to interface additional RAM, ROM and I/O ports for
# additional peripherals & memory and better software security.
# ● Once microcontrollers are programmed then they can be reprogrammed with
# some difficulty, so reusability exist.
# ● At the same time many tasks can be performed, so human effort can be saved.
# ● Easy trouble shooting &maintenance.
# ● Integrated circuits, such as the microcontroller, are much more dependable
# than relays. Before microcontrollers, control circuitry relied on many
# electromechanical relays and timers to control the system.
# '''

def chunk_string(text, max_chunk_size):
    print(len(text))
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
    # max_chunk_size = 100
    # input_chunks = [input_text[i:i+max_chunk_size] for i in range(0, len(input_text), max_chunk_size)]
    # generated_questions = []
    
    for chunk in input_chunks:
        prompt_text = \
            f'''
            You are a chatbot that creates quizzes for the user. Based on the input that is fed to you, you test the user in an interactive way. There should be a minimum of 5 questions and a maximum of 10. All the questions are in multiple-choice format. Wait for the user to answer before moving on to the next question.  You only reveal the answer after the user has responded. After responding to the user's answer, move to the next question immediately. 
            ```
            INPUT:
            {chunk}
            ```
            Human: Hi, can you test me based on the input given above ?
            AI: Sure ! Let's start the test.
            AI: 
            '''
        
        for i in range(4):
            
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_text,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.5,
            stop=["Human:"]
            )
            question = response.choices[0].text.strip()
            print(question)
            resp = input()
            prompt_text = prompt_text +question + "\nHuman: "+resp + "\nAI: "

            # giving answer feedback
            # response = openai.Completion.create(
            # model="text-davinci-003",
            # prompt=prompt_text,
            # temperature=0.7,
            # max_tokens=150,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0.5,
            # stop=["Human:"]
            # )
            # question = response.choices[0].text.strip()
            # print(question)

        # generated_questions.append(question)
    # return generated_questions

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


# data = generate_questions(prompt)
pdf_data = get_pdf_data("Module 5.pdf")
chunked = chunk_string(pdf_data,4000)
generate_questions(chunked)





