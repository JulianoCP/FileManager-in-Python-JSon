import os
from diskManager import cDISK_MANAGER

def main():
    cDISK = cDISK_MANAGER()

    #cDISK.add_folder_on_disk("Juliano", {})
    #cDISK.add_file_on_disk("codigo.pdf", {"codigo.pdf": "Ola"}, 20, 3)

    #cDISK.add_file_on_disk("michel.txt")
    cDISK.add_file_on_disk("juliano.txt")
    #cDISK.add_file_on_disk("codigo.pdf")

    #cDISK.recover_file_on_disk("codigo.pdf")
    #cDISK.add_folder_on_disk("home")

    #cDISK.remove_file_on_disk("juliano.txt")

    cDISK.scan_struct()
    cDISK.view_disk_data()

    cDISK.save_disk()
    #cDISK.erase_disk()

if __name__ == '__main__': 
    main() 
