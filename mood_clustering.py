from sklearn.cluster import KMeans
import numpy as np

def get_audio_features(sp, track_ids):
    try: 
        features = sp.audio_features(tracks=track_ids)
        print(f"Fetched audio features: {features}")
        if features is None:
            print(f"No audio features found for track IDs: {track_ids}")
            return np.array([])
        return np.array([[f['danceability'], f['energy'], f['valence']] for f in features])
    except Exception as e:
        print(f"Error fetching audio features: {e}")
        return np.array([])

def cluster_tracks(sp, track_ids, n_clusters=3):
    features = get_audio_features(sp, track_ids)
    if features.size == 0:
        print("No features available for clustering.")
        return None
    try:
        kmeans = KMeans(n_clusters=n_clusters)
        clusters = kmeans.fit_predict(features)
        return clusters
    except Exception as e:
        print(f"Error during clustering: {e}")
        return None

def create_mood_playlists(sp, track_ids, clusters, n_clusters=3):
    playlists = []
    user_id = sp.current_user()['id']

    for i in range(n_clusters):
        mood_tracks = [track_ids[j] for j in range (len(track_ids)) if clusters[j] == i]
        playlist = sp.user_playlists_create(user_id, f"Mood {i+1} Playlist")
        sp.user_playlist_add_tracks(user_id, playlist['id'], mood_tracks)
        playlists.append(playlist['external_urls']['spotify'])

    return playlists