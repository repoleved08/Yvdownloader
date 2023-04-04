from django.views.generic import View
from pytube import YouTube
from django.shortcuts import render, redirect

import tkinter as tk
from tkinter import filedialog

class Home(View):
    def get(self, request):
        return render(request, 'core/home.html')

    def post(self, request):
        # for fetching the video
        if request.POST.get('fetch-vid'):
            url = request.POST.get('given_url')
            video = YouTube(url)
            vidTitle, vidThumbnail = video.title, video.thumbnail_url
            qual, stream = [], []
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)
            context = {'vidTitle': vidTitle, 'vidThumbnail': vidThumbnail,
                       'qual': qual, 'stream': stream,
                       'url': url}
            return render(request, 'core/home.html', context)

        # for downloading the video
        elif request.POST.get('download-vid'):
            url = request.POST.get('given_url')
            video = YouTube(url)
            stream = [x for x in video.streams.filter(progressive=True)]
            video_qual = video.streams[int(request.POST.get('download-vid')) - 1]

            # use tkinter file dialog to let user select download directory
            root = tk.Tk()
            root.withdraw()
            download_dir = filedialog.askdirectory()

            # download video to selected directory
            video_qual.download(output_path=download_dir)
            return redirect('home')

        return render(request, 'core/home.html')
