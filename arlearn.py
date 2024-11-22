import pyttsx3
from tkinter import Tk, Label, Entry, Button, Frame
import vtk

# Function to process the topic and display results
def process_topic():
    topic = entry.get().strip().lower()  # Get the topic input from the user
    if topic in topics:
        label_result.config(text=f"Topic Identified: {topics[topic]['name']}")
        play_voice_explanation(topics[topic]['description'])
        display_3d_model(topics[topic]['model_path'])
    else:
        label_result.config(text="Topic Not Identified. Try another topic.")
        clear_3d_viewer()

# Function to play voice explanations
def play_voice_explanation(description):
    engine = pyttsx3.init()
    engine.say(description)
    engine.runAndWait()

# Function to display the 3D model using vtk
def display_3d_model(model_path):
    global vtk_widget  # Make sure we can replace the 3D viewer dynamically
    clear_3d_viewer()  # Clear the existing viewer
    
    # VTK setup
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Read the 3D model file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(model_path)

    # Map the 3D model to a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor for the 3D model
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    ren.AddActor(actor)

    # Render the 3D model
    ren.SetBackground(0.1, 0.2, 0.4)  # Set background color
    renWin.Render()

    # Embed the 3D view into the Tkinter GUI
    vtk_widget = Frame(root)
    vtk_widget.pack(pady=20)
    vtk_widget_id = vtk_widget.winfo_id()
    renWin.SetParentId(vtk_widget_id)
    renWin.Render()
    iren.Initialize()

# Function to clear the 3D viewer
def clear_3d_viewer():
    if vtk_widget:
        vtk_widget.destroy()

# Predefined topics with 3D models and descriptions
topics = {
    "solar system": {
        "name": "Solar System",
        "description": "The solar system consists of the Sun, eight planets, and their moons.",
        "model_path": "models/solar_system.stl",  # Path to your 3D model file
    },
    "photosynthesis": {
        "name": "Photosynthesis",
        "description": "Photosynthesis is the process by which plants convert sunlight into energy.",
        "model_path": "models/photosynthesis.stl",  # Path to your 3D model file
    },
    "human heart": {
        "name": "Human Heart",
        "description": "The human heart is a muscular organ that pumps blood throughout the body.",
        "model_path": "models/human_heart.stl",  # Path to your 3D model file
    },
}

# GUI setup
root = Tk()
root.title("ARLearn - Augmented Reality for Education")
root.geometry("800x600")

# Instruction label
label_instruction = Label(
    root, text="Enter a challenging topic (e.g., Solar System, Photosynthesis):", font=("Arial", 14)
)
label_instruction.pack(pady=20)

# Text input field
entry = Entry(root, font=("Arial", 14), width=50)
entry.pack(pady=10)

# Submit button
submit_button = Button(root, text="Submit", command=process_topic, font=("Arial", 12))
submit_button.pack(pady=10)

# Result label
label_result = Label(root, text="", font=("Arial", 14))
label_result.pack(pady=20)

# Frame for 3D model viewer
vtk_widget = None  # Placeholder for the 3D viewer

# Run the GUI event loop
root.mainloop()
