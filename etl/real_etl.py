from flask import Flask, request, redirect, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

SPOTIPY_CLIENT_ID = os.environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'  # Match the registered redirect URI
SPOTIPY_SCOPE = 'user-top-read'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE)

@app.route('/')
def home():
    return '<a href="/login">Log in with Spotify</a>'

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect('/top_artists')

from flask import render_template

# ...

@app.route('/top_artists')
def top_artists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/login')

    sp = Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=30, time_range='short_term')

    # Convert the top artists data to a Pandas DataFrame
    selected_fields = []
    for artist in top_artists['items']:
        artist_info = {
            'Name': artist['name'],
            'Genres': ', '.join(artist['genres']),
            'Popularity': artist['popularity'],
            'URL': artist['external_urls']['spotify'],
        }
        selected_fields.append(artist_info)

    # Create the DataFrame
    df = pd.DataFrame(selected_fields)

    # Sort the DataFrame by popularity
    df_sorted = df.sort_values(by='Popularity', ascending=False)
    print(df_sorted)

    # Save the DataFrame to a CSV file
    csv_filename = 'top_artists.csv'
    df_sorted.to_csv(csv_filename, index=False)

    # Render the DataFrame as HTML using Flask's render_template
    return render_template('top_artists.html', top_artists=df_sorted.to_html(index=False))
    


if __name__ == '__main__':
    app.run(debug=True)
