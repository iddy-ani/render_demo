# Import necessary libraries
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import json
import random


with open('questions.json') as f:
    quiz = json.load(f)

game_layout = html.Div(
    [
        html.H2("Ava's Puzzle Pursuit", style={'color': 'black', 'text-align': 'center'}),
        dcc.Store(id='store', storage_type='memory'),  # for keeping the score and current question
        dcc.Dropdown(
            id='genre',
            options=[{'label': i, 'value': i} for i in quiz.keys()],
            placeholder="Select a genre",
            disabled=False,
            style={'width': '200px', 'margin-bottom': '20px', 'color': 'black'}
        ),
        html.P("Answer as many questions correctly as you can:", style={'color': 'black', 'font-size': '20px'}),
        html.P(id='question', style={'color': 'black', 'font-size': '24px', 'font-weight': 'bold'}),
        dcc.RadioItems(
            id='options',
            style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'}
        ),
        html.Button(
            'Submit',
            id='submit-val',
            n_clicks=0,
            style={
                'margin-top': '20px',
                'background-color': '#9370DB',
                'color': 'white',
                'padding': '10px 20px',
                'border': 'none',
                'border-radius': '5px',
                'cursor': 'pointer',
                'font-size': '16px'
            }
        ),
        html.Div(
            id='container-button-basic',
            children='Select an option and submit.',
            style={'color': 'black', 'font-size': '16px'}
        ),
        html.Button(
            'Next question',
            id='next-question',
            n_clicks=0,
            style={
                'margin-top': '20px',
                'background-color': '#9370DB',
                'color': 'white',
                'padding': '10px 20px',
                'border': 'none',
                'border-radius': '5px',
                'cursor': 'pointer',
                'font-size': '16px'
            }
        ),
        html.H3(
            id='score',
            style={'color': 'black', 'font-size': '28px', 'font-weight': 'bold', 'margin-top': '20px'}
        ),
        html.Button(
            'Start New Game',
            id='new-game',
            n_clicks=0,
            style={
                'display': 'none',
                'background-color': '#9370DB',
                'color': 'white',
                'padding': '10px 20px',
                'border': 'none',
                'border-radius': '5px',
                'cursor': 'pointer',
                'font-size': '16px'
            }
        ),
        html.Button(
            'Restart',
            id='restart',
            n_clicks=0,
            style={
                'margin-top': '20px',
                'background-color': '#9370DB',
                'color': 'white',
                'padding': '10px 20px',
                'border': 'none',
                'border-radius': '5px',
                'cursor': 'pointer',
                'font-size': '16px'
            }
        )
    ],
    style={
        'background-image': "url('/static/images/background_img.jpeg')",
        'background-size': 'cover',
        'background-position': 'center',
        'height': '90vh',
        'padding': '20px',
        'color': 'black'
    }
)



@app.callback(
    [
        Output('store', 'data'),
        Output('question', 'children'),
        Output('options', 'options'),
        Output('options', 'value'),
        Output('container-button-basic', 'children'),
        Output('score', 'children'),
        Output('genre', 'disabled')
    ],
    [
        Input('submit-val', 'n_clicks'),
        Input('next-question', 'n_clicks'),
        Input('genre', 'value'),
        Input('restart', 'n_clicks')
    ],
    [
        State('options', 'value'),
        State('store', 'data')
    ]
)
def update_output(n_submit, n_next, genre, restart_clicks, value, data):
    from dash import callback_context

    if not data:
        data = {
            'score': 0,
            'current_question': 0,
            'correct_answers': [],
            'attempted_questions': [],
            'selected_genre': None,
            'question_order': []
        }

    if not genre:
        return (
            data,
            "Please select a genre to start the game.",
            [],
            None,
            '',
            f'Score: {data["score"]}',
            False
        )

    # Check if the restart button is clicked
    if callback_context.triggered[0]['prop_id'].split('.')[0] == 'restart':
        data = {
            'score': 0,
            'current_question': 0,
            'correct_answers': [],
            'attempted_questions': [],
            'selected_genre': genre,
            'question_order': []
        }
        return (
            data,
            "Please select a genre to start the game.",
            [],
            None,
            '',
            f'Score: {data["score"]}',
            False
        )

    # Update the selected genre if it has been changed
    if genre and genre != data['selected_genre']:
        data['selected_genre'] = genre
        data['current_question'] = 0
        data['question_order'] = random.sample(range(len(quiz[genre])), len(quiz[genre]))

    question_index = data['question_order'][data['current_question']]
    question = quiz[genre][question_index]

    if callback_context.triggered[0]['prop_id'].split('.')[0] == 'next-question':
        data['current_question'] += 1
        if data['current_question'] < len(quiz[genre]):
            question_index = data['question_order'][data['current_question']]
            question = quiz[genre][question_index]
        else:
            return (
                data,
                "You've finished all the questions in this genre!",
                [],
                None,
                '',
                f'Score: {data["score"]}',
                False
            )
        return (
            data,
            f'Question: {question["question"]}',
            [{'label': i, 'value': i} for i in question['options']],
            None,
            'Select an option and submit.',
            f'Score: {data["score"]}',
            False
        )
    elif callback_context.triggered[0]['prop_id'].split('.')[0] == 'submit-val':
        if question_index not in data['attempted_questions']:
            data['attempted_questions'].append(question_index)
            if question['answer'] == value:
                data['score'] += 1
                data['correct_answers'].append(question_index)
                return (
                    data,
                    f'Question: {question["question"]}',
                    [{'label': i, 'value': i} for i in question['options']],
                    None,
                    f'Correct! The answer is {question["answer"]}.',
                    f'Score: {data["score"]}',
                    True
                )
            else:
                return (
                    data,
                    f'Question: {question["question"]}',
                    [{'label': i, 'value': i} for i in question['options']],
                    None,
                    f'Sorry, your answer {value} is incorrect. The correct answer is {question["answer"]}.',
                    f'Score: {data["score"]}',
                    True
                )
        else:
            return (
                data,
                f'Question: {question["question"]}',
                [{'label': i, 'value': i} for i in question['options']],
                None,
                'This question has already been attempted. Please move on to the next question.',
                f'Score: {data["score"]}',
                True
            )
    return (
        data,
        f'Question: {question["question"]}',
        [{'label': i, 'value': i} for i in question['options']],
        None,
        'Select an option and submit.',
        f'Score: {data["score"]}',
        True
    )


# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
