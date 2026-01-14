# CodeAssist

CodeAssist is a Python-based AI coding agent that leverages the Gemini 2.5 Flash model to interact with a local file system. It's designed to be a helpful AI coding assistant that can understand and fix Python code.

## Features

*   **AI-Powered Code Understanding:** Utilizes the Gemini 2.5 Flash model to comprehend and interact with your code.
*   **File System Interaction:** Can list files, read file content, write to files, and execute Python files.
*   **Command-Line Interface:** Provides a simple command-line interface for interacting with the agent.
*   **Secure:** Operates within a sandboxed working directory to prevent unintentional or malicious changes to your system.
*   **Extensible:** The agent's capabilities can be extended by adding new functions to the `functions` directory.

## Requirements

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) package manager

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/piratemeow/codeassist.git
    cd codeAssist
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    Create a `.env` file by copying the example file:

    ```bash
    cp .env.example .env
    ```

    Then, open the `.env` file and add your Gemini API key:

    ```
    GEMINI_API_KEY="your-api-key"
    ```
4.  **Assign wroking directory:**
    
    Assign the working directory name in `call_function.py` file.
    ```
    working_directory = "./your-working-directory"
    ```
    This is the working directory for the agent. For security reasons, the agent can not perform the functions or does not have the context outside this directory.
    

## Project Structure

```
codeAssist/
├── calculator/           # Working directory for the agent
│   ├── main.py
│   ├── tests.py
│   └── pkg/
├── functions/            # Predefined functions for the agent
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── .gitignore
├── .env.example          
├── main.py               # Main entry point for the agent
├── call_function.py      # Handles function calls from the model
├── requirements.txt      # Project dependencies
├── pyproject.toml        # Project metadata
└── README.md             # This file
```


## Usage

You can run the agent from the command line by providing a prompt:

```bash
uv run main.py "<your prompt>"
```
### Example

1. **Prompt:** check if there are any errors in the pkg/calculator.py with some test cases,fix the errors, make a report and save the report to report.txt file.
```bash
$ uv run main.py "check if there are any errors in the pkg/calculator.py with some test cases,fix the errors, make a report and save the report to report.txt file."

-> - Getting the contents of ./calculator directory
 - Getting the contents of ./calculator/pkg directory
 - Reading the contents of ./calculator/pkg/calculator.py file
 - Writing to ./calculator/pkg/calculator.py file
 - Writing to ./calculator/test_calculator.py file
 - Executing ./calculator/test_calculator.py file
 - Reading the contents of ./calculator/pkg/calculator.py file
 - Writing to ./calculator/pkg/calculator.py file
 - Executing ./calculator/test_calculator.py file
 - Writing to ./calculator/pkg/calculator.py file
 - Executing ./calculator/test_calculator.py file
 - Writing to ./calculator/report.txt file
The errors in `pkg/calculator.py` have been identified and fixed, and a detailed report has been generated and saved to `report.txt`. All core calculator functionalities are now working correctly, with the acknowledged limitation of direct unary minus support.
```
2. **Prompt:** how does the tic-tack-toe game work. [tic-tac-toe.py is the game program that was built by the agent and it works perfectly.]
```bash
$ uv run main.py "how does the tic-tack-toe game work"

-> - Getting the contents of ./calculator directory
 - Reading the contents of ./calculator/tic_tac_toe.py file
The tic-tac-toe game is implemented in `tic_tac_toe.py`.

Here's a breakdown of how it works:

**Core Game Logic:**

*   **`print_board(board)`:** This function takes the current game board (a 3x3 list of lists) and prints it to the console in a human-readable format.
*   **`check_win(board, player)`:** This function checks if the given `player` has won the game. It checks all rows, columns, and both diagonals for three consecutive marks of the `player`.
*   **`check_draw(board)`:** This function checks if the game is a draw. This occurs when all cells on the board are filled, and no player has won.
*   **`get_player_move(board, player, args)`:** This function handles getting a move from a human player.
    *   If `args` are provided (meaning the game is being run with command-line arguments), it attempts to parse the row and column from the arguments. It includes error handling for invalid move formats or invalid moves (e.g., out of bounds, already occupied).
    *   If no `args` are provided, it enters an interactive loop, prompting the player to enter their move (row and column) until a valid and empty cell is chosen.
*   **`get_computer_move(board, player)`:** This function implements the AI for the computer player. It follows a hierarchical strategy:
    1.  **Check for an immediate win:** If the computer can win in the next move, it takes that move.
    2.  **Block opponent's win:** If the human player can win in the next move, the computer blocks it.
    3.  **Take the center:** If the center cell (1, 1) is available, the computer takes it.
    4.  **Take a corner:** If any corner cells are available, the computer randomly chooses one.
    5.  **Take a side:** If any side cells are available, the computer randomly chooses one.
*   **`play_game(player_moves=None)`:** This is the main function that orchestrates the game.
    *   It initializes an empty 3x3 game `board`.
    *   It randomly determines which player (X or O) goes first.
    *   It enters a `while True` loop that continues until the game ends (win or draw).
    *   Inside the loop:
        *   It prints the current `board`.
        *   It gets a move from either the human player (`get_player_move`) or the computer (`get_computer_move`) based on whose turn it is.
        *   It updates the `board` with the chosen move.
        *   It checks for a win using `check_win`. If there's a winner, it prints the result and returns "win".
        *   It checks for a draw using `check_draw`. If it's a draw, it prints the result and returns "draw".
        *   It switches the `current_player`.

**How to Run:**

*   **Interactive Mode:** If you run the script directly without any command-line arguments (`python3 tic_tac_toe.py`), it will start an interactive game where you can input your moves. After each game, it will ask if you want to play again.
*   **Command-Line Mode:** You can also provide moves as command-line arguments. For example:
    `python3 tic_tac_toe.py 0 0 1 1 0 1`
    In this mode, the script will execute the game non-interactively, using the provided moves for the human player. The `sys.argv[1:]` captures these arguments, which are then passed to `play_game` as `player_moves`.

Let me know if you want to play the game or test any specific scenarios!
```
3. use ```--verbose``` flag for response analytics.
```bash
$ uv run main.py --verbose "can you check if the calculator is working properly"

-> Warning: there are non-text parts in the response: ['function_call'],returning concatenated text result from text parts,check out the non text parts for full response from model.
Prompt: can you check if the calculator is working properly
Prompt tokens: 775
Response: None
Response tokens: 12
Calling function: get_files_info({})
-> {'result': '- pkg: file_size=4096 bytes, is_dir=True\n- montu.py: file_size=28 bytes, is_dir=False\n- ins.txt: file_size=73 bytes, is_dir=False\n- tic_tac_toe.py: file_size=5430 bytes, is_dir=False\n- tests.py: file_size=1353 bytes, is_dir=False\n- __pycache__: file_size=4096 bytes, is_dir=True\n- main.py: file_size=740 bytes, is_dir=False\n'}
Warning: there are non-text parts in the response: ['function_call'],returning concatenated text result from text parts,check out the non text parts for full response from model.
Prompt: can you check if the calculator is working properly
Prompt tokens: 954
Response: None
Response tokens: 21
Calling function: run_python_file({'file_path': 'tests.py'})
-> {'result': "\n                STDOUT: b'',\n                STDERR: b'.........\\n----------------------------------------------------------------------\\nRan 9 tests in 0.000s\\n\\nOK\\n'\n"}
Prompt: can you check if the calculator is working properly
Prompt tokens: 1039
Response: The tests seem to be passing, so the calculator should be working properly.
Response tokens: 15
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.


