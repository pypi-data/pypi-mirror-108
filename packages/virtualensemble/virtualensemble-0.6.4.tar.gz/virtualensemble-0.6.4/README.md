# Introduction

VirtualEnsemble is free and makes it quick and easy to record music individually and merge the recordings to create a mosaic video.

If you find VirtualEnsemble useful and post your performances online, we'd love to see them so please do email a link to <EmailVirtualEnsemble@gmail.com>. 


**Note that this program is quite new and has only been tested on Linux and Windows (though should work on Macs too). Before starting a large project with it, please test that it works well for you.**

# How to install VirtualEnsemble
### Step 1: Install python
Download [python3](https://www.python.org/) and install it, if you don't already have it. If you use Linux you almost certainly already have python.

### Step 2: Install VirtualEnsemble
In Windows, open a "command prompt" and type:
    
        py -m pip install --index-url virtualensemble

In Linux, open a terminal and type:

        python3 -m pip install virtualensemble

### Step 3: Install FFmpeg
Download and install [FFmpeg](https://ffmpeg.org/).

For Windows, there are various guides on the internet on how to install FFmpeg if needed. In short, download [this file](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) (link correct at the time of writing) and unzip it where you like (remembering where you unzipped it).

For Mac, you need to download **FFmpeg** and also **FFprobe** and put them in the same folder. You can download them using these links: [FFmpeg](https://evermeet.cx/ffmpeg/getrelease/zip), [FFprobe](https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip).

If you use Linux you probably already have FFmpeg installed or an easy way or doing so. Note that you need support for mp3 files, which might not be there in your default version of FFmpeg.

### Step 4: Run VirtualEnsemble

In Windows, open a "command prompt" and type:
    
        py -m virtualensemble

In Linux, open a terminal and type:

        virtualensemble

If VirtualEnsemble can't find FFmpeg it will ask you to do so. You need to choose the file called "ffmpeg.exe" (Windows) or "ffmpeg" (Linux), usually in the "bin" folder of where you installed FFmpeg.

# How to create a virtual performance
### Step 1: prepare a backing track
Your singers/players will play along to a backing track whilst recording themselves on a phone. Timing is everything so a strong metronome beat on the backing track is highly recommended.

There are various ways of creating a backing track, for example:

1. Download midi or similar music from the [Choral Public Domain Library](www.cpdl.org) or [IMSLP](www.imslp.org) and add a metronome beat/edit the tempo in your favourite score editor (e.g. [Musescore](www.musescore.org) which is free).
2. Record a piano accompaniment with a load metronome beat.
3. Search the web for others was of doing this.

### Step 2: add the VirtualEnsemble audio signature to you backing track
1. Go to the **Mosaic maker** tab in VirtualEnsemble and to the **Create backing track** tab. 
3. Choose the **audio file** with your backing track and choose and **output file**.
4. Click **Create backing track**.

VirtualEnsemble will create add an audio signature at the start of your backing track which will be used to automatically align the individual recordings.

### Step 3: get the recordings
Send the backing track (with audio signature) to your performers with instructions. **Stress that the most important thing is that your performers are exactly in time with the backing track.**

They need to:

1. Start a video recording of themselves using a phone or similar.
2. Play the backing track from a playback device.
3. At the start, the backing track needs to be played *through speakers*. This way, the audio signature will be captured on the recording. It is important that this is recorded clearly.
4. Once the audio signature has played, plug headphones into the playback device so that the rest of the backing track won't be recorded.
5. Send you the recording (e.g. using [WeTransfer](https://wetransfer.com/)).

### Step 4: add the recordings to VirtualEnsemble

1. Go to the **Add files** tab of VirtualEnsemble. 
2. Click on **Add files and calculate lags...**. 

Your recordings will be added to the table at the bottom of the window. You can also remove files from the table using the **Remove** buttons.

### Step 5: choose the video layout

1. Go to the **Render** tab of VirtualEnsemble. 
2. Choose the **Number of videos** you want in the mosaic.
3. Change in which frame each video is showing. You can do this by dragging them around in the preview pane with the mouse. You can also change the **Position** in the table at the bottom. 
4. Play around with the **Row layout**, **No. rows/cols** and **Border width** to make the mosaic look good. 
5. You will need to zoom in and move the videos. There are two ways to do this:
	1. By clicking and dragging in the preview pane. Instructions are written under the preview pane.
	2. Typing the **Zoom**, **X offset** and **Y offset** into the table.
6. Select an **Output file**.
7. Choose the **Start** and **End** times of the output. Pressing **Grab** will copy the current time from preview slider.
8. Add a **Title** and **Subtitle**. Note the preview does not show these.

### Step 6 - option 1: use automatic audio

VirtualEnsemble can automatically mix the audio, and does so if you don't select an **Audio file (optional)**. The approach used is to ensure that each part has a similar overall volume and then mix them together.

Optionally, you can change the **Volume** of each track in the table. Note that this only affects the relative volume. This can be useful if, for example, you don't have as many people singing/playing a particular part.

### Step 6 - option 2: edit the audio yourself

If you want to do some more serious auto editing:

1. Go back to the **Add files** tab. 
2. Click **Output synchronised audio**. This will output a flac audio file for each input that has been synchronised.
3. These files will be saved in the same place as the original but with **".timelag.flac"** added to the filename.
4. You can import these into an audio editing program (e.g. [Audacity](www.audacityteam.org) which is free) and edit them. **You should avoid repositioning the audio** (e.g. trimming the start).
5. Once you have finished editing, output the audio into an audio file (preferable a lossless format like .wav or .flac).
6. You can choose to use this audio file by selecting it as the **Audio file (optional)** in the **Render** tab.

### Step 7: Render the video

Click **Render** on the **Render** tab. After some time (you can see progress in the **Output** tab), your mosaic should be ready.

### Also...

1. You can **save** or **load** at any time using the **File** menu.
2. You can add audio only files in the same way as adding videos, if needed.
3. In the **Render** tab you can choose **High quality audio**. This is the default and will encode the audio as vorbis. If you use [VLC player](www.videolan.org/vlc) or similar this will work on Windows and Macs, but it doesn't seem to work on the default players. If you unclick, audio will be encoded in aac which is still very high quality.
4. In the **Render** tab there are two more buttons:
	- **Replace audio in video** can be used just to change the audio if you have already produced the video, which is quicker than re-rendering the whole video, and useful to change the balance or similar. The result will be saved in a new file. Note this will not be synchronised if you have changed the start/end times since rendering the video.
	- **Encode audio only** will mix the audio only and output a flac file. This is useful if you want to edit the automatic audio (e.g. add reverb or noise reduction). You can then input this audio by choosing it in **Audio file (optional)**. The audio file will reflect the start/end times for the video, but may have some silence at the start so that it can be used with the **Replace audio in video** button whilst remaining synchronised.
4. The **Copy video/sync audio** tab provides different functionality. If you have recorded a video and at the same time recorded separate audio (e.g. on a high quality microphone) then this will automatically synchronise them. 

### If something went wrong...
#### It’s out of sync

If the performance is out of sync because the performers were not in time, then audio editing is the only option. See **Step 6 - option 2** above.

VirtualEnsemble may have calculated the synchronisation incorrectly. In this case, you can adjust this by editing the **Cut/(add) secs** in the table. The best way of doing this is probably to output the audio (see **Step 6 - option 2**), load the files into an audio editor and try and work out the adjustment that is needed.

#### The balance is wrong

You might be able to fix this with the **Volume** option in the table, but this will adjust the volume by the same amount over the whole video. If you need something more precise, then you will have to edit the audio yourself (see **Step 6 - option 2**).

#### There is no audio

Your audio player may be to blame. Try using [VLC player](www.videolan.org/vlc) or unselecting **High quality audio** as described above.

#### The program didn’t work

Sorry to hear this. Please do get in touch to say what went wrong (<EmailVirtualEnsemble@gmail.com>). Please include the output in the **Output** tab and a copy of the file saved using through the **File** menu. 
