from g4f.client import Client

def generer_reponses(cv, preprompt, question):
    prompt = preprompt+ "{"+ question + "?" +"}"+ "\n" + cv

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        provider="OIVSCode Blackbox ChatGpt ChatGptEs DDG",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )

    return response.choices[0].message.content