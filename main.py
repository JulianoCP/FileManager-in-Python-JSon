import os
from discManager2 import cDISC_MANAGER

def main():
    cDISC = cDISC_MANAGER()
    #cDISC.add_in_folder_on_disc("Juliano", {})
    #cDISC.add_in_file_on_disc("codigo.pdf", {"codigo.pdf": "Ola"}, 20, 3)
    #cDISC.add_in_file_on_disc("codigo.pdf", 20, 1)
    cDISC.recover_file_on_disc([0])
    cDISC.view_disc_data()
    #cDISC.save_disc()
    exit()

if __name__ == '__main__': 
    main() 
