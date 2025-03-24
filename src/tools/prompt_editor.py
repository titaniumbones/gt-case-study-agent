#!/usr/bin/env python
"""Tool for viewing and editing prompts for the GivingTuesday Campaign Advisor.

This script provides a simple interface for developers to:
1. View existing prompts
2. Compare prompts
3. Edit prompts directly

Usage:
  python -m src.tools.prompt_editor [view|edit|help] [prompt_name]
"""

import importlib
import os
import sys
import inspect
from pathlib import Path

# Add parent directory to path to allow importing from src
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import prompts module
from src import prompts


def get_prompt_names():
    """Get names of all prompt variables in the prompts module."""
    return [name for name, value in inspect.getmembers(prompts) 
            if isinstance(value, str) and name.isupper() and '_PROMPT' in name]


def view_prompt(prompt_name=None):
    """View a specific prompt or list all available prompts."""
    if prompt_name is None:
        # List all available prompts
        print("Available prompts:")
        for name in get_prompt_names():
            print(f"  - {name}")
        return

    # Check if the prompt exists
    if not hasattr(prompts, prompt_name):
        print(f"Error: Prompt '{prompt_name}' not found.")
        print("Available prompts:")
        for name in get_prompt_names():
            print(f"  - {name}")
        return

    # Get the prompt
    prompt_text = getattr(prompts, prompt_name)

    # Print the prompt
    print(f"=== {prompt_name} ===")
    print(prompt_text)


def edit_prompt(prompt_name):
    """Edit a specific prompt using the default editor."""
    if prompt_name is None:
        print("Error: Please specify a prompt name to edit.")
        return

    # Check if the prompt exists
    if not hasattr(prompts, prompt_name):
        print(f"Error: Prompt '{prompt_name}' not found.")
        return

    # Get the current prompt
    current_prompt = getattr(prompts, prompt_name)

    # Create a temporary file
    temp_file = Path(f"/tmp/{prompt_name.lower()}_temp.txt")
    with open(temp_file, "w") as f:
        f.write(current_prompt)

    # Open the editor
    editor = os.environ.get("EDITOR", "nano")
    os.system(f"{editor} {temp_file}")

    # Read the edited prompt
    with open(temp_file, "r") as f:
        edited_prompt = f.read()

    # Check if the prompt was changed
    if edited_prompt == current_prompt:
        print("No changes made.")
        return

    # Update the prompts.py file
    prompts_file = inspect.getfile(prompts)
    with open(prompts_file, "r") as f:
        content = f.read()

    # Escape the prompts for string replacement
    current_prompt_escaped = current_prompt.replace("\\", "\\\\").replace('"', '\\"')
    edited_prompt_escaped = edited_prompt.replace("\\", "\\\\").replace('"', '\\"')

    # Replace the prompt in the file content
    # We need to handle both triple-quoted strings and regular strings
    if '"""' in content:
        current_block = f'{prompt_name} = """{current_prompt}"""'
        new_block = f'{prompt_name} = """{edited_prompt}"""'
        content = content.replace(current_block, new_block)
    else:
        current_block = f'{prompt_name} = "{current_prompt_escaped}"'
        new_block = f'{prompt_name} = "{edited_prompt_escaped}"'
        content = content.replace(current_block, new_block)

    # Write the updated content back to the file
    with open(prompts_file, "w") as f:
        f.write(content)

    print(f"Prompt '{prompt_name}' updated successfully.")

    # Reload the prompts module to reflect changes
    importlib.reload(prompts)


def compare_prompts(prompt1, prompt2):
    """Compare two prompts side by side."""
    if not hasattr(prompts, prompt1) or not hasattr(prompts, prompt2):
        print("Error: One or both prompts not found.")
        return

    # Get the prompts
    prompt1_text = getattr(prompts, prompt1)
    prompt2_text = getattr(prompts, prompt2)

    # Split the prompts into lines
    prompt1_lines = prompt1_text.split("\n")
    prompt2_lines = prompt2_text.split("\n")

    # Get the terminal width
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    # Calculate the width for each prompt
    prompt_width = (terminal_width - 3) // 2

    # Print the header
    print(f"{prompt1:<{prompt_width}} | {prompt2:<{prompt_width}}")
    print("-" * terminal_width)

    # Print the prompts side by side
    for i in range(max(len(prompt1_lines), len(prompt2_lines))):
        line1 = prompt1_lines[i] if i < len(prompt1_lines) else ""
        line2 = prompt2_lines[i] if i < len(prompt2_lines) else ""
        print(f"{line1:<{prompt_width}} | {line2:<{prompt_width}}")


def print_help():
    """Print help information."""
    print("Prompt Editor Tool")
    print("=================")
    print("Usage:")
    print("  python -m src.tools.prompt_editor [command] [args]")
    print("\nCommands:")
    print("  view               List all available prompts")
    print("  view [prompt_name] View a specific prompt")
    print("  edit [prompt_name] Edit a specific prompt")
    print("  compare [prompt1] [prompt2] Compare two prompts side by side")
    print("  help               Show this help information")


def main():
    """Main function to parse arguments and call the appropriate function."""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "view":
        prompt_name = sys.argv[2] if len(sys.argv) > 2 else None
        view_prompt(prompt_name)
    elif command == "edit":
        if len(sys.argv) < 3:
            print("Error: Please specify a prompt name to edit.")
            return
        prompt_name = sys.argv[2]
        edit_prompt(prompt_name)
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Error: Please specify two prompt names to compare.")
            return
        prompt1 = sys.argv[2]
        prompt2 = sys.argv[3]
        compare_prompts(prompt1, prompt2)
    elif command == "help":
        print_help()
    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()