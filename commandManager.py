from diskManager import cDISK_MANAGER
import os

class cCOMMAND_MANAGER:
    def __init__(self):

        self.cDISK = cDISK_MANAGER()
        print("Shell Started.")

    #Pega o comando e verifica se é para o Sistema real ou o virtual
    def command_line(self, cmd):
        if (len(cmd) > 1):
            parametro = cmd[1].split("/");
            for interator in cmd:
                if interator.find("dsk") == 1:
                   self.virtual_command_line(cmd)
                   return

        self.real_command_line(cmd)

    #Executa para o Sistema de arquivo Virtual
    def virtual_command_line(self, cmd):
        print("Virtual Command_line ", cmd)
        command = cmd[0]
        parametros = cmd[1:]

        for interator in range(len(parametros)):
            if parametros[interator].find("dsk") == 1:
                tmp = parametros[interator].split("/")
                tmp.remove("dsk")
                tmp = "/".join(tmp)
                parametros[interator] = tmp;


        if ("view" == command):
            self.cDISK.view_disk_data()

        if ("pwd" == command):
           self.cDISK.show_path()

        if ("mkdir" == command):

            tmp_folder = self.cDISK.current_folder
            tmp_parametros = parametros[0].split("/")
            count = 0;
            for verify in tmp_parametros:
                if verify != "":
                    count += 1

            if count <= 0: return

            self.cDISK.change_current_folder(".")
            for folder_interator in tmp_parametros[:-1]:
                if folder_interator != "":
                    self.cDISK.change_current_folder(folder_interator)


            self.cDISK.add_folder_on_disk(tmp_parametros[-1])
            self.cDISK.current_folder = tmp_folder

        if ("cd" == command):
           self.cDISK.change_current_folder("michel")

        if ("ls" == command):

            tmp_folder = self.cDISK.current_folder
            tmp_parametros = parametros[0].split("/")
            count = 0;
            for verify in tmp_parametros:
                if verify != "":
                    count += 1

            if count > 0:
                self.cDISK.change_current_folder(".")
                for folder_interator in tmp_parametros:
                    if folder_interator != "":
                        self.cDISK.change_current_folder(folder_interator)

            self.cDISK.show_data_in_folder()
            self.cDISK.current_folder = tmp_folder

    #Executa para o Sistema de arquivo Real
    def real_command_line(self, cmd):
        cmd = " ".join(cmd)
        os.system(cmd)
