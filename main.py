# WikiBuilder
import os
import datetime
import random

# Documentation Variables
program_name: str = "WikiBuilder"
version: str = "v2.0.0"
possible_dev_comments: list = [
    "You ain't seen nothing yet.",
    "It started without crashing!",
    "Now in 2D!",
    "IT ReUse, my beloved!"
]
dev_comment: str = random.choice(possible_dev_comments)
divider_character: str = "-"
divider: str = None
dir_split: str = "\\" if os.name == "nt" else "/"

# Global Variables
rootpath: str = "."
file_extension: str = ".md"

# Greet the user when the program starts
def welcome():
    # Edit the following global variables
    global divider

    # Construct the first message and the divider
    first_message: str = f"Welcome to {program_name} {version}.\n\"{dev_comment}\""
    divider = (divider_character * len(first_message))[:len(first_message)]
    
    # Print the message
    print(first_message)
    print(divider)

    # Give context
    print("This is an tool for Wiki.js developed for IT ReUse York by volunteer Skylar Garrett (sky@itreuse.org.uk).")
    print("After you have built a file system full of empty files, fill them all with markdown metadata.")
    print(divider)

    # Help the user
    print("To get started first time, type 'help' to list all possible commands.")
    print(divider)


# Read, write, and execute
def term(preloaded_command=""):
    # Edit the following global variables
    global rootpath
    global file_extension
    
    # User inputted command
    command: str = input("> ") if preloaded_command == "" else preloaded_command
    command = command.split(" ")
    
    match command[0].lower():
        # Change the value of a global variable
        case "set":
            # There is the wrong number of commands for "set"
            if len(command) != 3:
                print(f"Error: 'set' command requires 2 arguments, {len(command)-1} given.")
                
            else:

                # See which arguments we accept
                match command[1].lower():
                    case "rootpath":
                        rootpath = command[2]
                    case "extension":
                        file_extension = command[2]
                    case _:
                        print(f"Error: 'set' command doesn't recognise {command[1]}. Type 'help set' for possible commands.")

                print(divider)
                print("Variables updated.")
                term("info")
            

        # Get the current state of the global variables
        case "info":
            # Non-fatal warning about info taking no arguments
            if len(command) != 1:
                print("WARNING: 'info' command doesn't take any arguments.")

            # Print the current state of the concerned variables
            print(divider)
            print("Current Settings:")
            print(divider)
            print("* ROOTPATH: ", rootpath)
            print("* EXTENSION:", file_extension)
            print(divider)


        # Run the program
        case "run":
            # Flags
            logging_target: str = None
            verbosity_flag: bool = False
            
            # Set a logging target
            if "-o" in command or "--output" in command:
                logging_target = command[
                    max(
                        command.index("-o") if "-o" in command else -1,
                        command.index("--output") if "--output" in command else -1
                    ) + 1
                ]

            # Set the verbose flag on
            if "-v" in command or "--verbose" in command:
                verbosity_flag = True

            print("Running...")
            main(logging_target, verbosity_flag)


        # Help me!
        case "help":
            def setHelp():
                return str(
                    "set [VARIABLE NAME] [VALUE]\n\t" +
                        "Sets an execution variable to a particular value.\n\t" +
                        "VARIABLE NAME can be any of the following:\n\t" +
                        " - `ROOTPATH`:  the topmost path to traverse from.\n\t" +
                        " - `EXTENSION`: the file extension to fill if found empty.\n\t" +
                        "VALUE should be strings."
                )
            
            def infoHelp():
                return str(
                    "info\n\t" +
                        "Shows the current states of execution variables."
                )

            def runHelp():
                return str(
                    "run -{o|v} --{output|verbose}\n\t" +
                        "Run the program with the execution variables (displayed by `info`).\n\t" +
                        "There are flags that can be set with this command:\n\t" +
                        "  -o   --output   [TARGET PATH] : Save the log to a file at TARGET PATH.\n\t" +
                        "  -v   --verbose                : Show all logging levels."
                )

            def helpHelp():
                return str(
                    "help {COMMAND}\n\t" +
                        "Displays this message.\n\t" +
                        "COMMAND specifies which command you need help with."
                )

            def exitHelp():
                return str(
                    "exit\n\t" +
                        "Exits the program safely."
                )

            def allHelp():
                return str(
                    divider + "\n" +
                    "Full help list:\n" +
                    divider + "\n" +
                    setHelp() + "\n\n" +
                    infoHelp() + "\n\n" +
                    runHelp() + "\n\n" +
                    helpHelp() + "\n\n" +
                    exitHelp() + "\n" +
                    divider
                )
            
            # Help all
            if len(command) == 1:
                print(allHelp())
            else:

                print(divider)
                match command[1].lower():
                    case "set":
                        print(setHelp())
                    case "info":
                        print(infoHelp())
                    case "run":
                        print(runHelp())
                    case "help":
                        print(helpHelp())
                    case "exit":
                        print(exitHelp())
                    case "me":
                        print("If you are in trouble, call 999 (UK) or your local emergency carrier.")
                    case _:
                        print(allHelp())
                print(divider)

        # Exit the program
        case "exit":
            print(divider)
            print("Goodbye!")
            print(divider, end="")
            quit()

        # Nothing doing
        case _:
            print(divider)
            print("Error: Command not found.")
            print(divider)
                
            
                
# The meat of the program
def main(logging_target, verbosity_flag):
    logging_trail: str = ""
    num_files_processed: int = 0
    
    # Add to the logging trail
    def printLog(msg: str, stdout: bool = False):
        nonlocal logging_trail
        logging_trail += msg + "\n"
        if verbosity_flag or stdout:
            print(msg)

    # Write to the log trail
    def writeLog():
        printLog("Writing log...")
        open(logging_target, "w").write(logging_trail)

    # Notify the user of logging
    if logging_target != "" and logging_target is not None:
        printLog(f"Begun logging at '{logging_target}'.")

    # Rootpath does not exist
    if rootpath != "." and os.path.exists(rootpath):
        printLog(f"Error: '{rootpath}' is not a valid path. Aborting.", True)
        writeLog()
        quit()

    # Empty extension
    if file_extension == "":
        printLog("Every empty file selected. Warning displayed.")

        if input("No extension selected. Are you sure you want to apply this operation to all empty files? [y/N]:").lower() in ["y", "yes"]:
            printLog("First Warning Bypassed. Testing user.")

            if input("Please type the following to confirm: arboreal-insights-beloved") == "arboreal-insights-beloved":
                printLog("Second warning bypassed. Every empty file selected.")
                pass
            else:
                printLog("Second warning failed. Aborting.", True)
                quit()

        else:
            printLog("First warning failed. Aborting.", True)
            quit()

    # Generate walk
    root = os.walk(rootpath, followlinks=True)
    # Enumerate walk
    for (dirpath, dirnames, filenames) in root:
        printLog(f"{dirpath} {dirnames} {filenames}")

        if ".git" in dirpath:
            printLog(f"Skipping Git managed folder '{dirpath}'...", True)
            printLog(divider, True)
            continue

        # Iterate files
        for file in filenames:
            printLog(f"Found file {dirpath}{dir_split}{file}.", True)

            # If file exists
            if file.endswith(file_extension):
                try:
                    # If file is empty
                    if os.path.getsize(dirpath+dir_split+file) == 0:
                        printLog(f"Selecting {file}.", True)
                        num_files_processed += 1
                        # Get the title properly
                        title: str = "".join(file.split(".")[:-1]).replace("-", " ").title()

                        # Message to print, write, and log
                        msg: str = str(
                            "---\n" +
                            "title: " + title + "\n" +
                            "description: \n" +
                            "published: true\n" +
                            "date: " + datetime.datetime.now().isoformat() + "\n" +
                            "tags: WikiBulk\n" +
                            "editor: markdown\n" +
                            "dateCreated: " + datetime.datetime.now().isoformat() + "\n"
                            "---\n" +
                            "\n" +
                            "# " + title + "\n" +
                            "\n\n\n<sub>Created with WikiBulk</sub>\n"
                        )

                        # Write to file
                        open(dirpath+dir_split+file, "w").write(msg)
                        # Log
                        printLog(f"Written to {file}.", True)
                        printLog(f"Wrote this to the {file}:\n```\n" + msg + "\n```")

                    else:
                        printLog(f"File {file} populated. Skipping...")

                    printLog(divider, True)
                # Catch if file does not have a calculable size
                except OSError:
                    printLog(f"Warning: '{dirpath}{dir_split}{file}' does not have a readable length.")
                    continue

    # Files processed stats
    print(divider)    
    printLog(f"Completed. {num_files_processed} files processed.", True)

    # Write the log
    if logging_target != "" and logging_target is not None:
        writeLog()

    print(divider)

# Runtime
welcome()
while True:
    term()
