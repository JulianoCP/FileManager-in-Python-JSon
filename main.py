from commandManager import cCOMMAND_MANAGER

def main():
    cCOMMAND = cCOMMAND_MANAGER()
    curent_folder = "/"

    while(True):
        cmd = input("SO-UTFPR@2021: <" + curent_folder + "> # ")
        cmd = cmd.split(" ")
        cCOMMAND.command_line(cmd)
        curent_folder = cCOMMAND.cDISK.return_correct_context(cCOMMAND.cDISK.current_folder)

if __name__ == '__main__':
    main()
