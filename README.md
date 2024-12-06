
# VRINSITU VIDEO SERVER

The goal of this project is to streamline the process of creating, managing, and delivering 180 or 360-degree video content. It is designed as a web server to enable remote access and administration.


### Here is a simple diagram showing how the final video is generated.

![Server-Work-Flow](https://vrinsitu-aaron-bucket.s3.amazonaws.com/repos/vr-video-server/images/Server-Work-Flow.png)


## Roadmap

- Add single input support

- Add input recognition

- Change playfab for in house backend


## requirements

  - [GPU Drivers](https://ubuntu.com/server/docs/nvidia-drivers-installation)
  - [nvidia-smi](https://ubuntu.com/server/docs/nvidia-drivers-installation)
  - [Python >= 3.8.0](https://www.python.org/downloads/)
  - [Gstreamer-Core Library version >= 1.20.3](https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c)
  - DMD Stitcher (gstreamer plugin)
  - [AWS CLI >=2.15.27](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - [Inotify-tools](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - Playfab account


## Run Locally

Clone the project

```bash
  https://github.com/aaronx3011/vr-video-server.git
```

Go to the project directory

```bash
  cd vr-video-server
```

Create virtual enviroment

```bash
  python3 -m venv .
```

Activate the virtual enviroment (Linux/Ubuntu)

```bash
  source ./bin/activate
```

Activate the virtual enviroment (Windows)

```bash
  ./Scripts/activate
```

Install all the dependencies (Linux/Ubuntu)

```bash
  pip install -r virtualenv.txt
```

Install all the dependencies (Windows)

```bash
  pip install -r virtualenv.txt
```

Run the app
```bash
  python app.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- **AWS:** `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` `AWS_REGION` `DEFAULT_BUCKET_NAME` `DEFAULT_BUCKET_LINK`

- **FOLDERS** `DEFAULT_DOWNLOAD_FOLDER`

- **PLAYFAB:** `TitleId` `DeveloperSecretKey` `ACCOUNT_LINK_ID`


## Author

- [@aaronx3011](https://www.github.com/aaronx3011)


## Contributors

- [@vitto-jf](https://www.github.com/vitto-jf)
