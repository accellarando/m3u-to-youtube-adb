# m3u To YouTube ADB

My music library is just on my phone, I make playlists there, I store songs there.

This makes sharing playlists kinda hard. So this is my stab at translating these m3u playlists into a YouTube playlist.

This is very much a work in progress, but it (generally) works.

## Getting your YouTube API credentials.
I'm using the unofficial ytmusicapi module.
Per [their documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html), it's easiest to just grab the authenticated POST request from your browser.
So, open the developer tools network tab, log in to YouTube Music, and look for a POST 200 response in json.
Copy and paste the *request* headers into "auth.json" in the root directory, as JSON.
If you don't do that, the program should prompt you on first run. It will also jsonify the headers for you if you can't figure it out. (me)

## Dependencies
- Android Debug Bridge
- Python modules (install with Pip):
	- eyeD3
	- ytmusicapi

## Todo
- Auto mode (no selecting from similar search results)
- Batch playlist upload
- Take arguments from the shell
- Further testing and debugging
