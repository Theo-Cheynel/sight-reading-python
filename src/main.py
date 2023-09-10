import abjad
import mido
import random
import threading

# Constants for MIDI note numbers
MIDDLE_C = 60

# Function to update the note display
def update_note_display(note):
    staff = abjad.Staff(r"\relative c' { " + abjad.NamedPitch(note).lilypond() + "4 }")
    score = abjad.Score([staff])
    lilypond_file = abjad.LilyPondFile.new(
        score,
        includes=["abjad.ily"],
        default_paper_size=("letter", "portrait"),
    )
    lilypond_file_path = "sheet_music.ly"
    abjad.persist(lilypond_file).as_ly(lilypond_file_path)
    abjad.Command().execute(["lilypond", lilypond_file_path])
    abjad.system.IOManager.open_pdf(lilypond_file_path)

# Function to handle incoming MIDI messages
def handle_midi_message(message):
    if message.type == "note_on":
        note = message.note
        update_note_display(note)
        if note == random_note:
            print("Congratulations! You played the correct note.")
            threading.Thread(target=generate_random_note).start()

# Function to generate a random note
def generate_random_note():
    global random_note
    random_note = random.randint(MIDDLE_C - 12, MIDDLE_C + 12)  # Random note within an octave
    print(f"Play the note: {abjad.NamedPitch(random_note)}")

# Initialize the random note
random_note = None
generate_random_note()

# Create a MIDI input thread
def midi_input_thread():
    try:
        with mido.open_input() as port:
            print(f"Using MIDI input: {port.name}")
            print("Listening for MIDI input...")

            for message in port:
                handle_midi_message(message)

    except KeyboardInterrupt:
        print("\nMIDI input monitoring terminated.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Start the MIDI input thread
midi_thread = threading.Thread(target=midi_input_thread)
midi_thread.daemon = True
midi_thread.start()

# Start the Tkinter main loop (for displaying sheet music)
abjad.system.IOManager.main()

# Wait for the MIDI thread to finish (Ctrl+C to terminate)
midi_thread.join()
