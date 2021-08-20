import json, base64, os, math, sys

DISK_NAME = "disk.dsk" #Nome do disco.

SIZE_DISK = 16 #Tamanho total do disko em KB/s.
SIZE_BLOCK = 4 #Tamanho dos blocos em KB/s.
SIZE_BYTES_BLOCK = 1024 #Quantidade de byte em cada bloco.

DEFAULT_CARACTER = "=" #Caracter defaul para preencher os campos do json.
DEFAULT_CARACTER_FOLDEDR = "/" #Caracter defaul para preencher o primeiro folder.

MAX_SIZE_FILE_NAME = 20 #Nome maximo suportado para um file.
MAX_SIZE_FOLDER_NAME = 20 #Nome maximo suportado para um folder.
MAX_SIZE_METADATA_FILE = 20 #Nome maximo para os metadados de um file.
MAX_ADDRESSES_IN_BLOCK = 5 #Quantidade maximo de blocos que podem ser enderecados, lembrando que 5 == "00000" ou seja até 99999 blocos

AMOUNT_FILE = 2 #Quantidade maxima de files no disco.
AMOUNT_FOLDER = 5 #Quantidade maxima de folders no disco.
AMOUNT_DATA_IN_FOLDER = 3 #Quantidade de itens em um folder.
AMOUNT_BLOCK_AVAILABLE_TO_FILE = 5 #Quantidade maximo de blocks de enderecamento que pode ser usadas por um file.

#Class responsavel por manipular as informações do disko que vao ser salva no .dsk
class cDISK_MANAGER:
    #Construtor do disko.
    def __init__(self):
        self.file_name = DISK_NAME
        self.current_folder = DEFAULT_CARACTER_FOLDEDR
        self.current_folder_indice = 0
        self.default_value_block = ""
        self.default_block_used_files = []

        self.register_files = ""
        self.register_folder = ""
        self.register_env = ""

        start_folder = DEFAULT_CARACTER_FOLDEDR
        for interator in range(MAX_SIZE_FOLDER_NAME - len(DEFAULT_CARACTER_FOLDEDR)):
            start_folder += DEFAULT_CARACTER
        self.current_folder = start_folder

        for interator in range(SIZE_BYTES_BLOCK):
            self.default_value_block += DEFAULT_CARACTER

        for interator in range(AMOUNT_BLOCK_AVAILABLE_TO_FILE):
            self.default_block_used_files.append(self.create_default_name_using_size(MAX_ADDRESSES_IN_BLOCK))

        try:
            print("Looking for the disk.")
            self.file_pointer = open(self.file_name)
            self.disk_data = json.load(self.file_pointer)
        except:
            print("Disc not found.")
            struct_to_disk = {
                "blocks": [],
                "files" : [],
                "folders": [],
                "environmental_variables": {
                    "block_list_available": [],
                    "file_list_available": [],
                    "folder_list_available" : [],
                    "amount_block_available" : 0,
                }
            }

            while(len(struct_to_disk["environmental_variables"]["block_list_available"]) < math.ceil(SIZE_DISK / SIZE_BLOCK)):
                struct_to_disk["environmental_variables"]["block_list_available"].append(1)
                struct_to_disk["blocks"].append(self.default_value_block)

            struct_to_disk["environmental_variables"]["amount_block_available"] = self.verify_size_string(str(len(struct_to_disk["environmental_variables"]["block_list_available"])), 10)
            self.register_env += str(struct_to_disk["environmental_variables"])

            for interator in range(AMOUNT_FILE):
                struct_to_disk["files"].append(self.create_default_file())
                struct_to_disk["environmental_variables"]["file_list_available"].append(1)
            
            vet_folder_inside = []
            for indice in range(AMOUNT_DATA_IN_FOLDER):
                vet_folder_inside.append(self.create_default_name_using_size(MAX_SIZE_FILE_NAME))

            for interator in range(AMOUNT_FOLDER):
                struct_to_disk["folders"].append(
                    [
                        self.create_default_name_using_size(MAX_SIZE_FOLDER_NAME),
                        vet_folder_inside
                    ]
                )
                struct_to_disk["environmental_variables"]["folder_list_available"].append(1)

            self.register_folder += str(struct_to_disk["folders"])
            struct_to_disk["folders"][0][0] = self.current_folder

            #Seta o primeiro bloco com dados dos files.
            mnt_data = self.verify_size_string(("files" + self.register_files), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated files.", mnt_data)
            struct_to_disk["blocks"][0] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][0] = 0

            #Seta o segundo bloco com dados dos folders.
            mnt_data = self.verify_size_string(("folders" + self.register_folder), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated folders.", mnt_data)
            struct_to_disk["blocks"][1] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][1] = 0

            #Seta o segundo bloco com dados dos folders.
            mnt_data = self.verify_size_string(("environmental_variables" + self.register_env), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated environmental.", mnt_data)
            struct_to_disk["blocks"][2] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][2] = 0

            with open(DISK_NAME, "w") as file_write:
                json.dump(struct_to_disk, file_write)

            print("Disc created successfully.")
            self.file_pointer = open(self.file_name)
            self.disk_data = json.load(self.file_pointer)
        finally:
            print("Disk opened successfully.")

    #Cria mockup de files.
    def create_default_file(self):
        mock_file = {
                        "file_name" : self.create_default_name_using_size(MAX_SIZE_METADATA_FILE),
                        "extension_file" : self.create_default_name_using_size(MAX_SIZE_METADATA_FILE),
                        "bytes_used" : self.create_default_name_using_size(MAX_SIZE_METADATA_FILE),
                        "block_used" : self.default_block_used_files
                    }
        for key in mock_file:
            self.register_files += str(key) + str(mock_file[key])
        return mock_file

    #Cria uma string de caracter defaulm usando como base um tamanho passado por parametro.
    def create_default_name_using_size(self, size):
        new_name = ""
        for interator in range(size):
            new_name += DEFAULT_CARACTER
        return new_name

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
                block_result.append(str(blocks_list[interator]))
            else:
                block_result.append(self.create_default_name_using_size(MAX_ADDRESSES_IN_BLOCK))
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
        mnt_amount = ""
        for caracter in self.disk_data["environmental_variables"]["amount_block_available"]:
            if caracter != DEFAULT_CARACTER:
                mnt_amount += caracter

        if size_file <= int(mnt_amount):
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
            data = (chunk).decode("utf8")
            if len(data) >= SIZE_BYTES_BLOCK:
                self.disk_data["blocks"][indice_block] = (chunk).decode("utf8")
            else:
                self.disk_data["blocks"][indice_block] = self.verify_size_string(data, SIZE_BYTES_BLOCK)
        except:
            print("Failed, unable to add block to disk.")
    
    #Metodo que remove os dados contidos no block_list[indice_block]
    def remove_block_on_disk(self, indice_block):
        try:
            self.disk_data["blocks"][indice_block] = None
            self.disk_data["environmental_variables"]["block_list_available"][indice_block] = 1
        except:
            print("Failed to erase block on disk.")

    #Metodo que deleta o arquivo do disco.
    def remove_file_on_disk(self, file_name):
        try:
            extract_file = self.disk_data["files"][self.current_folder + file_name]

            for block in extract_file["block_used"]:
                self.remove_block_on_disk(block)
            
            self.disk_data["files"].pop((self.current_folder + file_name), None)
            self.disk_data["folders"][self.current_folder].remove(file_name)
        except:
            print("Failed to remove file.")

    #Metodo que reconstroi o arquivo apatir dos bytes salvos nos blocos.
    def recover_file_on_disk(self, file_name):
        try:
            recover_bytes = ""
            extract_file = self.disk_data["files"][self.current_folder + file_name]

            for block in extract_file["block_used"]:
                recover_bytes += self.disk_data["blocks"][block]

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
            extract_soft_info_file = [None, None]
            extract_hard_info_file = file_name.split(".") #[0] - Nome arquivo / [1] - Extensao do arquivo.
            extract_soft_info_file[0] = self.verify_size_string(extract_hard_info_file[0], MAX_SIZE_FILE_NAME)
            extract_soft_info_file[1] = self.verify_size_string(extract_hard_info_file[1], MAX_SIZE_METADATA_FILE)

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

            for indice in range(len(self.disk_data["environmental_variables"]["block_list_available"])):
                if amount_block <= 0: break
                if self.disk_data["environmental_variables"]["block_list_available"][indice]:
                    self.disk_data["environmental_variables"]["block_list_available"][indice] = 0
                    self.add_block_on_disk(indice, b64[start_chunk : start_chunk + chunk])
                    list_block_used.append(self.verify_size_string(str(indice), MAX_ADDRESSES_IN_BLOCK))
            
                    if ((start_chunk + chunk) > len(b64)):
                        chunk = len(b64)
                    else:
                        start_chunk += chunk
                    amount_block -= 1

            for interator in range(len(self.disk_data["environmental_variables"]["file_list_available"])):
                if self.disk_data["environmental_variables"]["file_list_available"][interator]:
                    self.disk_data["files"][interator].update({"file_name" : extract_soft_info_file[0]}),
                    self.disk_data["files"][interator].update({"extension_file" : extract_soft_info_file[1]}),
                    self.disk_data["files"][interator].update({"bytes_used" : self.verify_size_string(str(size_64_encode), MAX_SIZE_METADATA_FILE)}),
                    self.disk_data["files"][interator]["block_used"] = self.set_block_used(list_block_used)
                    break

            self.disk_data["folders"][self.current_folder_indice][1][0] = extract_soft_info_file[0]
            #self.erase_file_upload_to_disk(file_name)
            self.persist_data()

        except:
            print("Failed to add file to disk.")
