# m3u To YouTube ADB

My music library is just on my phone, I make playlists there, I store songs there.

This makes sharing playlists kinda hard. So this is my stab at translating these m3u playlists into a YouTube playlist.

## Setting up your YouTube API credentials.

Refer to [this reference](https://developers.google.com/youtube/v3/quickstart/python) from Google.
1. Create a project in the [API console](https://console.cloud.google.com/projectselector2/apis/dashboard).
	- Agree to the ToS and click "Create Project." Give it a name.
2. From Library, enable the YouTube Data API v3.A
3. Create your credentials. Navigate to Credentials, and create an API key and OAuth client ID.
	- For the OAuth key, set the application type to "Other".
4. Copy your credentials into config.py.

## Dependencies
- Android Debug Bridge
- Python modules (install with Pip):
	- eyeD3
	- google-api-python-client
	- google-auth-oauthlib
	- google-auth-httplib2
