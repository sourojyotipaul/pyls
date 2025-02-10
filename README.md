# pyls

A Python implementation of the `ls` command that lists files and directories in a specified format.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

2. Install dependencies (if any):
    ```bash
    pip install -r requirements.txt

## Usage

1. Run the script using Python:

    ```python
    python -m pyls [options] [path]```

- Options
- A: Include hidden files.
- l: Use long listing format.
- r: Reverse order.
- t: Sort by time modified.
- filter=: Filter by file type (file or dir).

## Running Tests

- To run the tests, use:

    ```bash
    pytest test_pyls.py

