from app import app
from dash import dcc
from dash import html
import openai
from dash.dependencies import Input, Output, State

# Set up OpenAI API key
openai.api_key = "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"

# Define the layout for the Dona's Diagnosis page
dona_layout = html.Div([
    html.H1("Dona's Diagnosis"),
    dcc.Input(id='question-input', type='text',
              placeholder='Ask Dona a question...'),
    html.Button('Submit', id='submit-question'),
    html.Div(id='answer-output')
])


@app.callback(Output('answer-output', 'children'),
              [Input('submit-question', 'n_clicks')],
              [State('question-input', 'value')])
def generate_answer(n_clicks, question):
    if not question:
        return html.P("Please ask a question.")
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Patient: {question}\nDona:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return html.P(answer)
