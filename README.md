# Hay Day Farm Bot

IMPORTANT: This is just a hobby project and is not actively maintained. If you have any issues I cannot help you, I just wanted to share this bot with the public. 

I only tested this bot with a windows machine, i cannot guarantee that this bot runs with linux or mac.

## Setup

This guide will help you set up a virtual environment and install the required dependencies for this project.

### 1. Create a Virtual Environment

Run the following command in the project root directory:

```sh
python -m venv venv
```

### 2. Activate the Virtual Environment

#### Windows (Command Prompt):
```sh
venv\Scripts\activate.bat
```

#### Windows (PowerShell):
```sh
venv\Scripts\Activate.ps1
```

#### macOS/Linux:
```sh
source venv/bin/activate
```

After activation, your terminal prompt should start with `(venv)`.

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```


## How to use

### Requirements
- Hay Day running inside an emulator (I used **Memu Player**) in fullscreen mode (with borders).
- For more than one screen, use the screen where Emulator with Hay Day is visible in the preview of the program.
- Python installed on your system (I used 3.10).

### Running the Bot
1. Open **Hay Day** in your Emulator.
2. Start the bot by clicking the **Start** button in the application.
3. Let the bot run while Hay Day remains open.

### Customizing the Bot
Currently, the bot only harvests **wheat**, but you can modify it to harvest other crops:

1. **Add a new plant image:**
   - Navigate to the `templates` folder.
   - Add an image of the new crop (use the wheat image as a reference).

2. **Update the bot constants:**
   - Open `bot.py`.
   - Locate the constants section and add your new plant image under a variable ending with `_img`.

Example:
```python
plant_img = cv2.imread('templates/plants/new_crop.png', cv2.IMREAD_UNCHANGED)
```

### Notes
- The bot works best in **Memu Player in fullscreen mode with borders enabled**.
- If you use multiple screens, ensure the one with Hay Day is selected within the program.
- The bot continuously runs until stopped manually.
