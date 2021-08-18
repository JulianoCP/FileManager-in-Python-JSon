import os
from diskManager import cDISK_MANAGER

def main():
    cDISK = cDISK_MANAGER()

    #cDISK.add_in_folder_on_disk("Juliano", {})
    #cDISK.add_in_file_on_disk("codigo.pdf", {"codigo.pdf": "Ola"}, 20, 3)

    #cDISK.add_in_file_on_disk("michel.txt")
    #cDISK.add_in_file_on_disk("juliano.txt")

    #cDISK.recover_file_on_disk("juliano.txt")

    cDISK.view_disk_data()

    cDISK.save_disk()
    #cDISK.erase_disk()

if __name__ == '__main__': 
    main() 
