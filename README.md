# CopyReader

CopyReader is a Python application that enhances your text reading experience by integrating with the clipboard, utilizing the Flet GUI module, pyttsx3 for text-to-speech functionality, and librosa for audio processing. The app intelligently splits the text into parts, providing a visual indication of the currently spoken segment, making it easier for users to follow along while listening.

![image](https://github.com/phanstudio/X-reader/assets/85735876/eb259040-c9d1-49f7-b78c-29b6a5787319)

![image](https://github.com/phanstudio/X-reader/assets/85735876/ffa136df-0219-4a2d-aab2-c6f8a0b23ab1)

![image](https://github.com/phanstudio/X-reader/assets/85735876/a8116563-9ed9-4d7b-9af1-334d327286ec)


**it is a working application but test are been ran to improve it.**
to download an try ().

## Features

### 1. Clipboard Integration

CopyReader seamlessly integrates with your device's clipboard, allowing you to effortlessly capture text from various sources.

### 2. Text-to-Speech (TTS) with pyttsx3

Enjoy hands-free text consumption by converting copied text into speech. CopyReader utilizes the pyttsx3 library for robust and natural-sounding text-to-speech functionality.

### 3. Flet GUI Module

The application employs the Flet GUI module to create an intuitive and user-friendly interface. Flet enhances the overall user experience with its clean design and interactive elements.

### 4. Dynamic Text Splitting

CopyReader intelligently splits the copied text into parts, visually highlighting the segment that is currently being read. This dynamic splitting enhances user comprehension and helps in following along with the spoken content.

### 5. librosa for Audio Processing

The librosa library is used for audio processing, ensuring a smooth and clear reading experience. librosa enhances the quality of the spoken text, providing a pleasant and natural listening experience.

### 6. Customization

Tailor your reading experience with customizable settings. Adjust the reading speed, voice, and other preferences to suit your individual needs. **will be added if needed**

### 7. History and Favorites

Access a history of your copied texts and mark specific snippets as favorites for quick reference. This feature helps you keep track of important information and revisit it effortlessly. **Will be added if Needed**

### 8. Offline Mode

CopyReader works seamlessly offline, allowing you to read text even when you don't have an active internet connection. This is especially useful for users who want to access information on the go.

### 9. Privacy-Focused

Your privacy is a top priority. CopyReader doesn't store or share your copied text, ensuring that your sensitive information remains secure.

## Installation

1. Install the required dependencies:
   ```bash
   pip install flet pyperclip pyttsx3 shutil librosa
   ```

2. Clone the CopyReader repository:
   ```bash
   git clone https://github.com/phanstudio/X-reader.git
   ```

3. Navigate to the CopyReader directory:
   ```bash
   cd X-reader
   ```

4. Run the application:
   ```bash
   flet run
   ```

## Contribution

Contributions to CopyReader are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request on the [GitHub repository](https://github.com/phanstudio/X-reader).

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
