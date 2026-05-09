from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import shlex

def get_file_path():
    file = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4",)]
    )
    file_label.config(text=f"file: {file}")
    return file

def convert_video_to_xvid(filepath, output_file):
    subprocess.run(f"ffmpeg -i \"{filepath}\" -c:v libxvid -g 250 -bf 0 -c:a copy \"{output_file}\" -y", shell=True)

def apply_bitstream_noise(input_file, output_file):
    subprocess.run(f"ffmpeg -i \"{input_file}\" -c:v copy -bsf:v noise=amount=key -c:a copy \"{output_file}\" -y", shell=True)

def convert_to_mp4(input_file, output_file):
    subprocess.run(f"ffmpeg -i \"{input_file}\" -c:v libx264 -c:a aac \"{output_file}\" -y", shell=True)

def corrupt():
    filepath = file_label.cget("text").replace("file: ", "")
    if not filepath or filepath == "":
        print("No file selected")
        return
    
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    xvid_file = f"{base_name}_temp_xvid.avi"
    noise_file = f"{base_name}_temp_noise.avi"
    out = f"{base_name}_corrupted.mp4"
    
    if os.path.exists(xvid_file):
        os.remove(xvid_file)
    if os.path.exists(noise_file):
        os.remove(noise_file)
    
    convert_video_to_xvid(filepath, xvid_file)
    finished.config(text="finished xvid conversion")
    if os.path.exists(xvid_file):
        apply_bitstream_noise(xvid_file, noise_file)
        finished.config(text="finished bitstream noise")
        os.remove(xvid_file)
    else:
        finished.config(text="Failed to create xvid file")
        return
        
    if os.path.exists(noise_file):
        convert_to_mp4(noise_file, out)
        finished.config(text=f"saved as {os.path.basename(out)}")
        os.remove(noise_file)
    else:
        finished.config(text="Failed to create bit file")

root = tk.Tk()
root.title("ffmpeg ui")
root.geometry("400x300")
root.resizable(False, False)
root.option_add("*Font", "@SimSun")

label = tk.Label(root, text="ffmpeg ui for corrupting video and datamoshing")
label.pack()

file_button = tk.Button(root, text="open video", command=get_file_path)
file_button.pack(pady=10)

file_label = tk.Label(root, text="")
file_label.pack()

convert_button = tk.Button(root, text="start corruption", command=corrupt)
convert_button.pack(pady=10)

finished = tk.Label(root, text="")
finished.pack()

root.mainloop()