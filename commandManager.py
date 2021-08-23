from diskManager import cDISK_MANAGER
import os

class cCOMMAND_MANAGER:
    #Constructor.
    def __init__(self):
        self.save_old_folder_name = ""
        self.save_olf_folder_indice = 0

        self.cDISK = cDISK_MANAGER()
        print("Shell Started.")

    #Pega o comando e verifica se é para o Sistema real ou o virtual
    def command_line(self, cmd):
        if (len(cmd) > 1):
            parametro = cmd[1].split("/")
            for interator in cmd:
                if interator.find("dsk") == 1:
                   self.virtual_command_line(cmd)
                   return

        self.real_command_line(cmd)

    #Splita o commando para ser utilizado no disco virtual.
    def virtual_command_line(self, cmd):
        command = cmd[0]
        parametros = cmd[1:]

        for interator in range(len(parametros)):
            if parametros[interator].find("dsk") == 1:
                tmp = parametros[interator].split("/")
                tmp.remove("dsk")
                tmp = "/".join(tmp)
                parametros[interator] = tmp

        #Trata o commando VIEW.
        if ("view" == command):
            self.cDISK.view_disk_data()

        #Trata o commando PWD.
        if ("pwd" == command):
            self.save_current_folder()
            tmp_parametros = parametros[0].split("/")

            if self.verify_caracter_empty(tmp_parametros) > 0:
                self.cDISK.change_current_folder(".")
                for folder_interator in tmp_parametros:
                    if folder_interator != "":
                        self.cDISK.change_current_folder(folder_interator)

            self.cDISK.show_path()
            self.recover_old_folder()

        #Trata o commando MKDIR.
        if ("mkdir" == command):
            self.save_current_folder()
            tmp_parametros = parametros[0].split("/")

            if self.verify_caracter_empty(tmp_parametros) <= 0: return

            self.cDISK.change_current_folder(".")
            for folder_interator in tmp_parametros[:-1]:
                if folder_interator != "":
                    self.cDISK.change_current_folder(folder_interator)

            self.cDISK.add_folder_on_disk(tmp_parametros[-1])
            self.recover_old_folder()

        #Trata o commando CD.
        if ("cd" == command):
            tmp_parametros = parametros[0].split("/")

            if self.verify_caracter_empty(tmp_parametros) <= 0: return
            for folder_interator in tmp_parametros:
                if folder_interator != "":
                    self.cDISK.change_current_folder(folder_interator)
        
        #Trata o commando LS.
        if ("ls" == command):
            self.save_current_folder()
            tmp_parametros = parametros[0].split("/")

            if self.verify_caracter_empty(tmp_parametros) > 0:
                self.cDISK.change_current_folder(".")
                for folder_interator in tmp_parametros:
                    if folder_interator != "":
                        self.cDISK.change_current_folder(folder_interator)

            self.cDISK.show_data_in_folder()
            self.recover_old_folder()

    #Executa para o Sistema de arquivo Real
    def real_command_line(self, cmd):
        cmd = " ".join(cmd)
        os.system(cmd)

    #Verifica a quantidade de caracter empty.
    def verify_caracter_empty(self, param):
        count = 0
        for verify in param:
            if verify != "": count += 1
        return count

    #Salva os dados do diretorio atual.
    def save_current_folder(self):
        self.save_old_folder_name = self.cDISK.current_folder
        self.save_old_indice_folder = self.cDISK.current_folder_indice
    
    #Recupera os dados do diretorio que era o atual.
    def recover_old_folder(self):
        self.cDISK.current_folder = self.save_old_folder_name
        self.cDISK.current_folder_indice = self.save_old_indice_folder