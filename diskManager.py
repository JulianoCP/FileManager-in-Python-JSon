import json, base64, os, math

DISK_NAME = "disk.dsk" #Nome do disco.
SIZE_DISK = 4 #Tamanho total do disko em KB/s.
SIZE_BLOCK = 1 #Tamanho dos blocos em KB/s.

#Class responsavel por manipular as informações do disko que vao ser salva no .dsk
class cDISK_MANAGER:
    #Construtor do disko.
    def __init__(self):
        self.file_name = DISK_NAME
        self.current_folder = "/"

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
                "folders": {
                    "/": []
                },
                "environmental_variables": {
                    "block_list_avaliable": [],
                    "size_block_list": 0,
                    "size_block": SIZE_BLOCK,
                    "indice_file" : 0,
                }
            }
            while(struct_to_disk["environmental_variables"]["size_block_list"] < math.ceil(SIZE_DISK / SIZE_BLOCK)):
                struct_to_disk["environmental_variables"]["block_list_avaliable"].append(True)
                struct_to_disk["blocks"]["block_list"].append(None)
                struct_to_disk["environmental_variables"]["size_block_list"] += 1

            with open(DISK_NAME, "w") as file_write:
                json.dump(struct_to_disk, file_write)

            print("Disc created successfully.")
            self.file_pointer = open(self.file_name)
            self.disk_data = json.load(self.file_pointer)
        finally:
            print("Disk opened successfully.")

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
            self.disk_data["environmental_variables"]["block_list_avaliable"][indice_block] = True
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
        try:
            start_chunk = 0
            list_block_used = []
            extract_info_file = file_name.split(".")

            with open(file_name, "rb") as file:
                    file_bytes = file.read()

            b64 = base64.b64encode(file_bytes)
            size_bytes = os.path.getsize(file_name)
            amount_block = math.ceil(((size_bytes) / 1000)  / SIZE_BLOCK)
            chunk = math.ceil((len(b64) / amount_block ))

            for indice in range(len(self.disk_data["environmental_variables"]["block_list_avaliable"])):
                if amount_block <= 0: break
                if self.disk_data["environmental_variables"]["block_list_avaliable"][indice]:
                    self.disk_data["environmental_variables"]["block_list_avaliable"][indice] = False
                    self.add_block_on_disk(indice, b64[start_chunk : start_chunk + chunk])
                    list_block_used.append(indice)

                    if ((start_chunk + chunk) > len(b64)):
                        chunk = len(b64)
                    else:
                        start_chunk += chunk
                        
                    amount_block -= 1

            self.disk_data["files"]["file_list"].update(
                {   self.current_folder + file_name : {
                        "file_name" : extract_info_file[0],
                        "extension_file" : extract_info_file[1],
                        "bytes_used" : size_bytes,
                        "block_used" : list_block_used
                    }
                }
            )

            self.disk_data["folders"][self.current_folder].append(file_name)
            self.erase_file_upload_to_disk(file_name)
            self.persist_data()

        except:
            print("Failed to add file to disk.")
