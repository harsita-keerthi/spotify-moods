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
    if not sp:
        return redirect(url_for('index'))
    
    track_ids = fetch_track_ids(sp)
    if not track_ids:
        return "No tracks found. Please save some tracks to your library."
    
    clusters = cluster_tracks(sp, track_ids)
    if clusters is not None:
        playlist_urls = create_mood_playlists(sp, track_ids, clusters)
    else:
        playlist_urls = []
    return render_template('create_playlist.html', playlist_urls=playlist_urls)

def fetch_track_ids(sp):
    track_ids = []
    try:
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track_ids.append(item['track']['id'])
        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                track_ids.append(item['track']['id'])
    except Exception as e:
        print(f"Error fetching track IDs: {e}")
    return track_ids

if __name__ == '__main__':
    app.run(debug=True)