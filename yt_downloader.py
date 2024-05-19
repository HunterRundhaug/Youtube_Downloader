import tkinter
import customtkinter
from pytube import YouTube


def startDownload():
    try:
        ykLink = link.get()
        ytObject = YouTube(ykLink, on_progress_callback=on_progress)
        videoTitle = ytObject.title
        # Update UI to show download Started
        title.configure(text=videoTitle)
        finishedLabel.configure(text='Downloading...')
        download_button.pack_forget()
        progressBar.pack(padx=10, pady=10)
        pPercentage.pack()
        if dropDown.get() == 'Video':
            video = ytObject.streams.get_highest_resolution()
            video.download()
        else:
            audio_mp4 = ytObject.streams.get_audio_only()
            audio_mp4.download()

        # Reset the finishedLabel text.
        finishedLabel.configure(text='', text_color= 'black')
    except:
        finishedLabel.configure(text="Download Failed...", text_color='red')
        return
    finishedLabel.configure(text="Download Complete!", text_color='green')

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = int(percentage_of_completion)
    # Update UI Progress
    pPercentage.configure(text=str(per) + '%')
    pPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)

def check_valid_link(selection):
    '''
        this function is used to turn on the download button only when
        a valid link is inside the link text box, it is called whenever
        the input changes inside the textbox and whenever the option
        changes selection in the dropdown menu.
        Selection is not used.
    '''
    ytLink = link.get()
    try:
        ytObject = YouTube(ytLink)
        download_button.pack(padx=10, pady=40)
        finishedLabel.configure(text='',)
        progressBar.pack_forget()
        pPercentage.pack_forget()
        title.configure(text='Insert Youtube Link')
    except:
        download_button.pack_forget()
        finishedLabel.configure(text='',)
        progressBar.pack_forget()
        pPercentage.pack_forget()
        title.configure(text='Insert Youtube Link')
        return


# Functions above --------------

#system setup
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

#UI label
title = customtkinter.CTkLabel(app, text='Insert Youtube Link')
title.pack(padx=10, pady=10)

#Link Textbox input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()
link.bind("<KeyRelease>", lambda event: check_valid_link(None))

# Finished Downloading
finishedLabel = customtkinter.CTkLabel(app, text='', font=('Arial', 20))
finishedLabel.pack(pady=10, padx=10)

# Progress UI
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack_forget()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0.0)
progressBar.pack_forget()

# Dropdown Menu
dropDown = customtkinter.CTkOptionMenu(app, values=['Audio only', 'Video'], command=check_valid_link)
dropDown.pack(padx=10, pady=10)
dropDown.set('Video')

#download button
download_button = customtkinter.CTkButton(app, text='Download', command=startDownload)
download_button.pack_forget()

# Run app ---
app.mainloop()
