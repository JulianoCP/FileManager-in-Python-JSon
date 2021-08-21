import os
from diskManager import cDISK_MANAGER

def main():
    cDISK = cDISK_MANAGER()

    #cDISK.add_file_on_disk("michel.txt")
    #cDISK.add_file_on_disk("ola.txt")

    #cDISK.add_file_on_disk("juliano.jpg")
    #cDISK.erase_file_upload_to_disk("juliano.jpg")
    #cDISK.view_disk_data()
    #cDISK.recover_file_on_disk("juliano.jpg")

    cDISK.add_file_on_disk("codigo.pdf")
    cDISK.erase_file_upload_to_disk("codigo.pdf")
    cDISK.recover_file_on_disk("codigo.pdf")

    #cDISK.add_file_on_disk("ola.txt")
    #cDISK.erase_file_upload_to_disk("ola.txt")
    #cDISK.recover_file_on_disk("ola.txt")

    #cDISK.remove_file_on_disk("codigo.pdf")

    cDISK.save_disk()
    #cDISK.view_disk_data()
    cDISK.erase_disk()

    #VER DPS
    #cDISK.discover_file_on_folder("michel.txt")
    #cDISK.add_folder_on_disk("juliano.jpg")

if __name__ == '__main__': 
    main() 
