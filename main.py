from commandManager import cCOMMAND_MANAGER

def main():
    cCOMMAND = cCOMMAND_MANAGER()

    while(1):
        cmd = input(" # ")
        cmd = cmd.split(" ")
        cCOMMAND.command_line(cmd)

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

    #cDISK.save_disk()
    #cDISK.view_disk_data()
    #cDISK.erase_disk()

if __name__ == '__main__':
    main()
