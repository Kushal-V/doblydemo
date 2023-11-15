import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

class SongNode:
    def __init__(self, number, title):
        self.number = number
        self.title = title
        self.prev = None
        self.next = None

class MusicPlaylistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist Management")
        self.root.geometry("800x400")

        self.playlist_head = None
        self.current_song_number = 1
        self.currently_playing = None

        self.create_ui()

    def create_ui(self):
        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, width=2500, height=400)
        self.canvas.pack(pady=30)

        # Entry fields for song information
        self.title_label = tk.Label(self.root, text="Title:", font=("Helvetica", 14))
        self.title_label.pack(pady=2)
        self.title_entry = ttk.Entry(self.root, style="Padded.TEntry", font=("Helvetica", 15))
        self.title_entry.pack(pady=15)

        # Entry field for song title to remove
        self.remove_title_label = tk.Label(self.root, text="Song Title to Remove:", font=("Helvetica", 14))
        self.remove_title_label.pack(pady=2)
        self.remove_title_entry = ttk.Entry(self.root, style="Padded.TEntry", font=("Helvetica", 15))
        self.remove_title_entry.pack(pady=15)

        # Buttons for playlist management
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=20)

        # Insert buttons
        insert_end_button = ttk.Button(self.button_frame, text="Add Song to Playlist", command=self.add_song, style="TButton")
        insert_end_button.grid(row=0, column=0, padx=10)

        # Delete buttons
        delete_button = ttk.Button(self.button_frame, text="Remove Song", command=self.remove_song, style="TButton")
        delete_button.grid(row=0, column=1, padx=10)

        # Shuffle button
        shuffle_button = ttk.Button(self.button_frame, text="Shuffle Playlist", command=self.shuffle_playlist, style="TButton")
        shuffle_button.grid(row=0, column=2, padx=10)

        # Play, Next, and Previous buttons
        play_button = ttk.Button(self.button_frame, text="Play", command=self.play_song, style="TButton")
        play_button.grid(row=0, column=3, padx=10)

        next_button = ttk.Button(self.button_frame, text="Next", command=self.next_song, style="TButton")
        next_button.grid(row=0, column=4, padx=10)

        prev_button = ttk.Button(self.button_frame, text="Previous", command=self.prev_song, style="TButton")
        prev_button.grid(row=0, column=5, padx=10)

        # Delete current song and Add next song buttons
        delete_current_button = ttk.Button(self.button_frame, text="Delete Current Song", command=self.delete_current_song, style="TButton")
        delete_current_button.grid(row=0, column=6, padx=10)

        add_next_button = ttk.Button(self.button_frame, text="Add Next Song", command=self.add_next_song, style="TButton")
        add_next_button.grid(row=0, column=7, padx=10)

        # Move current song to next and previous positions
        move_next_button = ttk.Button(self.button_frame, text="Move to Next Position", command=self.move_to_next_position, style="TButton")
        move_next_button.grid(row=0, column=8, padx=10)

        move_prev_button = ttk.Button(self.button_frame, text="Move to Previous Position", command=self.move_to_prev_position, style="TButton")
        move_prev_button.grid(row=0, column=9, padx=10)

    def add_song(self):
        title = self.title_entry.get()

        if title:
            new_song = SongNode(self.current_song_number, title)
            self.current_song_number += 1

            if not self.playlist_head:
                self.playlist_head = new_song
            else:
                current = self.playlist_head
                while current.next:
                    current = current.next
                current.next = new_song
                new_song.prev = current

            self.display_playlist()

    def remove_song(self):
        title_to_remove = self.remove_title_entry.get()
        if not title_to_remove:
            messagebox.showerror("Error", "Enter the title of the song to remove.")
            return

        current = self.playlist_head
        while current:
            if current.title == title_to_remove:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.playlist_head = current.next
                if current.next:
                    current.next.prev = current.prev
                self.display_playlist()
                return
            current = current.next

        messagebox.showerror("Error", f"Song with title '{title_to_remove}' not found in the playlist.")

    def shuffle_playlist(self):
        if self.playlist_head:
            node_values = []
            current = self.playlist_head
            while current:
                node_values.append(current.title)
                current = current.next

            random.shuffle(node_values)

            current = self.playlist_head
            for value in node_values:
                current.title = value
                current = current.next

            self.display_playlist()

    def delete_current_song(self):
        if self.currently_playing:
            current = self.currently_playing
            if current.prev:
                current.prev.next = current.next
            else:
                self.playlist_head = current.next
            if current.next:
                current.next.prev = current.prev
            self.currently_playing = current.next
            self.display_playlist()

    def add_next_song(self):
        if self.currently_playing:
            title = self.title_entry.get()
            if title:
                new_song = SongNode(self.current_song_number, title)
                self.current_song_number += 1

                current = self.currently_playing
                new_song.next = current.next
                new_song.prev = current
                if current.next:
                    current.next.prev = new_song
                current.next = new_song

                self.display_playlist()

    def play_song(self):
        if self.playlist_head:
            self.currently_playing = self.playlist_head
            self.display_playlist()

    def next_song(self):
        if self.currently_playing and self.currently_playing.next:
            self.currently_playing = self.currently_playing.next
            self.display_playlist()

    def prev_song(self):
        if self.currently_playing and self.currently_playing.prev:
            self.currently_playing = self.currently_playing.prev
            self.display_playlist()

    def move_to_next_position(self):
        if self.currently_playing and self.currently_playing.next:
            current = self.currently_playing
            next_node = current.next
            if next_node.next:
                current.next = next_node.next
                next_node.next.prev = current
                next_node.prev = current.prev
                current.prev.next = next_node
                next_node.next = current
                current.prev = next_node
                self.display_playlist()

    def move_to_prev_position(self):
        if self.currently_playing and self.currently_playing.prev:
            current = self.currently_playing
            prev_node = current.prev
            if prev_node.prev:
                current.prev = prev_node.prev
                prev_node.prev.next = current
                prev_node.next = current.next
                current.next.prev = prev_node
                prev_node.prev = current
                current.next = prev_node
                self.display_playlist()

    def display_playlist(self):
        self.canvas.delete("all")
        current = self.playlist_head
        temp_x = 50

        while current:
            fill_color = "yellow" if current == self.currently_playing else "#3498db"
            text_color = "black" if current == self.currently_playing else "white"

            self.canvas.create_rectangle(temp_x, 150, temp_x + 200, 200, fill=fill_color)

            self.canvas.create_text(temp_x + 30, 175, text=f"Prev: {current.prev.number}" if current.prev else "Prev: null", font=("Helvetica", 9), fill=text_color)
            self.canvas.create_text(temp_x + 100, 175, text=f"{current.number}. {current.title}", font=("Helvetica", 12), fill=text_color)
            self.canvas.create_text(temp_x + 170, 175, text=f"Next: {current.next.number}" if current.next else "Next: null", font=("Helvetica", 9), fill=text_color)

            if current.next:
                self.canvas.create_line(temp_x + 200, 175, temp_x + 270, 175, arrow=tk.LAST)

            self.canvas.create_line(temp_x + 58, 150, temp_x + 58, 200, fill="black")  # Line between prev and title
            self.canvas.create_line(temp_x + 140, 150, temp_x + 140, 200, fill="black")  # Line between title and next

            temp_x += 270
            current = current.next
            self.root.update()
            time.sleep(0.2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlaylistApp(root)
    root.mainloop()
