import os, configparser, shutil, psutil

user_home = os.path.expanduser("~")
mods_folder_path = os.path.join(user_home, 'AppData', 'Roaming', '.minecraft', 'mods')
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

def countmods(folder_path):
    return sum(1 for file_name in os.listdir(folder_path) if file_name.endswith('.jar'))

def list_mod_folders(mods_folder):
    subfolders = get_sorted_subfolders(mods_folder)
    for i, subfolder in enumerate(subfolders, start=1):
        folder_path = os.path.join(mods_folder, subfolder)
        mods_count = countmods(folder_path)
        print(f"{i}. {subfolder} ({mods_count} mods)")

def save_assigned_folder(folder_name):
    config = configparser.ConfigParser()
    config['Settings'] = {'AssignedFolder': folder_name}
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

def get_sorted_subfolders(folder_path, exclude_folder=None):
    subfolders = sorted(f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)))
    if exclude_folder:
        subfolders = [folder for folder in subfolders if folder != exclude_folder]
    return subfolders

def choose_create_setup(mods_folder):
    subfolders = get_sorted_subfolders(mods_folder)
    empty_folders = [folder for folder in subfolders if countmods(os.path.join(mods_folder, folder)) == 0]
    while True:
        if len(empty_folders) == 1:
            print(f"The only empty folder is '{empty_folders[0]}'. What would you like to do?")
            print("1. Use this empty folder")
            print("2. Create a new folder")
            choice = input("Enter your choice: ")
            if choice == '1':
                return empty_folders[0]
            elif choice == '2':
                while True:
                    new_folder_name = input("Please enter the name of the new folder: ").strip()
                    if not new_folder_name:
                        print("Folder name cannot be empty. Please provide a valid name.")
                        continue
                    new_folder_path = os.path.join(mods_folder, new_folder_name)
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                        print(f"New folder '{new_folder_name}' created.")
                        return new_folder_name
                    else:
                        print(f"Folder '{new_folder_name}' already exists. Choosing existing folder.")
                        return new_folder_name
            else:
                print("Invalid choice. Exiting the program.")
                exit()
        elif len(empty_folders) > 1:
            print("Choose an empty folder to assign the mods to:")
            for i, folder in enumerate(empty_folders, start=1):
                print(f"{i}. {folder}")
            print(f"{i + 1}. Create a new folder")
            choice = input("Enter your choice: ")
            if choice.isdigit() and 1 <= int(choice) <= i + 1:
                if int(choice) == i + 1:
                    while True:
                        new_folder_name = input("Please enter the name of the new folder: ").strip()
                        if not new_folder_name:
                            print("Folder name cannot be empty. Please provide a valid name.")
                            continue
                        new_folder_path = os.path.join(mods_folder, new_folder_name)
                        if not os.path.exists(new_folder_path):
                            os.makedirs(new_folder_path)
                            print(f"New folder '{new_folder_name}' created.")
                            return new_folder_name
                        else:
                            print(f"Folder '{new_folder_name}' already exists. Choosing existing folder.")
                            return new_folder_name
                else:
                    return empty_folders[int(choice) - 1]
            else:
                print("Invalid choice. Exiting the program.")
                exit()
        else: 
            while True:
                new_folder_name = input("No empty folders found. Please enter a name to create a new folder: ").strip()
                if not new_folder_name:
                    print("Folder name cannot be empty. Please provide a valid name.")
                    continue
                new_folder_path = os.path.join(mods_folder, new_folder_name)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    print(f"New folder '{new_folder_name}' created.")
                    return new_folder_name
                else:
                    print(f"Folder '{new_folder_name}' already exists. Choosing existing folder.")
                    return new_folder_name

def advanced(mods_folder, exclude_folder=None):
    subfolders = get_sorted_subfolders(mods_folder)
    if exclude_folder:
        subfolders = [folder for folder in subfolders if folder != exclude_folder]
    empty_folders = [folder for folder in subfolders if countmods(os.path.join(mods_folder, folder)) == 0]
    if len(empty_folders) == 1:
        choice = input(f"Assign the mods to the only empty folder '{empty_folders[0]}'? (y/n): ")
        if choice.lower() == 'y':
            return empty_folders[0]
        elif choice.lower() == 'n':
            return create(mods_folder, True)
        else:
            print("Invalid choice. Exiting the program.")
            exit()
    elif len(empty_folders) > 1:
        print("Choose an empty folder to assign the mods to:")
        for i, folder in enumerate(empty_folders, start=1):
            print(f"{i}. {folder}")
        print(f"{i + 1}. Create a new folder")
        print(f"{i + 2}. Keep the assigned folder and return to the main menu")
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= i + 2:
            if int(choice) == i + 1:
                return create(mods_folder, False)
            elif int(choice) == i + 2:
                print("Returning to the main menu.")
                return None
            else:
                return empty_folders[int(choice) - 1]
        else:
            print("Invalid choice. Exiting the program.")
            exit()
    else:
        return create(mods_folder, True)

def get_other_empty_folder(mods_folder, assigned_folder):
    subfolders = [f for f in os.listdir(mods_folder) if os.path.isdir(os.path.join(mods_folder, f))]
    empty_folders = [folder for folder in subfolders if countmods(os.path.join(mods_folder, folder)) == 0 and folder != assigned_folder]
    if len(empty_folders) == 1:
        return empty_folders[0]
    else:
        return None

def create(mods_folder, setup):
    while True:
        new_folder_name = input("Please enter the name of the new folder: ").strip()
        if not new_folder_name:
            print("Folder name cannot be empty. Please provide a valid name.")
            continue
        new_folder_path = os.path.join(mods_folder, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"New folder '{new_folder_name}' created.")
            return new_folder_name
        else:
            if setup:
                print(f"Folder '{new_folder_name}' already exists. Choosing existing folder.")
                return new_folder_name
            else:
                print(f"Folder '{new_folder_name}' already exists. Please provide a different name.")
                continue

def get_assigned_folder():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config.get('Settings', 'AssignedFolder', fallback='')

def setup():
    print("Setup:")
    assigned_folder = choose_create_setup(mods_folder_path)
    if assigned_folder is not None:
        print(f"\nAssigning mods to folder: {assigned_folder}")
        save_assigned_folder(assigned_folder)
        print(f"\nAssigned Folder: {assigned_folder}")

def initialize():
    assigned_folder = get_assigned_folder()
    if assigned_folder and not os.path.exists(os.path.join(mods_folder_path, assigned_folder)):
        print(f"The assigned folder '{assigned_folder}' no longer exists. Removing assignment and running setup.")
        save_assigned_folder('')
        setup()
    elif not assigned_folder:
        setup()
    else:
        print(f"\nAssigned Folder: {assigned_folder}")

def main_menu():
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")
        handle_choice(choice)

def display_main_menu():
    print("\nMain Menu:")
    print("1. Display all mod folders")
    print("2. Reassign assigned folder")
    print("3. Unassign current assigned folder")
    print("4. Swap mods with a different mod folder")
    print("5. Exit the program")

def handle_choice(choice):
    if choice == '1':
        list_mod_folders(mods_folder_path)
    elif choice == '2':
        reassign()
    elif choice == '3':
        unassign()
    elif choice == '4':
        swap()
    elif choice == '5':
        print("Exiting the program.")
        exit()
    else:
        print("Invalid choice. Exiting the program.")
        exit()

def reassign():
    assigned_folder = get_assigned_folder()
    subfolders = get_sorted_subfolders(mods_folder_path)
    if assigned_folder in subfolders and countmods(os.path.join(mods_folder_path, assigned_folder)) == 0:
        other_empty_folder = get_other_empty_folder(mods_folder_path, assigned_folder)
        if other_empty_folder:
            handle_reassign(assigned_folder, other_empty_folder, subfolders)
        else:
            assigned_folder = advanced(mods_folder_path)
            if assigned_folder is not None:
                print(f"\nReassigning mods to folder: {assigned_folder}")
                save_assigned_folder(assigned_folder)
    else:
        assigned_folder = advanced(mods_folder_path)
        if assigned_folder is not None:
            print(f"\nReassigning mods to folder: {assigned_folder}")
            save_assigned_folder(assigned_folder)

def handle_reassign(assigned_folder, other_empty_folder, subfolders):
    if len(subfolders) == 2:
        print(f"\nThere is only one other folder: '{other_empty_folder}'.")
    else:
        choice(assigned_folder, other_empty_folder)

def choice(assigned_folder, other_empty_folder):
    print(f"\nYour mods are currently assigned to the empty folder '{assigned_folder}'.")
    print("What would you like to do?")
    print(f"1. Assign the mods to the only other empty folder '{other_empty_folder}'")
    print("2. Create a new folder to assign the mods to")
    print(f"3. Keep the mods assigned to '{assigned_folder}' and go back to the main menu")
    choice = input("Enter your choice: ")
    if choice == '1':
        assigned_folder = other_empty_folder
        print(f"\nReassigning mods to folder: {assigned_folder}")
        save_assigned_folder(assigned_folder)
    elif choice == '2':
        assigned_folder = create(mods_folder_path, True)
        if assigned_folder is not None:
            print(f"\nReassigning mods to folder: {assigned_folder}")
            save_assigned_folder(assigned_folder)
            return
    elif choice == '3':
        print("Returning to the main menu.")
        initialize()
    else:
        print("Invalid choice. Returning to the main menu.")
        initialize()

def unassign():
    assigned_folder = get_assigned_folder()
    if assigned_folder:
        print(f"Unassigning current assigned folder: {assigned_folder}")
        folder_path = os.path.join(mods_folder_path, assigned_folder)
        if countmods(folder_path) == 0:
            print("Assigned folder is empty. Running setup to assign a new folder.")
            setup()
        else:
            save_assigned_folder('')
    else:
        print("No folder is currently assigned. Running setup to assign a new folder.")
        setup()

def swap():
    if check():
        print("Minecraft is currently running. Please close it before swapping mods.")
        print("Returning to the main menu.")
        return
    assigned_folder = get_assigned_folder()
    if not assigned_folder or not os.path.exists(os.path.join(mods_folder_path, assigned_folder)):
        print("No assigned mods folder or the assigned folder doesn't exist.")
        return
    print(f"Swapping mods in the assigned folder '{assigned_folder}':")
    assigned_folder_path = os.path.join(mods_folder_path, assigned_folder)
    mods_in_assigned_folder = getmods(assigned_folder_path)
    available_folders = sorted(available(mods_folder_path, assigned_folder))
    if not available_folders:
        print("No eligible mod folders to swap with.")
        return
    mods_in_main_folder = getmods(mods_folder_path)
    for mod_file in mods_in_main_folder:
        src_path = os.path.join(mods_folder_path, mod_file)
        dest_path = os.path.join(assigned_folder_path, mod_file)
        shutil.move(src_path, dest_path)
    if not available_folders:
        print("No eligible mod folders to swap with.")
        return
    print("Choose a mod folder to swap with:")
    for i, folder in enumerate(available_folders, start=1):
        folder_path = os.path.join(mods_folder_path, folder)
        mods_count = countmods(folder_path)
        print(f"{i}. {folder} ({mods_count} mods)")
    print(f"{i + 1}. Cancel and go back to the main menu")
    choice = input("Enter your choice: ")
    if choice.isdigit() and 1 <= int(choice) <= i + 1:
        if int(choice) == i + 1:
            print("Canceling. Returning to the main menu.")
            for mod_file in mods_in_main_folder:
                src_path = os.path.join(assigned_folder_path, mod_file)
                dest_path = os.path.join(mods_folder_path, mod_file)
                shutil.move(src_path, dest_path)
            for mod_file in mods_in_assigned_folder:
                src_path = os.path.join(mods_folder_path, mod_file)
                dest_path = os.path.join(assigned_folder_path, mod_file)
                shutil.move(src_path, dest_path)
            return
        else:
            selected_folder = available_folders[int(choice) - 1]
            selected_folder_path = os.path.join(mods_folder_path, selected_folder)
            mods_in_selected_folder = getmods(selected_folder_path)
            for mod_file in mods_in_selected_folder:
                src_path = os.path.join(selected_folder_path, mod_file)
                dest_path = os.path.join(mods_folder_path, mod_file)
                shutil.move(src_path, dest_path)
            save_assigned_folder(selected_folder)
            print(f"Mods swapped successfully. Assigned Folder is now '{selected_folder}'.")
    else:
        print("Invalid choice. Mods not swapped.")
        for mod_file in mods_in_main_folder:
            src_path = os.path.join(assigned_folder_path, mod_file)
            dest_path = os.path.join(mods_folder_path, mod_file)
            shutil.move(src_path, dest_path)
        for mod_file in mods_in_assigned_folder:
            src_path = os.path.join(mods_folder_path, mod_file)
            dest_path = os.path.join(assigned_folder_path, mod_file)
            shutil.move(src_path, dest_path)

def check():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'javaw.exe' in process.info['name'] and 'minecraft' in ' '.join(process.info['cmdline']).lower():
            return True
    return False
def available(mods_folder, assigned_folder):
    subfolders = [f for f in os.listdir(mods_folder) if os.path.isdir(os.path.join(mods_folder, f)) and f != assigned_folder and countmods(os.path.join(mods_folder, f)) > 0]
    return subfolders
def getmods(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.jar')]

initialize()
main_menu()