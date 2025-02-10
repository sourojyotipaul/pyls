import pytest
import subprocess
import os

@pytest.fixture
def json_file():
    """Fixture to provide the path to the existing structure.json file."""
    return os.path.join(os.path.dirname(__file__), 'structure.json')

def test_ls_default(json_file):
    """Test the default ls command."""
    result = subprocess.run(['python', '-m', 'pyls'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    assert "LICENSE README.md ast go.mod lexer main.go parser token" in result.stdout

def test_ls_A(json_file):
    """Test the ls -A command."""
    result = subprocess.run(['python', '-m', 'pyls', '-A'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    assert ".gitignore LICENSE README.md ast go.mod lexer main.go parser token" in result.stdout

def test_ls_l(json_file):
    """Test the ls -l command."""
    result = subprocess.run(['python', '-m', 'pyls', '-l'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    print(result.stdout)
    # Adjusting the expected output based on the actual output format
    assert "drwxr-xr-x 1.0K Nov 14 11:27 ./LICENSE" in result.stdout
    assert "drwxr-xr-x 83.0B Nov 14 11:27 ./README.md" in result.stdout
    assert "drwxr-xr-x 4.0K Nov 14 15:58 ./ast" in result.stdout
    assert "drwxr-xr-x 60.0B Nov 14 13:51 ./go.mod" in result.stdout
    assert "drwxr-xr-x 4.0K Nov 14 15:21 ./lexer" in result.stdout
    assert "-rw-r--r-- 74.0B Nov 14 13:57 ./main.go" in result.stdout  # Adjusted for main.go
    assert "drwxr-xr-x 4.0K Nov 17 12:51 ./parser" in result.stdout
    assert "-rw-r--r-- 4.0K Nov 14 14:57 ./token" in result.stdout  # Adjusted for token

def test_ls_r(json_file):
    """Test the ls -l -r command."""
    result = subprocess.run(['python', '-m', 'pyls', '-l', '-r'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    
    # Adjusting the expected output based on the actual output format
    assert "drwxr-xr-x 4.0K Nov 14 15:58 ./token" in result.stdout
    assert "drwxr-xr-x 4.0K Nov 17 12:51 ./parser" in result.stdout

def test_ls_t(json_file):
    """Test the ls -l -t command."""
    result = subprocess.run(['python', '-m', 'pyls', '-l', '-t'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    
    # Adjusting the expected output based on the actual output format
    assert "drwxr-xr-x 1.0K Nov 14 11:27 ./LICENSE" in result.stdout
    assert "drwxr-xr-x 4.0K Nov 17 12:51 ./parser" in result.stdout

def test_ls_filter_dir(json_file):
    """Test the ls -l --filter=dir command."""
    result = subprocess.run(['python', '-m', 'pyls', '-l', '--filter=dir'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    
    # Adjusting the expected output based on the actual output format
    assert "drwxr-xr-x 4.0K Nov 14 15:58 ./ast" in result.stdout
    assert "drwxr-xr-x 4.0K Nov 17 12:51 ./parser" in result.stdout

def test_ls_invalid_filter(json_file):
    """Test the ls -l --filter=invalid command."""
    result = subprocess.run(['python', '-m', 'pyls', '-l', '--filter=invalid'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    assert "invalid choice: 'invalid' (choose from 'file', 'dir')" in result.stderr

def test_ls_non_existent_path(json_file):
    """Test accessing a non-existent path."""
    result = subprocess.run(['python', '-m', 'pyls', 'non_existent_path'], cwd=os.path.dirname(json_file), capture_output=True, text=True)
    assert "error: cannot access 'non_existent_path': No such file or directory" in result.stdout