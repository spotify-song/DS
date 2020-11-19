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

### 1. Repository Setup

Git clone this repo (or fork, depending on your desired involvement).

Create a [conda env and kernel](https://youtu.be/6kXLUvsnhuI) or pip env.
You can find documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for more information on managing conda environments and [here](https://docs.python-guide.org/dev/virtualenvs/) for pipenvs

Install SpotiPy and all other dependencies found in the [requirements.txt](https://github.com/spotify-song/DS/blob/master/requirements.txt) file using pip3 (pip3 is for Python 3) or conda in the terminal:

```shell
pip3 install spotipy
```

My recommendation is to build `requirements.txt` file to install all of your dependencies all at once and simply use the following command:

```shell
pip3 install -r requirements.txt
```


### Data Flow

![](https://github.com/spotify-song/DS/blob/master/references/Data_Flow_illu.png?raw=true)
