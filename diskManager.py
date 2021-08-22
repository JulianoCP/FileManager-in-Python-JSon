import json, base64, os, math, sys

DISK_NAME = "disk.dsk" #Nome do disco.

SIZE_DISK = 60 #Tamanho total do disko em KB/s.
SIZE_BLOCK = 4 #Tamanho dos blocos em KB/s.
SIZE_BYTES_BLOCK = 4096 #Quantidade de byte em cada bloco.
SIZE_TYPE_FOLDER = 1 #Tamanho maximo no campo TYPE do FOLDER.
SIZE_POINTER_FOLDER = 5 #Tamanho maximo do campo POINTER do FOLDER.

DEFAULT_CARACTER = "=" #Caracter defaul para preencher os campos do json.
DEFAULT_CARACTER_FOLDER_ROOT = "/" #Caracter defaul para preencher o primeiro folder.
DEFAULT_CARACTER_FILE = "A" #Caracter defaul para preencher se o bloco é um file na estrutura do folder.
DEFAULT_CARACTER_FOLDER = "F" #Caracter defaul para preencher se o bloco é um folder na estrutura do folder.

MAX_SIZE_FILE_NAME = 20 #Nome maximo suportado para um file.
MAX_SIZE_FOLDER_NAME = 20 #Nome maximo suportado para um folder.
MAX_SIZE_EXTENSION_FILE = 3 #Nome maximo de extensao
MAX_SIZE_METADATA_FILE = 20 #Nome maximo para os metadados de um file.
MAX_ADDRESSES_IN_BLOCK = 5 #Quantidade maximo de blocos que podem ser enderecados, lembrando que 5 == "00000" ou seja até 99999 blocos

AMOUNT_FILE = 2 #Quantidade maxima de files no disco.
AMOUNT_FOLDER = 3 #Quantidade maxima de folders no disco.
AMOUNT_DATA_IN_FOLDER = 3 #Quantidade de itens em um folder.
AMOUNT_BLOCK_AVAILABLE_TO_FILE = 20 #Quantidade maximo de blocks de enderecamento que pode ser usadas por um file.

#Class responsavel por manipular as informações do disko que vao ser salva no .dsk
class cDISK_MANAGER:
    #Construtor do disko.
    def __init__(self):
        self.file_name = DISK_NAME
        self.current_folder = DEFAULT_CARACTER_FOLDER_ROOT
        self.current_folder_indice = 0
        self.default_value_block = ""
        self.default_block_used_files = []

        self.register_files = ""
        self.register_folder = ""
        self.register_env = ""

        start_folder = DEFAULT_CARACTER_FOLDER_ROOT
        for interator in range(MAX_SIZE_FOLDER_NAME - len(DEFAULT_CARACTER_FOLDER_ROOT)):
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
                    "amount_file_available" : 0,
                    "amount_folder_available" : 0,
                }
            }

            #PREENCHE A ESTRUTURA DOS ENVIRONMENTAL.
            while(len(struct_to_disk["environmental_variables"]["block_list_available"]) < math.ceil(SIZE_DISK / SIZE_BLOCK)):
                struct_to_disk["environmental_variables"]["block_list_available"].append(1)
                struct_to_disk["blocks"].append(self.default_value_block)
            struct_to_disk["environmental_variables"]["amount_block_available"] = len(struct_to_disk["environmental_variables"]["block_list_available"])
            self.register_env += str(struct_to_disk["environmental_variables"])

            #CRIA OS FILES.
            for interator in range(AMOUNT_FILE):
                struct_to_disk["files"].append(self.create_default_file())
                struct_to_disk["environmental_variables"]["file_list_available"].append(1)
            struct_to_disk["environmental_variables"]["amount_file_available"] = len(struct_to_disk["environmental_variables"]["file_list_available"])
            
            #CRIA OS ESPACOS NO FOLDER INTERNO.
            vet_folder_inside = []
            for indice in range(AMOUNT_DATA_IN_FOLDER):
                vet_folder_inside.append([
                    self.create_default_name_using_size(MAX_SIZE_FILE_NAME),
                    self.create_default_name_using_size(SIZE_TYPE_FOLDER),
                    self.create_default_name_using_size(SIZE_POINTER_FOLDER)
                ])

            #FUNCAO AUXILIAR PARA CRIAR OS ESPACOS NA VARIAVEL DE AMBIENTE.
            vet_data_folder = []
            for interator in range(AMOUNT_DATA_IN_FOLDER):
                vet_data_folder.append(1)

            #CRIA VETOR DE ESPACOS LIVRES DENTRO DO FOLDER INTERNO NA VARAIVEL DE AMBIENTE.
            for interator in range(AMOUNT_FOLDER):
                struct_to_disk["environmental_variables"]["amount_folder_available"] += 1
                struct_to_disk["folders"].append(
                    [
                        self.create_default_name_using_size(MAX_SIZE_FOLDER_NAME),
                        vet_folder_inside
                    ]
                )
                struct_to_disk["environmental_variables"]["folder_list_available"].append(
                    [
                    1,
                    vet_data_folder
                    ]
                )

            #TRATANDO O FOLDER RAIZ
            self.register_folder += str(struct_to_disk["folders"])
            struct_to_disk["folders"][0][0] = self.current_folder
            struct_to_disk["environmental_variables"]["folder_list_available"][0][0] = 0
            struct_to_disk["environmental_variables"]["amount_folder_available"] -= 1

            #Seta o primeiro bloco com dados dos files.
            mnt_data = self.verify_size_string(("files" + self.register_files), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated files.", mnt_data)
            struct_to_disk["blocks"][0] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][0] = 0
            struct_to_disk["environmental_variables"]["amount_block_available"] -= 1 #UTILIZANDO UM BLOCO LOGICO PARA OS METADADOS DA TABELA DE ARQUIVOS.

            #Seta o segundo bloco com dados dos folders.
            mnt_data = self.verify_size_string(("folders" + self.register_folder), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated folders.", mnt_data)
            struct_to_disk["blocks"][1] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][1] = 0
            struct_to_disk["environmental_variables"]["amount_block_available"] -= 1 #UTILIZANDO UM BLOCO LOGICO PARA OS METADADOS DA TABELA DE FOLDERS.

            #Seta o segundo bloco com dados dos environmental.
            mnt_data = self.verify_size_string(("environmental_variables" + self.register_env), SIZE_BYTES_BLOCK)
            self.show_message_if_none("Failure, blocking limit for extrapolated environmental.", mnt_data)
            struct_to_disk["blocks"][2] = mnt_data
            struct_to_disk["environmental_variables"]["block_list_available"][2] = 0
            struct_to_disk["environmental_variables"]["amount_block_available"] -= 1 #UTILIZANDO UM BLOCO LOGICO PARA OS METADADOS DA TABELA DE FOLDERS.

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
                        "extension_file" : self.create_default_name_using_size(MAX_SIZE_EXTENSION_FILE),
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

    #Retorna o nome/bloco sem os "="
    def return_correct_context(self, content):
        return content.split(DEFAULT_CARACTER)[0]

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

    #Função que faz a releitura das estruturas padroes do json e rescreve os blocos logicos.
    def scan_struct(self):
        self.register_files = ""
        self.register_folder = ""
        self.register_env = ""

        for mock_file in self.disk_data["files"]:
            for key in mock_file:
                self.register_files += str(key) + str(mock_file[key])
        
        for mock_env in self.disk_data["environmental_variables"]:
            self.register_env += str(mock_env) + str(self.disk_data["environmental_variables"][mock_env])
        
        for mock_folder in self.disk_data["folders"]:
            self.register_folder += str(mock_folder)
        self.register_folder += "]"

        self.disk_data["blocks"][0] = self.verify_size_string(("files" + self.register_files), SIZE_BYTES_BLOCK)
        self.disk_data["blocks"][1] = self.verify_size_string(("folders[" + self.register_folder), SIZE_BYTES_BLOCK)
        self.disk_data["blocks"][2] = self.verify_size_string(("environmental_variables" + self.register_env), SIZE_BYTES_BLOCK)

    #Metodo para ser chamada antes de fechar o programa
    def save_disk(self):
        try:
            self.scan_struct()
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
                self.disk_data["blocks"][indice_block] = data
            else:
                self.disk_data["blocks"][indice_block] = self.verify_size_string(data, SIZE_BYTES_BLOCK)
        except:
            print("Failed, unable to add block to disk.")
    
    #Metodo que remove os dados contidos no block_list[indice_block]
    def remove_block_on_disk(self, indice_block):
        try:
            self.disk_data["blocks"][indice_block] = self.default_value_block
            self.disk_data["environmental_variables"]["block_list_available"][indice_block] = 1
        except:
            print("Failed to erase block on disk.")

    #Metodo que deleta o arquivo do disco.
    def remove_file_on_disk(self, file_name):
        try:
            
            indice_pointer_file, index_folder = self.discover_file_on_folder(file_name)

            self.disk_data["environmental_variables"]["folder_list_available"][index_folder[0]][1][index_folder[1]] = 1
            self.disk_data["environmental_variables"]["amount_file_available"] += 1
            self.disk_data["environmental_variables"]["file_list_available"][indice_pointer_file] = 1

            for interator in self.disk_data["files"][indice_pointer_file]["block_used"]:
                extract = self.return_correct_context(interator)
                if extract != "":
                    self.disk_data["environmental_variables"]["block_list_available"][int(extract)] = 1
                    self.disk_data["environmental_variables"]["amount_block_available"] += 1
        except:
            print("Failed to remove file.")

    #Descobre onde esta o ponteiro do arquivo, e seu retorno envolve:
        # - [0] = O ponteiro do ARQUIVO, para a estrutura dos files.
        # - [1] = Vetor contendo:
            # - [0] = Indice de qual folder estamos, na estrutura dos folders.
            # - [1] = Indice de qual subfolder estamos, na esturura interna do folder. 
    def discover_file_on_folder(self, file_name):
        discover = file_name.split(".")
        new_name_file = self.verify_size_string(discover[0], MAX_SIZE_FILE_NAME)

        extract = self.disk_data["folders"][self.current_folder_indice][1]
        current_inside_index = None
        data = None
        for interator in range(len(extract)):
            if extract[interator][0] == new_name_file:
                data = extract[interator]
                current_inside_index = interator
                break
        
        self.show_message_if_none("File don't exist in this folder", data)
        return(int(data[2]),[self.current_folder_indice, current_inside_index])
                
    #Metodo que reconstroi o arquivo apatir dos bytes salvos nos blocos.
    def recover_file_on_disk(self, file_name):
        try:
            recover_indice_blocks = []
            recover_data = ""
            indice, _ = self.discover_file_on_folder(file_name)
            extract_file = self.disk_data["files"][indice]

            for block in extract_file["block_used"]:
                extract = self.return_correct_context(block)
                if extract != "":
                    recover_indice_blocks.append(int(extract))

            for interator in recover_indice_blocks:
                recover_data += self.return_correct_context(self.disk_data["blocks"][interator])

            #Verifica o padding do arquivo.
            missing_padding = len(recover_data) % 4
            if missing_padding:
                recover_data += '='* (4 - missing_padding)
            decode_b64 = base64.b64decode(recover_data)
            file = open(file_name, 'wb')
            file.write(decode_b64)
            file.close()
        except:
            print("File recovery failed.")

    #Metodo que muda para o diretorio selecionado se existir.
    def change_current_folder(self, folder_name):
        #try:
            if folder_name == "..":
                #new_folder = ""
                #extract = self.current_folder.split("/")

                #for interator in range(len(extract) - 1):
                #    new_folder += extract[interator]

                #self.current_folder = self.disk_data["folders"][0][0]
                #self.current_folder_indice = 0
                return

            elif folder_name == ".":
                self.current_folder = self.disk_data["folders"][0][0]
                self.current_folder_indice = 0
                return

            else:
                for interator in range(len(self.disk_data["folders"])):
                    if self.disk_data["folders"][interator][0] == self.verify_size_string(self.return_correct_context(self.current_folder) + folder_name, MAX_SIZE_FOLDER_NAME):
                        self.current_folder = self.disk_data["folders"][interator][0]
                        self.current_folder_indice = interator
                        return

                return None

        #except:
         #   print("Failure, invalid directory.")

     #Descobre onde esta o ponteiro do folder, e retorna ele.
    def discover_folder_on_folder(self, folder_name):
        if self.current_folder_indice != 0:
            discover = self.return_correct_context(self.current_folder) + DEFAULT_CARACTER_FOLDER_ROOT + folder_name
        else:
            discover = self.return_correct_context(self.current_folder) + folder_name
        correct_name = self.verify_size_string(discover, MAX_SIZE_FOLDER_NAME)

        for folder in self.disk_data["folders"][self.current_folder_indice][1]:
            if folder[0] == correct_name:
                return int(self.return_correct_context(folder[2])), correct_name
        return None

    #Metodo para remover um folder.
    def remove_folder_on_disk(self, name_folder):
        indice, correct_name = self.discover_folder_on_folder(name_folder)
        self.show_message_if_none("File not exist.", indice)

        for interator in self.disk_data["environmental_variables"]["folder_list_available"][indice][1]:
            if interator == 0:
                self.show_message_if_none("Impossible remove folder, has files/folders inside.", None)
                break

        extract = self.disk_data["folders"][self.current_folder_indice][1]
        save_indice_removed = None

        for interator in range(len(extract)):
            if extract[interator][0] == correct_name:
                save_indice_removed = interator
            
        self.show_message_if_none("Faliure, indice not  found.", save_indice_removed)

        #Modifica as variaveis de ambiente.
        self.disk_data["environmental_variables"]["folder_list_available"][self.current_folder_indice][1][save_indice_removed] = 1
        self.disk_data["environmental_variables"]["folder_list_available"][indice][0] = 1
        self.disk_data["environmental_variables"]["amount_folder_available"] += 1

    #Metodo que adiciona novo diretorio no disko/atualizar algum já existente.
    def add_folder_on_disk(self, name_folder):
        try:
            if self.disk_data["environmental_variables"]["amount_folder_available"] <= 0:
                print("Don't have space to create more folders.")
                return
            
            slot_inside_folder_available = None
            slot_folder_available = None

            tmp_struct_folder_inside = self.disk_data["environmental_variables"]["folder_list_available"][self.current_folder_indice][1]
            tmp_struct_folder = self.disk_data["environmental_variables"]["folder_list_available"]

            for interator in range(len(tmp_struct_folder_inside)):
                if tmp_struct_folder_inside[interator]:
                    slot_inside_folder_available = interator
                    break
            
            for interator in range(len(tmp_struct_folder)):
                if tmp_struct_folder[interator][0]:
                    slot_folder_available = interator
                    break
            
            if slot_inside_folder_available != None and slot_folder_available != None:

                if self.return_correct_context(self.current_folder) != DEFAULT_CARACTER_FOLDER_ROOT:
                    new_name_folder = self.return_correct_context(self.current_folder) + DEFAULT_CARACTER_FOLDER_ROOT + name_folder
                else:
                    new_name_folder = self.return_correct_context(self.current_folder) + name_folder

                new_name_folder = self.verify_size_string(new_name_folder, MAX_SIZE_FOLDER_NAME)
                self.show_message_if_none("Name folder, extrapoled", new_name_folder)

                #Colocando as informações dentro do bloco do atual folder.
                self.disk_data["folders"][self.current_folder_indice][1][slot_inside_folder_available][0] = new_name_folder
                self.disk_data["folders"][self.current_folder_indice][1][slot_inside_folder_available][1] = DEFAULT_CARACTER_FOLDER
                self.disk_data["folders"][self.current_folder_indice][1][slot_inside_folder_available][2] = self.verify_size_string(str(slot_folder_available),SIZE_POINTER_FOLDER)

                #Criando o novo folder na estrutura.
                self.disk_data["folders"][slot_folder_available][0] = new_name_folder

                #Preenchendo a estrutura do folder no enviromental.
                self.disk_data["environmental_variables"]["folder_list_available"][self.current_folder_indice][1][slot_inside_folder_available] = 0
                self.disk_data["environmental_variables"]["folder_list_available"][slot_folder_available][0] = 0
                self.disk_data["environmental_variables"]["amount_folder_available"] -= 1

            else:
                print("Don't have space to create more folders inside/global.")
                return

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
            extract_soft_info_file[1] = self.verify_size_string(extract_hard_info_file[1], MAX_SIZE_EXTENSION_FILE)

            #Verifica se os metadados não sao extrapolados e se existe espaco no inode(files)
            self.show_message_if_none("File name, extrapolated size.", extract_soft_info_file[0])
            self.show_message_if_none("File extension extrapolated size.", extract_soft_info_file[1])
            if self.disk_data["environmental_variables"]["amount_file_available"] <= 0:
                print("Don't have more space in file.")
                return

            #Verifica se existe espaco interno no current folder.
            dest_folder = self.disk_data["environmental_variables"]["folder_list_available"][self.current_folder_indice]
            amount_slot_available = 0
            for interator in range(len(dest_folder[1])):
                if dest_folder[1][interator]:
                    amount_slot_available += 1
            if amount_slot_available <= 0:
                print("Don't have more space in current folder.")
                return

            with open(file_name, "rb") as file:
                file_bytes = file.read()

            b64 = base64.b64encode(file_bytes)
            
            size_64_encode = len(b64)
            amount_block = math.ceil(size_64_encode / SIZE_BYTES_BLOCK)
            has_available_slot = self.verify_has_block_available(amount_block)
            self.show_message_if_none("Don't have space to insert file.", has_available_slot)

            if size_64_encode - SIZE_BYTES_BLOCK >= 0:
                chunk = SIZE_BYTES_BLOCK
            else:
                chunk = size_64_encode

            #Coloca os dados do arquivo no disco logico.
            for indice in range(len(self.disk_data["environmental_variables"]["block_list_available"])):
                if amount_block <= 0: break
                if self.disk_data["environmental_variables"]["block_list_available"][indice]:
                    self.disk_data["environmental_variables"]["block_list_available"][indice] = 0
                    self.disk_data["environmental_variables"]["amount_block_available"] -= 1
                    self.add_block_on_disk(indice, b64[start_chunk : chunk])
                    list_block_used.append(self.verify_size_string(str(indice), MAX_ADDRESSES_IN_BLOCK))

                    if chunk + SIZE_BYTES_BLOCK <= size_64_encode:
                        start_chunk = chunk
                        chunk += SIZE_BYTES_BLOCK
                    else:
                        start_chunk = chunk
                        chunk = size_64_encode
            
                    amount_block -= 1

            indice_save_file = 0

            #Preencher o Node, dentro da estrutura dos files.
            for interator in range(len(self.disk_data["environmental_variables"]["file_list_available"])):
                if self.disk_data["environmental_variables"]["file_list_available"][interator]:
                    self.disk_data["files"][interator].update({"file_name" : extract_soft_info_file[0]}),
                    self.disk_data["files"][interator].update({"extension_file" : extract_soft_info_file[1]}),
                    self.disk_data["files"][interator].update({"bytes_used" : self.verify_size_string(str(size_64_encode), MAX_SIZE_METADATA_FILE)}),
                    self.disk_data["files"][interator]["block_used"] = self.set_block_used(list_block_used)
                    self.disk_data["environmental_variables"]["file_list_available"][interator] = 0
                    self.disk_data["environmental_variables"]["amount_file_available"] -= 1
                    indice_save_file = interator
                    break

            #Preencher o Node, dentro da estrutura do folder.
            for interator in range(len(dest_folder[1])):
                if dest_folder[1][interator]:
                    dest_folder[1][interator] = 0
                    self.disk_data["folders"][self.current_folder_indice][1][interator][0] = extract_soft_info_file[0]
                    self.disk_data["folders"][self.current_folder_indice][1][interator][1] = DEFAULT_CARACTER_FILE
                    self.disk_data["folders"][self.current_folder_indice][1][interator][2] = indice_save_file
                    break

            self.persist_data()

        except:
            print("Failed to add file to disk.")
