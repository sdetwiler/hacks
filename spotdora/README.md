Spotdora
===

Create Spotify playlists with tracks liked from Pandora stations.

Setup
---

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Usage
---

Performed with Chrome:

* Open a browser and browse to <a href="http://www.pandora.com/profile/likes/">http://www.pandora.com/profile/likes/</a>.
* Open the browser's developer tools and show the "Network" tab.
* Click on "show more" on the likes page.
* Select the `tracklikes?likeStartIndex=0&thumb...` entry in the Network developer tool.
* Select the "Headers" tab on the right.
* Copy the Cookie header and the Referer header.
* Edit the `getPandoraLikesHtml` function in `spotdora.py` with the copied values.
* Uncomment the call to `pullPandoraLikes` in the `main` function
* Run the script
* If you're lucky that will all work, but probably some digging and changes will be needed. Good luck.