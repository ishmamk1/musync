import json

import requests
from flask import Flask, render_template, redirect, request, jsonify, session, url_for
from flask_cors import CORS,cross_origin
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from app import app

CORS(app)


CLIENT_ID = 'insert'
CLIENT_SECRET = 'insert'
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = "https://api.spotify.com/v1/"
TOKEN_INFO = "token_info"

def create_sp_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for('redirect_page', _external=True),
        scope="user-library-read, user-top-read, user-read-currently-playing, playlist-modify-public, user-read-recently-played")

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    nowTime = int(time.time())

    is_expired = token_info['expires_at'] - nowTime < 60
    if (is_expired):
        sp_oauth = create_sp_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def get_artist_id(artist_name):
    token_info = session.get(TOKEN_INFO)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(q=artist_name, type='artist', limit=1)
    if results['artists']['items']:
        return results['artists']['items'][0]['id']
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    sp_oauth = create_sp_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    access_token = session.get('access_token')
    if access_token:
        revoke_token_url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': f'Bearer {access_token}'}
        requests.post(revoke_token_url, headers=headers)

    # Redirect the user to the Spotify logout page
    return render_template('index.html')


@app.route('/redirect')
def redirect_page():
    sp_oauth = create_sp_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect("home")


@app.route('/home')
def home():
    try:
        token_info = session.get(TOKEN_INFO)
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Extracts top 5 artists
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)  # Adjust time_range as needed

        top_artist_names = [artist['name'] for artist in top_artists['items']]
        top_artist_img = [artist['images'][0]['url'] if artist.get('images') else None for artist in top_artists['items']]
        artist_data = zip(top_artist_names,top_artist_img)
        try:
            user_profile = sp.current_user()
            username = user_profile.get('display_name', 'Guest')
            user_profile_pic = user_profile['images'][0]['url'] if user_profile else None
        except Exception as e:
            # Handle API request errors gracefully
            print(f"Error fetching user profile: {e}")
            username = 'Guest'
            user_profile_pic = None

        current_track = sp.currently_playing()
        if current_track:
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']
            album_name = current_track['item']['album']['name']
            track_url = current_track['item']['external_urls']['spotify']
            track_image = current_track['item']['album']['images'][0]['url']
            track_info = [track_name,artist_name,album_name,track_url, track_image]
        else:
            track_info = None

        top_tracks = sp.current_user_top_tracks(limit=10)
        top_track_data = []
        for track in top_tracks['items']:
            title = track['name']
            images = track['album']['images']
            image_url = images[0]['url'] if images else None
            track_artist = track['artists'][0]['name']
            top_track_data.append((title, image_url,track_artist))

        return render_template('home.html', top_artist_names=top_artist_names, top_artist_img=top_artist_img, username=username, user_profile_pic=user_profile_pic, artist_data=artist_data, track_info=track_info, top_track_data=top_track_data)
    except:
        return render_template("error.html")

@app.route('/recently-played')
def recently_played():
    try:
        token_info = session.get(TOKEN_INFO)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        recent_tracks = sp.current_user_recently_played(limit=50)
        recent_track_info = []
        for item in recent_tracks['items']:
            track = item['track']
            track_info = {
                "title" : track['name'],
                "artist" : track['artists'][0]['name'],
                "album" : track['album']['name'],
                "image" : track['album']['images'][0]['url'],
                "url" : track['external_urls']['spotify'],
                "uri" : track['uri']
             }
            recent_track_info.append(track_info)
        # Render the template with the list of track information
        return render_template('recently_played.html', recent_track_info=recent_track_info, track_info=track_info)
    except Exception as e:
        return render_template("error.html")

@app.route("/playlists",methods=["POST", "GET"])
def playlist_generator():
    try:
        token_info = session.get(TOKEN_INFO)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        if request.method == "POST":
            artist = request.form["artist"]
            genre = request.form["genre"]

            artist_id = get_artist_id(artist)
            modem = False
            recommendations = sp.recommendations(seed_artists=[artist_id], seed_genres=[genre],limit=15)
            return render_template("playlist.html",artist=artist_id, genre=genre, recommendations=recommendations, modem=modem)
        else:
            return render_template("playlist.html")
    except Exception as e:
        return render_template("error.html")

@app.route("/add_playlist", methods=["POST"])
def add_playlist():
    try:
        token_info = session.get(TOKEN_INFO)
        sp = spotipy.Spotify(auth=token_info['access_token'])

        user_info = sp.current_user()
        user_id = user_info['id']
        pl_name = "Musync's Recommended"
        tracks = json.loads(request.form["tracks"])
        user_playlist = sp.user_playlist_create(user=user_id, name=pl_name, public=True)
        track_uri = [track["uri"] for track in tracks]
        sp.playlist_add_items(user_playlist["id"], items=track_uri)
        modem = True
        artist_id = get_artist_id("Drake")
        recommendations = sp.recommendations(seed_artists=[artist_id], seed_genres=["Rap"], limit=15)
        return render_template("playlist.html",recommendations=recommendations,modem=modem)
    except Exception as e:
        print("Error:", e)
        # Log the error
        return render_template("error.html")




if __name__ == '__main__':
    app.run(debug=True)
