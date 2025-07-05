# poc_script.py

import os
import subprocess
import datetime

def greet_and_loop(name, count):
    """
    Prints a greeting and demonstrates a simple loop.
    """
    print(f"--- Function: greet_and_loop ---")
    print(f"Hello, {name}! Let's do some looping.")
    for i in range(count):
        print(f"Loop iteration: {i + 1}")
    print(f"--- End of greet_and_loop ---\n")

def file_operations(file_name, content_to_write):
    """
    Creates a file, writes content to it, and then reads it back.
    """
    print(f"--- File Operations: {file_name} ---")
    
    # Get current working directory for context
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    file_path = os.path.join(current_dir, file_name)

    try:
        # Create and write to the file
        print(f"Creating and writing to file: {file_path}")
        with open(file_path, 'w') as f:
            f.write(content_to_write)
        print(f"Successfully wrote content to '{file_name}'.")

        # Read from the file
        print(f"Reading content from file: {file_path}")
        with open(file_path, 'r') as f:
            read_content = f.read()
        print(f"Content read from '{file_name}':\n{read_content}")
        print(f"Successfully read content from '{file_name}'.")

    except IOError as e:
        print(f"Error performing file operations on '{file_name}': {e}")
    print(f"--- End of File Operations ---\n")
    return read_content # Return content for logging later

def execute_shell_command(command):
    """
    Executes a shell command and captures its output.
    """
    print(f"--- Shell Command Execution ---")
    print(f"Executing command: '{command}'")
    try:
        # Run the command, capture stdout and stderr
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True, # Decode stdout/stderr as text
            check=True # Raise an exception for non-zero exit codes
        )
        print(f"Command '{command}' executed successfully.")
        print(f"Command Output:\n{result.stdout}")
        if result.stderr:
            print(f"Command Error Output (stderr):\n{result.stderr}")
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}':")
        print(f"Return Code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return "", f"Error: {e.stderr}"
    except FileNotFoundError:
        print(f"Error: Command '{command.split()[0]}' not found.")
        return "", f"Error: Command '{command.split()[0]}' not found."
    print(f"--- End of Shell Command Execution ---\n")


def main():
    """
    Main function to orchestrate the POC script.
    All outputs are printed to console and collected for file output.
    """
    
    # --- Setup for collecting all output ---
    # We'll redirect stdout temporarily to capture everything for the output file
    # while still printing to the console.
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    redirected_output = StringIO()
    sys.stdout = redirected_output

    print(f"--- POC Script Start: {datetime.datetime.now()} ---")
    print("This script demonstrates basic Python functionalities for a Jenkins POC.")
    print("All output will be displayed in Jenkins logs and saved to 'poc_output.log'.\n")

    # 1. Echo/Print
    print("Hello from the Python script!")
    print("This line is printed directly to stdout.")

    # 2. Looping
    greet_and_loop("Jenkins User", 3)

    # 3. Function Call
    result_from_function = "This is a return value from a function."
    print(f"--- Function Return Value ---")
    print(f"Function returned: '{result_from_function}'")
    print(f"--- End of Function Return Value ---\n")

    # 4. Create and Write to File
    output_file_name = "example_data.txt"
    file_content = f"This is line 1 written by the script.\n" \
                   f"This is line 2 with a timestamp: {datetime.datetime.now()}\n" \
                   f"This is the final line."
    
    read_content = file_operations(output_file_name, file_content)

    # 5. Execute Shell Command
    shell_command_ls = "ls -l"
    shell_output_ls, shell_error_ls = execute_shell_command(shell_command_ls)

    shell_command_pwd = "pwd"
    shell_output_pwd, shell_error_pwd = execute_shell_command(shell_command_pwd)

    # --- Restore stdout and write to file ---
    sys.stdout = old_stdout # Restore original stdout

    final_output_log_file = "poc_output.log"
    full_script_output = redirected_output.getvalue()
    
    print(f"\n--- Writing all captured output to '{final_output_log_file}' ---")
    try:
        with open(final_output_log_file, 'w') as f:
            f.write(full_script_output)
        print(f"All script output successfully written to '{final_output_log_file}'.")
    except IOError as e:
        print(f"Error writing full script output to '{final_output_log_file}': {e}")

    print(f"\n--- POC Script End: {datetime.datetime.now()} ---")
    # Also print the full captured output to console so Jenkins captures it all
    print(full_script_output)


if __name__ == "__main__":
    main()
