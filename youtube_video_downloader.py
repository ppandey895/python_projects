# Importing modules --> Tkinter for GUI, pytube for downloading video
from pytube import YouTube
import pytube.request
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

# Change the value here to something smaller to decrease chunk sizes,
#  thus increasing the number of times that the progress callback occurs
pytube.request.default_range_size = 262144 # 1048576/4 --> 1/4 MB per chunk


# Defining Tkinter Window Variable --> dimensions and title
root = Tk()
root.geometry('500x320')
root.maxsize(500, 320)
root.title('YouTube Video Downloader - Heavy Driver')

# Defining functions

def progress_function(chunk, file_handle, bytes_remaining):
	'''
	this function fetches remaining file size to calculate the percentage
	to fill the progress bar
	'''

	progress_bar['value'] = round((1-bytes_remaining/video.filesize)*100, 3)
	root.update_idletasks()

def start_download():
    '''
    this function is responsible for downloading video to the selected directory

    to see calling of this function, see line 88
    '''

    global video
    qlty = clicked.get()
    loc = folder_selected

    for i in allStream:
    	if i.resolution == qlty:
            itag = i.itag
            file_size = i.filesize_approx/(1024*1024)
    video = allStream.get_by_itag(itag)

    video.download(loc)
    root.destroy()

def browse_folder():
    '''
    this function is used to fetch directory (location) to save the downloaded video

    to see calling of this function, see line 84
    '''

    global folder_selected
    folder_selected = filedialog.askdirectory()

def download_page(quality, title):
   	# this function takes possible qualities of the video and its title,
    # erases the homepage then makes a download page

    # to see calling of this function, see line 114
    
    label2.destroy()
    textinp.destroy()
    button1.destroy()

    # creating labels for sub-heading and title of video
    Label(frame, text='Download Your Video Here', font='Arial 13 bold').grid(row=1, column=0, columnspan=2)
    Label(frame, text=f'Title: {title}', font='Arial 10', wraplength=400).grid(row=2, column=0, columnspan=2, pady=(10, 5))
    Label(frame, text='Select Quality', font='Arial 10 bold', foreground='grey').grid(row=3, column=0)

    global clicked
    clicked = StringVar()
    clicked.set('Quality')
	
    # creating drop down menu for selecting qualities 
    drop = OptionMenu(frame, clicked, *quality)
    drop.grid(row=3, column=1)

    # creating a button for browsing directory for the download
    button2 = Button(frame, text='Browse Folder', style='TButton', command=browse_folder)
    button2.grid(row=4, column=0, columnspan=2, pady=10)
    
    # creating a button to start downloading the video
    button3 = Button(frame, text='Start Download!', command=start_download)
    button3.grid(row=5, column=0, columnspan=2)

    # creating a progress bar for downloading
    global progress_bar
    progress_bar = Progressbar(frame, orient='horizontal', length=300, mode='determinate')
    progress_bar.grid(row=6, column=0, columnspan=2, pady=(10,0))

def validate_link():
    '''
    this function validates the given link in the homepage

    to see calling of this function, see line 151
    '''

    # for error handling
    try:
    	global quality, allStream
    	link = textinp.get(1.0, "end-1c")
    	yt = YouTube(link, on_progress_callback=progress_function)
    	allStream = yt.streams.filter(progressive=True)
    	quality = []
    	title = yt.title
    	for i in allStream:
    		quality.append(i.resolution)
    	# print(quality)
    	download_page(quality, title)

    except:

        # displaying error
        Label(frame, text='Please enter a valid URL', foreground='red', font='Arial 10 bold').grid(row=3, column=0, columnspan=2, pady=(30, 0))


# Creating the Home Page

# creating frame for the window
frame = Frame(root, borderwidth=2)
frame.place(relx=0.5, rely=0.5, anchor='center')

# creating label for the main heading --> YouTube Video Downloader
label1 = Label(frame, text='YouTube Video Downloader', font='Corbel 18 bold')
label1.grid(row=0, column=0, columnspan=2, pady=(0, 30))

# creating a label for taking the input value
label2 = Label(frame, text='Video URL Here: ', font='Corbel 12 bold', foreground='grey')
label2.grid(row=1, column=0)

# creating an input box to take a URL from the user
textinp = Text(frame, width=40, height=1)
textinp.grid(row=1, column=1)
 
# This will create style object
style = Style()

# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).
style.configure('TButton', font =('calibri', 13, 'bold'), foreground = 'green', height=10)

# creating a button to proceed to the download page
button1 = Button(frame, text = 'Go To Download',
                  style = 'TButton',
             command = validate_link)
button1.grid(row=2, column=0, columnspan=2, pady=(10, 0))

# the tkinter main loop
root.mainloop()


'''
The basic code for getting youtube video streams for a given link

link = 'https://youtu.be/ZnZqB5Z75zI'
yt = YouTube(link, on_progress_callback=progress_function)
print("Title: ",yt.title)
allStreams = yt.streams.filter(progressive=True)

for i in allStreams:
    print(f'iTag: {i.itag}, resolution: {i.resolution}')
'''

