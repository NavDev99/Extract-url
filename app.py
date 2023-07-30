from flask import Flask, request
import docx2txt
import re
import base64

app = Flask(__name__)

@app.route('/extract-urls', methods=['POST'])
def extract_urls():
    base64_string = request.data.decode('utf-8')  # Decode byte string to Base64 string
    
    # Decode the Base64 string back into binary data
    doc_data = base64.b64decode(base64_string)

    # Save temporary file
    temp_filename = "temp.docx"
    with open(temp_filename, 'wb') as f:
        f.write(doc_data)

    # Extract text from the document
    doc_text = docx2txt.process(temp_filename)
    print("Extracted text:", doc_text)  # Print out the extracted text for debugging

    # Find all URL-like substrings in the document text
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', doc_text)
    print("Extracted URLs:", urls)  # Print out the extracted URLs for debugging

    # Return the list of URLs
    return {'urls': urls}

if __name__ == '__main__':
    app.run(debug=True)
