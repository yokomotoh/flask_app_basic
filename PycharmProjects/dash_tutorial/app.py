# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html

from dash.dependencies import Input, Output, State
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import plotly.express as px

app = dash.Dash()
app.server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Applications/MAMP/db/sqlite/test.db"
db = SQLAlchemy(app.server)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, primary_key=False, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

@app.callback(
    #Output(component_id='my_output', component_property='children'),
    #Output("users", "children"),
    Output("table", "children"),
    Output('example-graph', 'figure'),
    [Input("add-button", "n_clicks")],
    [State("username", "value"), State("email", "value"), State("age", "value"), State("price", "value")],
)
def add_and_show_users(n, username, email, age, price):
    if n is not None:
        # if button clicked, add user
        db.session.add(User(username=username, email=email, age=age, price=price))
        db.session.commit()

    # get all users in database
    users = db.session.query(User).all()

    rows = []
    for user in users:
        rows.append([user.username, user.age])

    df = pd.DataFrame(rows, columns=["username", "age"])
    fig = px.bar(df, x="username", y="age", barmode="group")
    #fig.update_layout(transition_duration=500)

    return generate_table(), update_graph()
        #[
        ##html.Div([
        #    html.Div(
        #    [
        #        html.Span([html.H5("Username: "), u.username]),
        #        html.Span([html.H5("Email: "), u.email]),
        #    ]
        #    )
        #    for u in users
        ##])#,
        ##generate_table(db),
        ##fig
        #], generate_table(df), update_graph()

#def generate_table(dataframe, max_rows=5):
def generate_table():
    users = db.session.query(User).all()
    users_num = db.session.query(User).count()

    return html.Table([
        # html.Thead(
            # html.Tr([html.Th(col) for col in db.columns])
        #),
        html.Thead(
            html.Tr([html.Th("id"), html.Th("username"), html.Th("email"), html.Th("age"), html.Th("price")])
        ),
        html.Tbody([
            html.Tr([
                html.Th(col.id),
                html.Th(col.username),
                html.Th(col.email),
                html.Th(col.age),
                html.Th(col.price)
                ])
                for col in users
            ]) #for i in range(max_rows)
        ])

def update_graph():
    users = db.session.query(User).all()
    #df = pd.DataFrame({
    #    "username": ["yoko", "romain", "cecile"],#[user for user in users],
    #    "age": [21, 17, 14] #[user.age for user in users]
    #})
    rows = []
    for user in users:
        rows.append([user.username, user.age])

    df = pd.DataFrame(rows, columns=["username", "age"])
    fig = px.bar(df, x="username", y="age", barmode="group")
    fig.update_layout(transition_duration=500)

    return fig

'''
users = db.session.query(User).all()

rows = []
for user in users:
    rows.append([user.username, user.age])

df = pd.DataFrame(rows, columns=["username", "age"])
fig = px.bar(df, x="username", y="age", barmode="group")
fig.update_layout(transition_duration=500)
'''

app.layout = html.Div(id='my_output', children=
    [
        html.H4("username"),
        dcc.Input(id="username", placeholder="enter username", type="text"),
        html.H4("email"),
        dcc.Input(id="email", placeholder="enter email", type="email"),
        html.H4("age"),
        dcc.Input(id="age", placeholder="enter age", type="integer"),
        html.H4("price"),
        dcc.Input(id="price", placeholder="enter price", type="integer"),
        html.Button("add user", id="add-button"),
        html.Hr(),
        #html.H3("users"),
        #html.Div(id="users"),

        #generate_table(db),
        html.Div(id="table"),

        dcc.Graph(
            id='example-graph',
            # figure=fig
            #figure=update_graph()
        )
    ]
)

if __name__ == "__main__":
    db.create_all()
    app.run_server()