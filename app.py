from flask import Flask, request, render_template
import openai
import requests
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mainkw = request.form.get("mainkw")
        additionalkw = request.form.get("additionalkw")
        language = request.form.get("language")
        geo = request.form.get("geo")
        tone = request.form.get("tone")
        style = request.form.get("style")
        intent = request.form.get("intent")
        openai.api_key = "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"
        key_points = additionalkw.split(",")


        #----------------- main section promt ----------------------
        main_prompt = (f"<p>Write an {tone} article with a {style} tone on the topic '{mainkw}' in {language}"
                  f"based up on the {geo} market"
                  f"providing a analysis that includes {additionalkw}</p>")
        model = "text-davinci-003"
        main_completions = openai.Completion.create(
            engine=model,
            prompt=main_prompt,
            max_tokens=1000,
            n=10,
            stop=None,
            temperature=0.5,
        )
        
        message=list()
        for i in range(2):
            message.append(main_completions.choices[i].text)

        #----------------- Heading section promt ----------------------

        headings_array= []  
        headings_array.append(mainkw) 

        prompt1 = (f"heading from google competitors top ranking articles h2,h3,h4 based on the topic {mainkw} in {language}\n")
        completions1 = openai.Completion.create(
            engine=model,
            prompt=prompt1,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message1 = completions1.choices[0].text
        message1 ='<p style="white-space: pre-wrap">{}</p>'.format(message1)
        message4 = message1.split('\n')
        heading_variable=""
        message3=""
        count=0
        for heading in message4:    
            if heading not in headings_array:        
                if "H2" in heading:
                    headings_array.append(heading) 
                    heading=heading.replace("H2:", " ")
                    my_var_without_spaces = heading.replace(" ", "")
                    if len(my_var_without_spaces) < 4:
                        heading_variable="H2"
                    else:
                        heading_variable="H2"
                        message3 +='<center><h2>{}</h2></center>'.format(heading)
                        sub_prompt =  (f"<p>Write an {tone} article with a {style} tone on the topic '{heading}' in {language}"
                                        f"based up on the {geo} market"
                                        f"providing a analysis that includes {additionalkw}</p>")
                        sub_completions1 = openai.Completion.create(
                            engine=model,
                            prompt=sub_prompt,
                            max_tokens=4000,
                            n=1,
                            stop=None,
                            temperature=0.5,
                        )
                        sub_message = sub_completions1.choices[0].text
                        message3 +='<p style="white-space: pre-wrap">{}</p>'.format(sub_message)
                        count=count+1
                    
                elif  "H3" in heading:
                    heading=heading.replace("H3:", " ")
                    my_var_without_spaces = heading.replace(" ", "")
                    if len(my_var_without_spaces) < 4:
                        heading_variable="H3"
                    else:
                        heading_variable="H3"
                        message3 +='<center><h3>{}</h3></center>'.format(heading)
                        sub_prompt =  (f"<p>Write an {tone} article with a {style} tone on the topic '{heading}' in {language}"
                                        f"based up on the {geo} market"
                                        f"providing a analysis that includes {additionalkw}</p>")
                        sub_completions1 = openai.Completion.create(
                            engine=model,
                            prompt=sub_prompt,
                            max_tokens=4000,
                            n=1,
                            stop=None,
                            temperature=0.5,
                        )
                        sub_message = sub_completions1.choices[0].text
                        message3 +='<p style="white-space: pre-wrap">{}</p>'.format(sub_message)
                        count=count+1

                elif  "H4" in heading:
                    heading=heading.replace("H4:", " ")
                    my_var_without_spaces = heading.replace(" ", "")
                    if len(my_var_without_spaces) < 4:
                        heading_variable="H4"
                    else:
                        heading_variable="H4"
                        message3 +='<center><h4>{}</h4></center>'.format(heading)
                        sub_prompt =  (f"<p>Write an {tone} article with a {style} tone on the topic '{heading}' in {language}"
                                        f"based up on the {geo} market"
                                        f"providing a analysis that includes {additionalkw}</p>")
                        sub_completions1 = openai.Completion.create(
                            engine=model,
                            prompt=sub_prompt,
                            max_tokens=4000,
                            n=1,
                            stop=None,
                            temperature=0.5,
                        )
                        sub_message = sub_completions1.choices[0].text
                        message3 +='<p style="white-space: pre-wrap">{}</p>'.format(sub_message)
                        count=count+1
                else:
                    my_var_without_spaces = heading.replace('<p style="white-space: pre-wrap">', "")
                    if len(my_var_without_spaces) > 4:
                        message3 +='<center><{}>{}</{}></center>'.format(heading_variable, heading, heading_variable)
                        sub_prompt =  (f"<p>Write an {tone} article with a {style} tone on the topic '{heading}' in {language}"
                                            f"based up on the {geo} market"
                                            f"providing a analysis that includes {additionalkw}</p>")
                        sub_completions1 = openai.Completion.create(
                            engine=model,
                            prompt=sub_prompt,
                            max_tokens=4000,
                            n=1,
                            stop=None,
                            temperature=0.5,
                        )
                        sub_message = sub_completions1.choices[0].text
                        message3 +='<p style="white-space: pre-wrap">{}</p>'.format(sub_message)
                        count=count+1
                
            if count > 6 :
                break
                


        #----------------- FAQ section promt ----------------------

        prompt2 = f"5 FAQ questions and answers for writing blog about the topic {mainkw} in {language}\n"
        completions2 = openai.Completion.create(
            engine=model,
            prompt=prompt2,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        
        message2 = completions2.choices[0].text
        message2 ='<p style="white-space: pre-wrap">{}</p>'.format(message2)


        #----------------- Competitor section promt ----------------------

        message5 =""
        google_url = f'https://www.google.com/search?q={mainkw}&num=6'
        response = requests.get(google_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith('/url?q='):
                url = href[7:].split('&')[0]
                links.append(url)
        competitors={}
        for i, url in enumerate(links[:6]):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            if headings:
                for j, heading in enumerate(headings):
                    similarity_ratio = SequenceMatcher(None, mainkw, heading.text).ratio()
                    if similarity_ratio > 0.25:
                        competitors[url]=heading.text.strip()
            else:
                print(' ')
        keys=list(competitors)
        message5=competitors
        return render_template("result.html", mainkw=mainkw, additionalkw=additionalkw,headings_array=headings_array,message=message,message1=message1,message2=message2,message3=message3,message5=message5)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)