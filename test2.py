import tkinter as tk
from tkinter import messagebox
import cv2
from deepface import DeepFace
import spotipy
import webbrowser

def on_enter(e):
    e.widget['bg'] = 'lightgreen'

def on_leave(e):
    e.widget['bg'] = 'white'


def capture_image():
    global frame, cap
    cap = cv2.VideoCapture(0) 
    ret,frame = cap.read() 
    while(True):
        cv2.imshow('img1',frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
            cv2.imwrite('C:\\Users\\User\\Desktop\\UTM\\Anul 2\\proiect an\\facedetection\\photo.jpg',frame)
            cv2.destroyAllWindows()
            break
    cap.release()
    messagebox.showinfo("Success", "Image captured successfully!")

def analyze_image():
    global verification, result
    result = DeepFace.analyze(frame, actions=['emotion'])
    verification = result['dominant_emotion']
    if verification:
        messagebox.showinfo("Success", "Image analyzed successfully! \n Dominant Emotion: " + verification)
    else:
        messagebox.showerror("Error", "No dominant emotion found.")

def search_music():
    global spotifyObject, user, searchResults, tracks_dict, tracks_items,song
    username = 'User'
    clientID = '3d22b9621eb04a12aeadf2827bc7d40a'
    clientSecret = '350ac38c7603471b9668960e61bf28d8'
    redirectURI = 'https://www.google.com/' 
    oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    searchResults = spotifyObject.search(verification,1,0,"track")
    tracks_dict = searchResults['tracks']
    tracks_items = tracks_dict['items']
    song = tracks_items[0]['external_urls']['spotify']
    webbrowser.open(song)
    messagebox.showinfo("Success", "Music search successful!")

def exit_program():
    root.destroy()

# GUI window
root = tk.Tk()
root.title("Music Emotion Recognition")
root.geometry('160x250')
main_frame = tk.Frame(root, bg='white')
main_frame.place(relwidth=1, relheight=1)
# bg_image = tk.PhotoImage(file='bg1.png')
# bg_label = tk.Label(main_frame, image=bg_image)
# bg_label.grid(row=4, column=1, columnspan=5, rowspan=5)

# Create the buttons
capture_button = tk.Button(main_frame, text="Capture Image", command=capture_image, bg='white',width=15,height=2,font=("Berlin Sans FB Demi", 12))
capture_button.grid(row=4, column=0,padx=5, pady=0,sticky="NSEW")
capture_button.bind("<Enter>", on_enter)
capture_button.bind("<Leave>", on_leave)

analyze_button = tk.Button(main_frame, text="Analyze Image", command=analyze_image, bg='white',width=15,height=2,font=("Berlin Sans FB Demi", 12))
analyze_button.grid(row=5, column=0,padx=5, pady=3,sticky="NSEW")
analyze_button.bind("<Enter>", on_enter)
analyze_button.bind("<Leave>", on_leave)

search_button = tk.Button(main_frame, text="Search Music", command=search_music, bg='white',width=15,height=2,font=("Berlin Sans FB Demi", 12))
search_button.grid(row=6, column=0,padx=5, pady=3,sticky="NSEW")
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

exit_button = tk.Button(main_frame, text="Exit", command=exit_program, bg='white',width=15,height=2,font=("Berlin Sans FB Demi", 12))
exit_button.grid(row=8, column=0, padx=5, pady=3,sticky="NSEW")
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)


root.mainloop()