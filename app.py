from flask import Flask, session, request, redirect, url_for, render_template
from spotify_auth import create_spotify_auth, get_spotify_client
from mood_clustering import cluster_tracks, create_mood_playlists

app = Flask(__name__)
app.secret_key = "random_secret_key"
app.config['SESSION_COOKIE_NAME'] = 'spotify-auth-session'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_auth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_auth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('create_playlist'))

@app.route('/create_playlist')
def create_playlist():
    sp = get_spotify_client()
    track_ids = []
    clusters = cluster_tracks(sp, track_ids)
    playlist_urls = create_mood_playlists(sp, track_ids, clusters)
    return render_template('create_playlist.html', playlist_urls=playlist_urls)

if __name__ == '__main__':
    app.run(debug=True)