import pdfplumber
# Open the PDF file

pdf = pdfplumber.open("Module 5.pdf")

# Create an empty list to store texts
texts = []

# Loop through all pages
for page in pdf.pages:

    # Extract text from the page
    text = page.extract_text()

    # Append the text to the list
    texts.append(text)

# Close the PDF file
pdf.close()

# Join all the texts in the list with a newline character
text = "\n".join(texts)

# Print the text
# print(text)
with open("final.txt", "w", encoding="utf-8") as f:
    f.write(text)
