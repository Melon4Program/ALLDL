<div align="center">

<pre>
                   ▄▄▄       ██▓     ██▓    ▓█████▄  ██▓                       
                  ▒████▄    ▓██▒    ▓██▒    ▒██▀ ██▌▓██▒                       
                  ▒██  ▀█▄  ▒██░    ▒██░    ░██   █▌▒██░                       
                  ░██▄▄▄▄██ ▒██░    ▒██░    ░▓█▄   ▌▒██░                       
                   ▓█   ▓██▒░██████▒░██████▒░▒████▓ ░██████▒                   
                   ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░ ▒▒▓  ▒ ░ ▒░▓  ░                   
                    ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░ ░ ▒  ▒ ░ ░ ▒  ░                   
                    ░   ▒     ░ ░     ░ ░    ░ ░  ░   ░ ░                      
                        ░  ░    ░  ░    ░  ░   ░        ░  ░                   
                                             ░                                 
▓██   ██▓ ▒█████   █    ██ ▄▄▄█████▓ █    ██  ▄▄▄▄   ▓█████    ▓█████▄  ██▓    
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒▓  ██▒ ▓▒ ██  ▓██▒▓█████▄ ▓█   ▀    ▒██▀ ██▌▓██▒    
  ▒██ ██░▒██░  ██▒▓██  ▒██░▒ ▓██░ ▒░▓██  ▒██░▒██▒ ▄██▒███      ░██   █▌▒██░    
  ░ ▐██▓░▒██   ██░▓▓█  ░██░░ ▓██▓ ░ ▓▓█  ░██░▒██░█▀  ▒▓█  ▄    ░▓█▄   ▌▒██░    
  ░ ██▒▓░░ ████▓▒░▒▒█████▓   ▒██▒ ░ ▒▒█████▓ ░▓█  ▀█▓░▒████▒   ░▒████▓ ░██████▒
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░▒▓███▀▒░░ ▒░ ░    ▒▒▓  ▒ ░ ▒░▓  ░
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░     ░    ░░▒░ ░ ░ ▒░▒   ░  ░ ░  ░    ░ ▒  ▒ ░ ░ ▒  ░
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░   ░       ░░░ ░ ░  ░    ░    ░       ░ ░  ░   ░ ░   
 ░ ░         ░ ░     ░                 ░      ░         ░  ░      ░        ░  ░
 ░ ░                                               ░            ░              
</pre>

**The Ultimate YouTube Downloader CLI**

</div>

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

`allyt-dlp` is a powerful, feature-rich, and user-friendly command-line tool designed to make downloading YouTube videos, subtitles, and thumbnails an absolute breeze. Built on the robust foundation of `yt-dlp`, it enhances the experience with a vibrant, color-coded interface, interactive format selection, and a focus on simplicity and power.

---

### 🌟 Core Features

-   **🎨 Vibrant, Color-Coded Logging**: Never get lost in a wall of text again. `allyt-dlp` provides beautiful, color-coded feedback for every step of the process. Success messages are green `[+]`, warnings are yellow `[*]`, and errors are red `[-]`, all timestamped for clarity.



-   **🎬 Interactive Video Downloader**: Not sure which quality to get? Simply run the tool with the `--video` flag, and it will present you with a clean, numbered list of all available formats—complete with resolution, file size, and codec info. Select one or **multiple** formats to download them all at once!



-   **🎯 Precision Quality Control**: If you already know what you want, use the `--list-formats` command to see all available format codes. Then, use the `--format` flag to download that specific version, bypassing the interactive menu entirely.



-   **📝 Advanced Subtitle Support**: Download subtitles for any video, including auto-generated captions. You can specify multiple languages (e.g., `en,ko,es`) and choose your preferred format (`.srt` or `.vtt`).



-   **🖼️ High-Quality Thumbnails**: Instantly grab the highest-resolution thumbnail for any video with the `--thumbnail` flag.



-   **📂 Smart File & Folder Management**: Keep your downloads organized. Use `--save-dir` to specify a base directory and `--save-folder` to create a dedicated folder for each download session.



-   **⚙️ Flexible Command Structure**: Don't worry about the order of your arguments. The URL can be placed anywhere in the command thanks to the `-u`/`--url` flag.



---



### 🚀 Installation



Getting started with `allyt-dlp` is simple.



1.  **Clone the Repository**:

    ```bash

    git clone https://github.com/your-username/allyt-dlp.git

    cd allyt-dlp

    ```



2.  **Install Dependencies**:

    The tool relies on a few powerful Python libraries. Install them easily using the `requirements.txt` file.

    ```bash

    pip install -r requirements.txt

    ```



---



### 📖 Usage & Recipes



The core of `allyt-dlp` is its flexibility. Here’s how to master it.



#### Basic Command Structure



```bash

python allyt.py -u "YOUTUBE_URL" [OPTIONS]

```



#### **Cookbook: Common Examples**



Here are some practical "recipes" to get you started.



**Recipe 1: The Interactive Download**

*The easiest way to grab a video.* You'll be prompted to choose the quality.



```bash

python allyt.py --video -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

```

*After running, you'll see a list. Enter numbers like `1` or `1,3,5` to download your chosen formats.*



---



**Recipe 2: The Precision Sniper**

*You know exactly what you want.* First, list the formats, then download by code.



1.  **Scout for formats:**

    ```bash

    python allyt.py --list-formats -u "https://www.youtube.com/watch?v=LXb3EKWsInQ"

    ```



2.  **Execute the download (e.g., format `18` for 360p mp4):**

    ```bash

    python allyt.py --video --format 18 -u "https://www.youtube.com/watch?v=LXb3EKWsInQ"

    ```



---



**Recipe 3: The Polyglot**

*Download a video and multiple language subtitles in a specific format.*



```bash

python allyt.py -u "URL" --video --subtitle --save-sub-lang "en,es,ko" --sub-style vtt --save-folder "Multi-Lang Video"

```



---



**Recipe 4: The Archivist**

*Download everything: the best video, the thumbnail, and English subtitles into a neat folder.*



```bash

python allyt.py -u "URL" --video --thumbnail --subtitle --save-folder "My Full Archive"

```

*(This will trigger interactive mode for video selection.)*



---



### 🧰 Full Command Reference



| Argument              | Short | Description                                                                 |
| --------------------- | ----- | --------------------------------------------------------------------------- |
| `--url`               | `-u`  | **(Required)** The URL of the YouTube video or playlist.                    |
| `--video`             |       | Download the video. Triggers interactive mode if `--format` is not used.    |
| `--subtitle`          |       | Download subtitles.                                                         |
| `--thumbnail`         |       | Download the thumbnail.                                                     |
| `--list-formats`      |       | Display all available video/audio formats and their codes.                  |
| `--list-subs`         |       | Display all available subtitle languages.                                   |
| `--format`            |       | Specify a format code to download, skipping the interactive menu.           |
| `--save-dir`          |       | The base directory where files will be saved. Defaults to the current dir.  |
| `--save-folder`       |       | The name of a sub-folder to save the files in.                              |
| `--save-sub-lang`     |       | Comma-separated list of subtitle languages to download (e.g., `en,ko`).     |
| `--sub-style`         |       | The format for the subtitles (`srt` or `vtt`).                              |
| `--help`              | `-h`  | Show the help message and exit.                                             |



---



### 📜 License



This project is proudly distributed under the **MIT License**. See the `LICENSE` file for more details.



### 📧 Contact & Support



For questions, feedback, or assistance, please feel free to reach out via email:

**[kbs.programmer@gmail.com](mailto:kbs.programmer@gmail.com)**
