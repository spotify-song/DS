# MySounds Playlist Builder

**Author**: Agustin Cody Vargas, Anthony Amaro

MySounds Playlist Builder is a playlist and music recommendation system available for use by the general public.  The recommender system was built using the Spotify Python wrapper [Spotipy](https://spotipy.readthedocs.io/en/2.16.1/#) for the [Spotify API](https://developer.spotify.com/documentation/web-api/).  It is a system that can take two or more individual Spotify users and generate playlists given their relative interests.  The idea was precipitated and brought about by a combination of factors, including but not limited to the 2020 COVID-19 global pandemic, remote working, and online dating.

## Table of Contents

- [API](https://github.com/spotify-song/DS/tree/master/api)
  - [Models](https://github.com/spotify-song/DS/tree/master/api/models)
  - [Visualizations](https://github.com/spotify-song/DS/tree/master/api/visualization)
  - [Spotify Client Auth](https://github.com/spotify-song/DS/blob/master/api/spotify_client_auth.py)
  - [Spotify Users](https://github.com/spotify-song/DS/blob/master/api/spotify_users.py)
- [Notebooks](https://github.com/spotify-song/DS/tree/master/notebooks)
- [References](https://github.com/spotify-song/DS/tree/master/references)

## How to replicate this project

### 1. Setup

Install SpotiPy with pip:

```shell
pip3 install spotipy
```


### Data Flow mock up

![](https://github.com/spotify-song/DS/blob/master/references/Data_Flow_illu.png?raw=true)
