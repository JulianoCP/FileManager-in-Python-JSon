import json, base64, os, math
from typing import Iterator

DISK_NAME = "disk.dsk" #Nome do disco.
SIZE_DISK = 16 #Tamanho total do disko em KB/s.
SIZE_BLOCK = 4 #Tamanho dos blocos em KB/s.
SIZE_BYTES_BLOCK = 50 #Quantidade de byte em cada bloco.

DEFAULT_CARACTER = "="
MAX_SIZE_FOLDER_NAME = 10
MAX_SIZE_FILE_NAME = 10
MAX_SIZE_EXTENSION_NAME = 10
MAX_SIZE_METADATA_FILE = 10

AMOUNT_BLOCK_AVAILABLE_TO_FILE = 20

#Class responsavel por manipular as informações do disko que vao ser salva no .dsk
class cDISK_MANAGER:
    #Construtor do disko.
    def __init__(self):
        self.file_name = DISK_NAME
        self.current_folder = "/"
        self.default_value_block = ""

        start_folder = self.current_folder
        for interator in range(MAX_SIZE_FOLDER_NAME - len(self.current_folder)):
            start_folder += DEFAULT_CARACTER
        self.current_folder = start_folder

        for interator in range(SIZE_BYTES_BLOCK):
            self.default_value_block += DEFAULT_CARACTER

        try:
            print("Looking for the disk.")
            self.file_pointer = open(self.file_name)
            self.disk_data = json.load(self.file_pointer)
        except:
            print("Disc not found.")
            struct_to_disk = {
                "blocks": {
                    "block_list" : []
                },
                "files" : {
                    "file_list": {}
                },
                "folders": {},
                "environmental_variables": {
                    "block_list_available": [],
                    "amount_block_available" : 0,
                    "size_block": SIZE_BLOCK,
                    "indice_file" : 0,
                }
            }
            while(len(struct_to_disk["environmental_variables"]["block_list_available"]) < math.ceil(SIZE_DISK / SIZE_BLOCK)):
                struct_to_disk["environmental_variables"]["block_list_available"].append(1)
                struct_to_disk["environmental_variables"]["amount_block_available"] += 1
                struct_to_disk["blocks"]["block_list"].append(self.default_value_block)
            
            struct_to_disk["folders"].update({self.current_folder : {}})

            with open(DISK_NAME, "w") as file_write:
                json.dump(struct_to_disk, file_write)

            print("Disc created successfully.")
            self.file_pointer = open(self.file_name)
            self.disk_data = json.load(self.file_pointer)
        finally:
            print("Disk opened successfully.")

    #Função para mostrar ao usuario o erro caso ocorra um excecao por 'None'
    def show_message_if_none(self, msg, result):
        if result == None:
            print(msg)
            exit()

    #Função para montar os blockos usados.
    def set_block_used(self, blocks_list):
        block_result = []
        for interator in range(AMOUNT_BLOCK_AVAILABLE_TO_FILE):
            if interator < len(blocks_list):
                block_result.append(blocks_list[interator])
            else:
                block_result.append(None)
        return block_result

    #Verifica o tamanho do arquivo, caso seja aceita ele é completado com valor default.
    def verify_size_string(self, name, expected_size):
        if len(name) <= expected_size:
            new_name = name
            for interator in range(expected_size - len(name)):
                new_name += DEFAULT_CARACTER
            return new_name
        else:
            return None

    #Verifica se tem espaco suficiente nos blocos.
    def verify_has_block_available(self, size_file):
        if size_file <= self.disk_data["environmental_variables"]["amount_block_available"]:
            return True
        return None

    #Metodo que persiste os dados no disko.
    def persist_data(self):
        try:
            with open(DISK_NAME, "w") as file_write:
                json.dump(self.disk_data, file_write)
        except:
            print("Failed to persist data.")

    #Metodo para ser chamada antes de fechar o programa
    def save_disk(self):
        try:
            self.file_pointer.close()
            self.persist_data()
        except:
            print("Failed, disk impossible to save.")

    #Metodo para deletar o disco dsk
    def erase_disk(self):
        try:
            os.remove(DISK_NAME)
            print(DISK_NAME + " deleted.")
        except:
            print("Failed, disk not found.")
    
    #Metodo para deletar o arquivo que foi mandado para nosso dsk
    def erase_file_upload_to_disk(self, file_name):
        try:
            os.remove(file_name)
            print(DISK_NAME + " deleted.")
        except:
            print("Failed, file not found.")

    #Metodo que mostra a estrutura do disko.
    def view_disk_data(self):
        try:
            print(json.dumps(self.disk_data, indent = 4))
        except:
            print("Failed, to dumps json.")

    #Metodo que adiciona novo bloco utilizazdo no disko/atualizar algum já existente.
    def add_block_on_disk(self, indice_block, chunk):
        try:
            self.disk_data["blocks"]["block_list"][indice_block] = (chunk).decode("utf8")
        except:
            print("Failed, unable to add block to disk.")
    
    #Metodo que remove os dados contidos no block_list[indice_block]
    def remove_block_on_disk(self, indice_block):
        try:
            self.disk_data["blocks"]["block_list"][indice_block] = None
            self.disk_data["environmental_variables"]["block_list_available"][indice_block] = 1
        except:
            print("Failed to erase block on disk.")

    #Metodo que deleta o arquivo do disco.
    def remove_file_on_disk(self, file_name):
        try:
            extract_file = self.disk_data["files"]["file_list"][self.current_folder + file_name]

            for block in extract_file["block_used"]:
                self.remove_block_on_disk(block)
            
            self.disk_data["files"]["file_list"].pop((self.current_folder + file_name), None)
            self.disk_data["folders"][self.current_folder].remove(file_name)
        except:
            print("Failed to remove file.")

    #Metodo que reconstroi o arquivo apatir dos bytes salvos nos blocos.
    def recover_file_on_disk(self, file_name):
        try:
            recover_bytes = ""
            extract_file = self.disk_data["files"]["file_list"][self.current_folder + file_name]

            for block in extract_file["block_used"]:
                recover_bytes += self.disk_data["blocks"]["block_list"][block]

            decode_b64 = base64.b64decode(recover_bytes)
            file = open(file_name, 'wb')
            file.write(decode_b64)
            file.close()
        except:
            print("File recovery failed.")

    #Metodo que muda para o diretorio selecionado se existir.
    def change_current_folder(self, name_folder):
        try:
            self.current_folder = name_folder
        except:
            print("Failure, invalid directory.")

    #Metodo que adiciona novo diretorio no disko/atualizar algum já existente.
    def add_folder_on_disk(self, name_folder):
        try:
            self.disk_data["folders"].update({name_folder : []})
            self.persist_data()
        except:
            print("Failed, unable to add folder on disk.")

    #Metodo que adiciona novo arquivo no disko/atualizar algum já existente.
    def add_file_on_disk(self, file_name):
        #try:
            start_chunk = 0
            list_block_used = []
            extract_soft_info_file = [None, None]
            extract_hard_info_file = file_name.split(".") #[0] - Nome arquivo / [1] - Extensao do arquivo.
            extract_soft_info_file[0] = self.verify_size_string(extract_hard_info_file[0], MAX_SIZE_FILE_NAME)
            extract_soft_info_file[1] = self.verify_size_string(extract_hard_info_file[1], MAX_SIZE_EXTENSION_NAME)

            self.show_message_if_none("File name, extrapolated size.", extract_soft_info_file[0])
            self.show_message_if_none("File extension extrapolated size.", extract_soft_info_file[1])

            with open(file_name, "rb") as file:
                file_bytes = file.read()

            b64 = base64.b64encode(file_bytes)
            size_64_encode = len(b64)
            amount_block = math.ceil(((size_64_encode) / 1000)  / SIZE_BLOCK)
            has_available_slot = self.verify_has_block_available(amount_block)
            self.show_message_if_none("Don't have space to insert file.", has_available_slot)
            chunk = math.ceil((size_64_encode / amount_block ))



            #for indice in range(len(self.disk_data["environmental_variables"]["block_list_available"])):
            #    if amount_block <= 0: break
            #    if self.disk_data["environmental_variables"]["block_list_available"][indice]:
            #        self.disk_data["environmental_variables"]["block_list_available"][indice] = 0
            #        self.add_block_on_disk(indice, b64[start_chunk : start_chunk + chunk])
            #        list_block_used.append(indice)
            #
            #        if ((start_chunk + chunk) > len(b64)):
            #            chunk = len(b64)
            #        else:
            #            start_chunk += chunk
            #            
            #        amount_block -= 1

            self.disk_data["files"]["file_list"].update(
                {   
                    self.current_folder + extract_soft_info_file[0] : 
                    {
                        "file_name" : extract_soft_info_file[0],
                        "extension_file" : extract_soft_info_file[1],
                        "bytes_used" : self.verify_size_string(str(size_64_encode), MAX_SIZE_METADATA_FILE),
                        "block_used" : self.set_block_used(list_block_used)
                    }
                }
            )

            self.disk_data["folders"][self.current_folder].update({file_name : extract_soft_info_file[0]})
            #self.erase_file_upload_to_disk(file_name)
            self.persist_data()

        #except:
         #   print("Failed to add file to disk.")
