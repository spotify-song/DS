# **References**

#### The following materials encompass references for the data and analysis in the [Exploratory Notebook](https://github.com/spotify-song/DS/blob/master/notebooks/1.0-av-initial-data-exploration.ipynb)

### **Data**

The data was obtained from the [Spotify API](https://developer.spotify.com) using the Python wrapper [SpotiPy](https://spotipy.readthedocs.io/en/2.13.0/#).  To gain access to the API go to the [Spotify Developers](https://developer.spotify.com) site.

##### **Audio Analysis for a Track**

- The initial exploration was performed on a single track within a user profile. The data being explored comes from the [Audio Analysis Objects](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/#rhythm).  With the `user-top-read`[scope](https://developer.spotify.com/documentation/general/guides/authorization-guide/) I was able to access a user's top tracks, which then provided access to a single track. The [Audio Analysis](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/) function generates the following features amongst others (the following features are part of the initial data exploration and are subject to change moving forward).
    - Bars
    - Beats
    - Sections
    - Segments
    - Tatums
    
##### **Audio Features for a Track**

- Similarly to the audio analysis for a track, [audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) generates a class object containing the following:
     - Duration (ms) (int)
     - Key (int)
     - Mode (int)
     - Time Signature (int)
     - Acousticness (float)
     - Danceability (float)
     - Energy (float)
     - Instrumentalness (float)
     - Liveness (float)
     - Loudness (float)
     - Speechiness (float)
     - Valence (float)
     - Tempo (float)
     - id (string)
     - uri (string)
     - track href (string)
     - analysis url (string)
     - type (string)
    

# Further exploratory details to come.