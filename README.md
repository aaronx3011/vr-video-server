
# VRINSITU VIDEO SERVER

The goal of this project is to streamline the process of creating, managing, and delivering 180 or 360-degree video content. It is designed as a web server to enable remote access and administration.


### Here is a simple diagram showing how the final video is generated.

![Server-Work-Flow](https://vrinsitu-aaron-bucket.s3.amazonaws.com/repos/vr-video-server/images/Server-Work-Flow.png)


## Roadmap

- Add single input support

- Add input recognition

- Change playfab for in house backend


## requirements

  - GPU Drivers (we are usign NVIDIA 4090)
  - Python >= 3.8.0
  - Gstreamer (Core Library version >= 1.20.3)
  - DMD Stitcher (gstreamer plugin)
  - AWS CLI (aws-cli >=2.15.27)
  - Inotify
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
  python -m venv .
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
  pip install -r requirements.txt
```

Install all the dependencies (Windows)

```bash
  pip install -r requirementsWindows.txt
```

Run the app
```bash
  python app.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- **AWS:** `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` `AWS_REGION`

- **PLAYFAB:** `TitleId` `DeveloperSecretKey` `ACCOUNT_LINK_ID`


## Author

- [@aaronx3011](https://www.github.com/aaronx3011)


## Contributors

- [@vitto-jf](https://www.github.com/vitto-jf)
