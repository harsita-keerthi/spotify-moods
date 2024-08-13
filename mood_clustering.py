from sklearn.cluster import KMeans
import numpy as np

def get_audio_features(sp, track_ids):
    features = sp.audio_features(tracks=track_ids)
    return np.array([[f['danceability'], f['energy'], f['valence']] for f in features])

def cluster_tracks(sp, track_ids, n_clusters=3):
    features = get_audio_features(sp, track_ids)
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(features)
    return clusters

def create_mood_playlists(sp, track_ids, clusters, n_clusters=3):
    playlists = []
    user_id = sp.current_user()['id']

    for i in range(n_clusters):
        mood_tracks = [track_ids[j] for j in ranfe (len(track_ids)) if clusters[j] == i]
        playlist = sp.user_playlists_create(user_id, f"Mood {i+1} Playlist")
        sp.user_playlist_add_tracks(user_id, playlist['id'], mood_tracks)
        playlists.append(playlist['external_urls']['spotify'])

    return playlists