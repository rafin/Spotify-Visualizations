# Spotify Plotter
- webapp that helps visualize a users public playlists on spotify
- Current version online at: http://plotify.herokuapp.com/

#### Some usage tips in the meantime since the ui doesn't explain much yet
- your username is the string of letters or numbers which can be found as the creator of your personal playlists.
- currently, only public playlists can be accessed.
- if you can, avoid plotting larger playlists (>200) as these exhaust api keys and take a long time to load.
- you can interact with the plot points by clicking on them to hear a song preview.

##### Features ([*source*](https://developer.spotify.com/web-api/get-audio-features/))
- **acousticness**: A confidence measure from 0 to 100 of whether the track is acoustic. 100 represents high confidence the track is acoustic.
- **danceability**: describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0 is least danceable and 100 is most danceable.
- **energy**: Energy is a measure from 0 to 100 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- **instrumentalness**: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 100, the greater likelihood the track contains no vocal content. Values above 50 are intended to represent instrumental tracks, but confidence is higher as the value approaches 100.
- **loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.
- **speechiness**: detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 100 the attribute value. Values above 66 describe tracks that are probably made entirely of spoken words. Values between 33 and 66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 33 most likely represent music and other non-speech-like tracks.
- **tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
- **valence**: A measure from 0 to 100 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
- **popularity**: The value will be between 0 and 100, with 100 being the most popular. The popularity is calculated from the popularity of the song on spotify.
- **duration**: length of the track in seconds.



#### Work in Progress / Possible Future Features
- better error handling and notifications
- ability to login to access private playlists
- visualize an artists entire catalog
- creating playlists from plot selection
- 1D histogram visualization
- individual song bar chart of features
