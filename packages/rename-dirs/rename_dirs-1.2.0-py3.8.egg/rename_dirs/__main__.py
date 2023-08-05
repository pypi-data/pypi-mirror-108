def main():
    import os
    path = input("Enter full directory path: ")
    format = input('Choose the name format:\n1. Example File.txt\n2. Example-File.txt\n3. Example-file.txt\n4. Example_File.txt\n5. example file.txt\n6. example-file.txt\n7. example_file.txt\n\nEnter a number: ')
    files = os.listdir(path)
    mainDirectorylist = list()

    for i in files:
        if i.startswith(".") == False:
            mainDirectorylist.append(i)
            filename = i.lower()
            if " " in filename:
                filename = filename.replace(" ", "_")
            if "-" in filename:
                filename = filename.replace("-", "_")
            if "_" in filename:
                filename = filename.replace("_", "_")
            confirmation = input(
                f"\n{mainDirectorylist[files.index(i)]} => {filename} (Y/n): ")
            if confirmation.lower() == "y" or "":
                os.rename(
                    f"{path}/{mainDirectorylist[files.index(i)]}", f"{path}/{filename}")
            else:
                continue

    print("\n\nAight, I'm done!")
