# Import necessary libraries
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import json


with open('questions.json') as f:
    quiz = json.load(f)

game_layout = html.Div([
    html.H2("Ava's Puzzle Pursuit"),
    dcc.Store(id='store', storage_type='memory'),  # for keeping the score and current question
    dcc.Dropdown(
    id='genre',
    options=[{'label': i, 'value': i} for i in quiz.keys()],
    placeholder="Select a genre"
    ),
    html.P("Try to answer the question:"),
    html.P(id='question'),
    dcc.RadioItems(
        id='options'
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic', children='Select an option and submit.'),
    html.Button('Next question', id='next-question', n_clicks=0),
    html.H3(id='score'),
    html.Button('Start New Game', id='new-game', n_clicks=0, style={'display': 'none'})
],
    style={
        # 'background-image': "url(background_img.jpeg)",
        'background-size': 'cover',
        'background-position': 'center',
        'height': '90vh',
        'padding': '20px',
        "background-color": "#9370DB"
    })

@app.callback(
    [Output('store', 'data'),
     Output('question', 'children'),
     Output('options', 'options'),
     Output('options', 'value'),
     Output('container-button-basic', 'children'),
     Output('score', 'children')],
    [Input('submit-val', 'n_clicks'),
     Input('next-question', 'n_clicks'),
     Input('genre', 'value')],
    [State('options', 'value'),
     State('store', 'data')]
)
def update_output(n_submit, n_next, genre, value, data):
    from dash import callback_context

    if not data:
        data = {'score': 0, 'current_question': 0, 'correct_answers': [], 'attempted_questions': [], 'selected_genre': None}

    if not genre:
        return data, "Please select a genre to start the game.", [], None, '', f'Score: {data["score"]}'

    # Update the selected genre if it has been changed
    if genre and genre != data['selected_genre']:
        data['selected_genre'] = genre
        data['current_question'] = 0

    question = quiz[data['selected_genre']][data['current_question']]

    if callback_context.triggered[0]['prop_id'].split('.')[0] == 'next-question':
        data['current_question'] += 1
        if data['current_question'] < len(quiz[data['selected_genre']]):
            question = quiz[data['selected_genre']][data['current_question']]
        else:
            return data, "You've finished all the questions in this genre!", [], None, '', f'Score: {data["score"]}'
        return data, f'Question: {question["question"]}', [{'label': i, 'value': i} for i in question['options']], None, 'Select an option and submit.', f'Score: {data["score"]}'
    elif callback_context.triggered[0]['prop_id'].split('.')[0] == 'submit-val':
        if data['current_question'] not in data['attempted_questions']:
            data['attempted_questions'].append(data['current_question'])
            if question['answer'] == value:
                data['score'] += 1
                data['correct_answers'].append(data['current_question'])
                return data, f'Question: {question["question"]}', [{'label': i, 'value': i} for i in question['options']], None, f'Correct! The answer is {question["answer"]}.', f'Score: {data["score"]}'
            else:
                return data, f'Question: {question["question"]}', [{'label': i, 'value': i} for i in question['options']], None, f'Sorry, your answer {value} is incorrect. The correct answer is {question["answer"]}.', f'Score: {data["score"]}'
        else:
            return data, f'Question: {question["question"]}', [{'label': i, 'value': i} for i in question['options']], None, 'This question has already been attempted. Please move on to the next question.', f'Score: {data["score"]}'
    return data, f'Question: {question["question"]}', [{'label': i, 'value': i} for i in question['options']], None, 'Select an option and submit.', f'Score: {data["score"]}'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
