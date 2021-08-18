import json, base64, os, math

SIZE_DISC = 250 #Tamanho total do disco em KB/s
SIZE_BLOCK = 4 #Tamanho dos blocos em KB/s

#Class responsavel por manipular as informações do disco que vao ser salva no .dsc
class cDISC_MANAGER:
    #Construtor do disco.
    def __init__(self):
        self.file_name = "disc.dsc"
        self.current_folder = "/"

        try:
            print("Looking for disk.")
            self.file_pointer = open(self.file_name)
            self.disc_data = json.load(self.file_pointer)
        except:
            print("Disk not found.")
            struct_to_disc = {
                "blocks": {
                    "block_list" : []
                },
                "files" : {
                    "file_list": []
                },
                "folders": {
                    "/": {}
                },
                "environmental_variables": {
                    "block_list_avaliable": [],
                    "size_block_list": 0,
                    "size_block": SIZE_BLOCK,
                    "indice_file" : 0,
                }
            }
            while(struct_to_disc["environmental_variables"]["size_block_list"] < SIZE_DISC / SIZE_BLOCK):
                struct_to_disc["environmental_variables"]["block_list_avaliable"].append(True)
                struct_to_disc["blocks"]["block_list"].append(None)
                struct_to_disc["environmental_variables"]["size_block_list"] += 1

            with open("disc.dsc", "w") as file_write:
                json.dump(struct_to_disc, file_write)

            print("Successfully created disc.")
            self.file_pointer = open(self.file_name)
            self.disc_data = json.load(self.file_pointer)
        finally:
            print("Disc opened with successfully.")

#Persiste os dados no disco.
    def persist_data(self):
        with open("disc.dsc", "w") as file_write:
            json.dump(self.disc_data, file_write)

    #Função para ser chamada antes de fechar o programa
    def save_disc(self):
        self.file_pointer.close()
        self.persist_data()

    #Mostra a estrutura do disco.
    def view_disc_data(self):
        print(json.dumps(self.disc_data, indent = 4))

    #Adiciona novo bloco utilizazdo no disco/atualizar algum já existente.
    def add_in_block_on_disc(self, name_block, name_file, chunk):
        self.disc_data["blocks"]["block_list"][name_block] = ({ str(name_block): (chunk).decode("utf8")})

    def recover_file_on_disc(self, list_block_used):
        recover = ""
        for block in list_block_used:
            recover += self.disc_data["blocks"]["block_list"][block][str(block)]

        #recover = self.disc_data["blocks"]["block_list"][0][str(0)]
        decode_b64 = base64.b64decode(recover)
        pdf = open('out.txt', 'wb')
        pdf.write(decode_b64)
        pdf.close()
        print("recover: ", len(recover))

    #Muda para o diretorio selecionado se existir.
    def change_current_folder(self, name_folder):
        if name_folder in self.disc_data["folders"]:
            self.current_folder = name_folder
        else:
            print("Whoops, invalid directory")

    #Adiciona novo diretorio no disco/atualizar algum já existente.
    def add_in_folder_on_disc(self, name_folder, content_folder):
        self.disc_data["folders"].update({name_folder : content_folder})
        self.persist_data()

    #Adiciona novo arquivo no disco/atualizar algum já existente.
    def add_in_file_on_disc(self, name_file):
        list_block_used = []

        #Abre arquivo name_file e pega todos os Bytes
        with open(name_file, "rb") as f:
                byte = f.read()

        b64 = base64.b64encode(byte)
        size_bytes = os.path.getsize(name_file)


        amount_block = math.ceil( ( (size_bytes) / 1000 )  / SIZE_BLOCK )
        chunk = math.ceil((len(b64) / amount_block ))
        print("size: {}\n caracteres: {} \namount_block: {} \nchunk: {} ".format(size_bytes,len(b64), amount_block, chunk ))
        #print( b64[0:5321])
        start = 0
        for indice in range(len(self.disc_data["environmental_variables"]["block_list_avaliable"])):
            if amount_block <= 0: break
            if self.disc_data["environmental_variables"]["block_list_avaliable"][indice]:
                self.disc_data["environmental_variables"]["block_list_avaliable"][indice] = False
                self.add_in_block_on_disc(indice, name_file, b64[ start: start + chunk])
                list_block_used.append(indice)

                if ( (start + chunk) > len(b64)):
                    chunk = len(b64)
                else:
                    start += chunk
                amount_block -= 1

        self.disc_data["files"]["file_list"].append(
            {
                "name_file" : name_file,
                "bytes_used" : size_bytes,
                "block_used" : list_block_used
            }
        )

        self.disc_data["folders"][self.current_folder].update({name_file : amount_block})
        self.persist_data()



