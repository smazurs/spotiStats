import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorama import Fore, Style
import matplotlib.pyplot as plt

def colorize(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def save_spotify_stats_as_image():
    CLIENT_ID = '31219d11cd8e442e82c9d32b4f8ad331'
    CLIENT_SECRET = 'e2080d0cadec476d8c92c29962741b94'
    REDIRECT_URI = 'http://localhost:5173/callback/'
    SCOPE = 'user-library-read user-top-read user-read-recently-played user-read-playback-state'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))

    # Initialize track_name and artists with default values
    track_name = "No track is currently playing"
    artists = "No artist found"
    res = sp.devices()

    # Retrieve the active device
    devices = sp.devices()
    active_device = next((device for device in devices['devices'] if device['is_active']), None)

    # Retrieve Spotify data
    now_playing = sp.current_playback()
    if now_playing and now_playing['is_playing']:
        track_name = now_playing['item']['name']
        artists = ', '.join([artist['name'] for artist in now_playing['item']['artists']])

    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    top_artists_names = [artist['name'] for artist in top_artists['items']]

    top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
    top_tracks_names = [f"{song['name']} - {', '.join([artist['name'] for artist in song['artists']])}" for song in top_tracks['items']]

    top_albums = sp.current_user_top_tracks(limit=5, time_range='medium_term')
    top_albums_names = [f"{album['album']['name']} - {', '.join([artist['name'] for artist in album['artists']])}" for album in top_albums['items']]

    recently_played = sp.current_user_recently_played(limit=5)
    recently_played_names = [f"{track['track']['name']} - {', '.join([artist['name'] for artist in track['track']['artists']])}" for track in recently_played['items']]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.title('Now Playing',color='black', fontsize=20)
    plt.axis('off')
    plt.text(0.1, 0.75, f"{track_name} - {artists}", color='magenta', fontsize=10)
    plt.text(0.1, 0.45, f"Active device: {active_device['type']}", color='magenta', fontsize=10)
    plt.text(0.1, 0.35, f"Device name: {active_device['name']}", color='magenta', fontsize=10)
    plt.text(0.1, 0.25, f"Volume Percent: {active_device['volume_percent']}", color='magenta', fontsize=10)

    plt.subplot(3, 1, 2)
    plt.title('Top 5 Artists',color='black', fontsize= 20)
    plt.axis('off')
    for idx, artist in enumerate(top_artists_names, 1):
        plt.text(0.1, 0.9 - 0.15 * idx, f"{idx}. {artist}", color='GREEN', fontsize=10)

    plt.subplot(3, 1, 3)
    plt.title('  Recently Played Songs', color='black', fontsize= 20)
    plt.axis('off')
    for idx, track in enumerate(recently_played_names, 1):
        plt.text(0.1, 0.9 - 0.15 * idx, f"{idx}. {track}", color='GREEN', fontsize=10)

    plt.tight_layout()
    plt.axis('off')
    plt.savefig('spotify_stats.png')
    plt.show()

# Main entry point
if __name__ == "__main__":
    save_spotify_stats_as_image()