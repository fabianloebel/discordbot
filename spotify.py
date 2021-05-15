import spotipy
import re
import os
from dotenv import load_dotenv


class Spotify:

    def __init__(self):
        load_dotenv()
        _CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        _CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

        if _CLIENT_ID is None or _CLIENT_SECRET is None:
            print('Spotify: Client credentials need to be provided in .env!')
            return None

        credentials = spotipy.SpotifyClientCredentials(client_id=_CLIENT_ID, client_secret=_CLIENT_SECRET)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)

    async def get_playlist(self, ctx, playlist_id):
        """Get list of tracks in a playlist"""
        try:
            playlist = self.sp.playlist(playlist_id=playlist_id, market='DE')
        except spotipy.SpotifyException:
            await ctx.send(f'Couldn\'t access playlist!')
            return None

        return [(item['track']['artists'][0]['name'], item['track']['name']) for item in playlist['tracks']['items']]

    async def get_album(self, ctx, album_id):
        """Get list of tracks in an album"""
        try:
            album = self.sp.album(album_id=album_id)
        except spotipy.SpotifyException:
            await ctx.send(f'Couldn\'t access album!')
            return None

        return [(item['artists'][0]['name'], item['name']) for item in album['tracks']['items']]

    async def get_tracks(self, ctx, search):
        """Get list of tracks in a playlist or album"""
        if 'playlist' in search:
            try:
                playlist_id = re.search('playlist/(.+?)\?', search).group(1)
            except AttributeError:
                await ctx.send(f'Couldn\'t find a playlist id in the link!')
                return None

            playlist = await self.get_playlist(ctx, playlist_id)
            return playlist

        elif 'album' in search:
            try:
                album_id = re.search('album/(.+?)\?', search).group(1)

            except AttributeError:
                await ctx.send(f'Couldn\'t find an album id in the link!')
                return None

            album = await self.get_album(ctx, album_id)
            return album

        else:
            await ctx.send(f'Only playlist and album links are supported!')
            return None

