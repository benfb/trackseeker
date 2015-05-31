import sys
import argparse
import shutil
import getpass
import os.path
import pydub as pd
import dars as d
#
# def saveFiles(fileName1, fileName2, songs):
#     """Save songs to files"""
#     songs[0].export(fileName1, format=fileName1.split(".")[1], tags={"album": args.album, "artist": args.artist})
#     songs[1].export(fileName2, format=fileName2.split(".")[1], tags={"album": args.album, "artist": args.artist})
#
def addToiTunes(itunesPath, fileName):
    """Attempts to add fileName to iTunes by moving it into the default Automatically Add to iTunes.localized folder"""
    try:
        shutil.move(fileName, "{}/Automatically Add to iTunes.localized".format(itunesPath))
    except IOError:
        print("Failed to add song to iTunes: The input file or destination folder doesn't exist!")

def getInput(inputString):
    if py3:
        res = input(inputString + "\n")
    else:
        res = raw_input(inputString + "\n")
    return res

def genPath(artist, album, track, trackNum, fmt, itunesPath):
    return "{}/{}/{}/{} {}.{}".format(itunesPath + "/Music", artist, album, trackNum, track, fmt)

def parseArgs():
    """Parses arguments passed in via the command line"""
    parser = argparse.ArgumentParser()
    # parser.add_argument("name", help="the file you want to split")
    # parser.add_argument("out1", help="the name of the first file you want to output")
    # parser.add_argument("out2", help="the name of the second file you want to output")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    # parser.add_argument("-i", "--itunes", help="attempt to add the split songs to iTunes", action="store_true")
    parser.add_argument("--artist", help="specifies artist for tagging of output files")
    parser.add_argument("--album", help="specifies album for tagging of output files")
    parser.add_argument("--track", help="specifies track title for tagging of output files")
    parser.add_argument("--num", help="specifies track number for tagging of output files")
    parser.add_argument("--itunes", help="tells the program where your iTunes folder is located (default: '/Users/{}/Music/iTunes/iTunes Media/')".format(getpass.getuser()))
    parser.add_argument("--fmt", help="specifies track format for tagging of output files")
    return parser.parse_args()

def main():
    """Actually runs the program"""
    artist = args.artist or getInput("Who wrote the song?")
    album = args.album or getInput("What album is the song on?")
    track = args.track or getInput("What is the track name?")
    trackNum = args.num or getInput("What number is the song on the album?")
    fmt = args.fmt or getInput("What format is the song in?")
    itunes = args.itunes or getInput("Where is your iTunes library located? (default: '/Users/{}/Music/iTunes/iTunes Media/')".format(getpass.getuser()))

    if itunes.strip() == "":
        itunes = "/Users/{}/Music/iTunes/iTunes Media".format(getpass.getuser())

    trackNum = trackNum.zfill(2)

    print(itunes)

    print(artist)
    print(album)
    print(track)
    print(trackNum)
    print(genPath(artist, album, track, trackNum, fmt, itunes))
    path = genPath(artist, album, track, trackNum, fmt, itunes)
    out = d.trackSeek(path, artist, album, track, trackNum, fmt)
    for song in out:
        addToiTunes(itunes, song)

    # songIn = d.instantiateSong(args.name, detectFormat(args.name))
    # times = findGap(songIn)
    # saveFiles(args.out1, args.out2, splitSong(songIn, times[0], times[1]))
    # if(args.itunes):
    #     if(args.verbose):
    #         print("Adding " + args.out1 + " to iTunes...")
    #     addToiTunes(args.out1)
    #     if(args.verbose):
    #         print("Adding " + args.out2 + " to iTunes...")
    #     addToiTunes(args.out2)
    # if(args.verbose):
    #     print "All done!"

py3 = sys.version_info[0] > 2
args = parseArgs()
