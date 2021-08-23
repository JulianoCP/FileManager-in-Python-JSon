import os
from diskManager import cDISK_MANAGER

def main():
    cDISK = cDISK_MANAGER()

    #cDISK.add_file_on_disk("juliano.jpg")
    #cDISK.erase_file_upload_to_disk("juliano.jpg")
    #cDISK.recover_file_on_disk("juliano.jpg")
    #cDISK.remove_file_on_disk("juliano.jpg")

    #cDISK.add_file_on_disk("codigo.pdf")
    #cDISK.erase_file_upload_to_disk("codigo.pdf")
    #cDISK.recover_file_on_disk("codigo.pdf")
    #cDISK.remove_file_on_disk("codigo.pdf")

    #cDISK.add_file_on_disk("ola.txt")
    #cDISK.erase_file_upload_to_disk("ola.txt")
    #cDISK.recover_file_on_disk("ola.txt")
    #cDISK.remove_file_on_disk("ola.txt")
    
    #cDISK.add_folder_on_disk("usr")
    #cDISK.change_current_folder("var")
    #cDISK.add_file_on_disk("juliano.txt")
    #cDISK.add_folder_on_disk("tmp")
    #cDISK.show_path()
    #cDISK.change_current_folder(".")
    #cDISK.show_path()
    #cDISK.change_current_folder("..")
    #cDISK.show_path()
    #cDISK.show_data_in_folder()
    #cDISK.erase_file_upload_to_disk("ola.txt")
    #cDISK.recover_file_on_disk("ola.txt")
    #cDISK.remove_file_on_disk("ola.txt")

    cDISK.save_disk()
    cDISK.view_disk_data()
    cDISK.erase_disk()

    #diretorio_atual = cDISK.show_path()
    #while(1):
    #    cmd = input(diretorio_atual+" # ")
    #    cmd = cmd.split(" ")

    #    if cmd[0] == "ls":
    #        cDISK.show_data_in_folder()
    #    elif cmd[0] == "mkdir":
    #        cDISK.add_folder_on_disk(cmd[1])
    #    elif cmd[0] == "cd":
    #        cDISK.change_current_folder(cmd[1])
    #    elif cmd[0] == "pwd":
    #        print(diretorio_atual)
    #    elif cmd[0] == "show":
    #        cDISK.view_disk_data()
    #    elif cmd[0] == "save":
    #        cDISK.persist_data()
    #    elif cmd[0] == "load":
    #        cDISK.add_file_on_disk(cmd[1])
    #    elif cmd[0] == "rm":
    #        cDISK.erase_file_upload_to_disk(cmd[1])
    #    elif cmd[0] == "rc":
    #        cDISK.recover_file_on_disk(cmd[1])
    #    diretorio_atual = cDISK.show_path()

if __name__ == '__main__': 
    main() 
