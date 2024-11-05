DEFAULT_DIR = "./videos/"

def createFile(fileName):
    try:
        master = open(DEFAULT_DIR + fileName, "x")
        return master
    except:
        master = open(DEFAULT_DIR + fileName, "w")
        return master


def writeFile(file, playlists):
    try:
        playlistsString = ""

        for playlist in playlists:
            playlistsString+= f"""
#EXT-X-STREAM-INF:BANDWIDTH={playlist["bandwidth"]}
{playlist["stream"]}
"""
        file.write(
                "#EXTM3U" + playlistsString
        )

        return True

    except:
        return False