import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import random

class Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("9 Puzzle Image Creator")
        self.root.geometry("800x600")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Original image attributes
        self.original_image = None
        self.image_path = None
        self.puzzle_pieces = [[None]*3 for _ in range(3)]
        self.puzzle_piece_labels = []

        # Screens
        self.upload_frame = tk.Frame(self.root)
        self.puzzle_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)

        # Setup UI
        self.create_upload_screen()

    def clear_frames(self):
        for frame in [self.upload_frame, self.puzzle_frame, self.game_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.pack_forget()


    def create_upload_screen(self):
        self.clear_frames()

        # Show upload frame
        self.upload_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            self.upload_frame,
            text="9 Puzzle Image Creator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        # Upload Button
        self.upload_button = tk.Button(
            self.upload_frame,
            text="Upload Image",
            command=self.upload_image,
            font=("Arial", 12)
        )
        self.upload_button.pack(pady=10)

        # Image Display
        self.image_label = tk.Label(self.upload_frame)
        self.image_label.pack(pady=10)

        # Create Puzzle Button
        self.create_puzzle_button = tk.Button(
            self.upload_frame,
            text="Create Puzzle",
            command=self.create_puzzle_pieces,
            state=tk.DISABLED,
            font=("Arial", 12)
        )
        self.create_puzzle_button.pack(pady=10)

    def upload_image(self):
        # Open file dialog to select image
        self.image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )

        if self.image_path:
            try:
                # Open and resize image
                self.original_image = Image.open(self.image_path)
                display_image = self.original_image.copy()
                display_image.thumbnail((400, 400))  # Resize for display

                # Convert to Tkinter-compatible image
                photo = ImageTk.PhotoImage(display_image)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference

                # Enable Create Puzzle button
                self.create_puzzle_button.config(state=tk.NORMAL)

            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {e}")

    def create_puzzle_pieces(self):
        self.clear_frames()
        if not self.original_image:
            messagebox.showwarning("Warning", "Please upload an image first")
            return

        # Clear upload frame
        self.upload_frame.pack_forget()
        self.puzzle_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Resize image to a square
        width, height = self.original_image.size
        size = min(width, height)
        self.original_image = self.original_image.resize((size, size))

        # Create output directory
        output_dir = "puzzle_pieces"
        os.makedirs(output_dir, exist_ok=True)

        # Calculate piece dimensions
        piece_size = size // 3

        # Clear previous puzzle pieces from frame
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()

        # Reset puzzle pieces list
        self.puzzle_pieces = [[None] * 3 for _ in range(3)]  # Ensure a proper matrix
        self.puzzle_piece_labels = []

        # Title
        title_label = tk.Label(
            self.puzzle_frame,
            text="Puzzle Pieces",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Pieces container
        pieces_container = tk.Frame(self.puzzle_frame)
        pieces_container.pack(pady=10)

        # Split and save puzzle pieces
        for row in range(3):
            for col in range(3):
                # Calculate coordinates
                left = col * piece_size
                top = row * piece_size
                right = left + piece_size
                bottom = top + piece_size

                # Crop piece
                piece = self.original_image.crop((left, top, right, bottom))

                # Create thumbnail for display
                piece_thumb = piece.copy()
                piece_thumb.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(piece_thumb)

                # Store piece image in the 2D list
                self.puzzle_pieces[row][col] = piece

                # Display piece
                piece_label = tk.Label(pieces_container, image=photo)
                piece_label.image = photo
                piece_label.grid(row=row, column=col, padx=5, pady=5)
                self.puzzle_piece_labels.append(piece_label)

        # Buttons for next steps
        button_frame = tk.Frame(self.puzzle_frame)
        button_frame.pack(pady=20)

        play_button = tk.Button(
            button_frame,
            text="Play Puzzle",
            command=self.show_game_screen,
            font=("Arial", 12)
        )
        play_button.pack(side=tk.LEFT, padx=10)

        solve_button = tk.Button(
            button_frame,
            text="Solve Puzzle",
            command=self.solve_puzzle,
            font=("Arial", 12)
        )
        solve_button.pack(side=tk.LEFT, padx=10)

        # Add back button
        back_button = tk.Button(
            self.puzzle_frame,
            text="Back to Upload",
            command=self.create_upload_screen,
            font=("Arial", 10)
        )
        back_button.pack(pady=10)



    def show_game_screen(self):
        self.puzzle_frame.pack_forget()
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Randomize puzzle pieces
        randomized_pieces = self.puzzle_pieces.copy()
        random.shuffle(randomized_pieces)

        # Title
        title_label = tk.Label(
            self.game_frame,
            text="Puzzle Game",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Pieces container
        game_container = tk.Frame(self.game_frame)
        game_container.pack(pady=10)

        # Display randomized pieces
        for i in range(3):
            for j in range(3):
                piece = randomized_pieces[i][j]
                photo = None

                # Create thumbnail for display
                if piece is not None:
                    piece_thumb = piece.copy()
                    piece_thumb.thumbnail((100, 100))
                    photo = ImageTk.PhotoImage(piece_thumb)

                # Create a image button, set the bottom right piece as disabled with a dark tint
                if i == 2 and j == 2:
                    piece_button = tk.Button(game_container, image=photo, state=tk.DISABLED, bg="gray")
                else:
                    piece_button = tk.Button(game_container, image=photo, command=lambda i=i, j=j: self.move_piece(i, j))

                piece_button.image = photo
                piece_button.grid(row=i, column=j, padx=5, pady=5)


        # Back and Reset buttons
        button_frame = tk.Frame(self.game_frame)
        button_frame.pack(pady=20)

        back_button = tk.Button(
            button_frame,
            text="Back to Pieces",
            command=self.create_puzzle_pieces,
            font=("Arial", 10)
        )
        back_button.pack(side=tk.LEFT, padx=10)


    def solve_puzzle(self):
        # Similar to game screen, but show pieces in correct order
        # Clear previous frames
        self.puzzle_frame.pack_forget()
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            self.game_frame,
            text="Solved Puzzle",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Pieces container
        solve_container = tk.Frame(self.game_frame)
        solve_container.pack(pady=10)

        # Display pieces in correct order
        for i in range(3):
            for j in range(3):
                piece = self.puzzle_pieces[i * 3 + j]
                photo = ImageTk.PhotoImage(piece)

                piece_label = tk.Label(solve_container, image=photo)
                piece_label.image = photo
                piece_label.grid(row=i, column=j, padx=5, pady=5)

        # Back button
        back_button = tk.Button(
            self.game_frame,
            text="Back to Pieces",
            command=self.create_puzzle_pieces,
            font=("Arial", 10)
        )
        back_button.pack(pady=10)