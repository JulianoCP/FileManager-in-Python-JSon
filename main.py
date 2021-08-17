from discManager import cDISC_MANAGER

def main():
    cDISC = cDISC_MANAGER()
    #cDISC.add_in_folder_on_disc("Juliano", {})
    cDISC.add_in_file_on_disc("juliano.txt", {"juliano.txt": "Ola"}, 20, 3)
    cDISC.view_disc_data()
    cDISC.save_disc()
    exit()

if __name__ == '__main__': 
    main() 