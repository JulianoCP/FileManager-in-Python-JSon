from commandManager import cCOMMAND_MANAGER

def main():
    cCOMMAND = cCOMMAND_MANAGER()

    while(True):
        cmd = input(" # ")
        cmd = cmd.split(" ")
        cCOMMAND.command_line(cmd)

if __name__ == '__main__':
    main()
