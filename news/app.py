from flask import Flask, request, render_template
import os
import sys
import urllib.request
import json
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = "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"

client_id = "rn3olXgLb4T5hiRgd02C"
client_secret = "qyfIe7VXwM"

def generate_summary(text, keyword):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please summarize the following news content, and delete the word </b> in your summary. '{keyword}': {text}",
        max_tokens=700,
        n=1,
        stop=None,
        temperature=0.50,
    )

    message = response.choices[0].text.strip()
    return message

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        search_keyword = request.form['search_keyword']
        encText = urllib.parse.quote(search_keyword)
        url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=7&start=1"

        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", client_id)
        req.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(req)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            news_data = json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)

        news_contents = " ".join([item["title"] + ". " + item["description"] for item in news_data["items"]])
        summary = generate_summary(news_contents, search_keyword)

    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
