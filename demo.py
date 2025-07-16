from lib.GI6E import *
 
if __name__ == '__main__':
    # Get input text from the user
    text = input("Enter text: ")
    # Create an instance of the grid class
    grid_ = grid()
    # Convert the text to grid code, returning the code and file path (if any)
    data, path = grid_.text_2_grid(text)
    # Decode the grid code back to text and print the result
    print("grid_2_text=>", grid_.grid_2_text(data))
    # Convert text to grid code and generate a wav audio file, returning code and audio path
    data, path = grid_.text_2_grid(text, wav=True)
    # Decode text from the generated wav audio file and print the result
    print("wav_2_text=>", grid_.wav_2_text(path))
    # Get and print the list of available loopback audio devices
    print("get_audio_list=>", grid_.get_audio_list())
    # Start real-time grid audio detection and print the output
    print(grid_.realtime_grid_detection())
 