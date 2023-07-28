# dataVid
Convert any file into a video and back to files!


# Usage:
### Prerequisites:
* Python 3.10
### Instructions:
Execute each step in order:
* After installing [python](https://www.python.org/downloads/), clone the repository in your local system by opening powershell or cmd in any folder and typing:
```git clone https://github.com/HassanAbbas7/dataVid.git```
* After cloning, run ```pip install -r requirements.txt``` in the downloaded folder.
* Now, copy the file you want to convert into the downloaded folder...
* Run this command ```python vidizer.py vidize --file example.pdf``` for full RGB compression. Use ``--makeinblocks true``` along with the first command to make black and white compression suitable for compressed videos.
* To retrieve data from a video, copy the video into the Images/ folder without renaming it and run ```python vidizer.py filify``` , use ```--isblockencoding true``` if the video is black and white.

Please star the repo if you liked my work!
