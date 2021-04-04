class Writer:
    def __init__(self, is_console: bool, is_file: bool = False, filename: str = None):
        self.__is_console = is_console
        self.__is_file = is_file
        self.__filename = filename
        self.__is_first = True
        self.__server_id_mapper_dict = {}

    def set_mapped_server_id(self, server_id: str) -> int:
        if server_id in self.__server_id_mapper_dict.keys():
            raise ValueError(f"The Server[{server_id}] already exists.")
        mapped_server_id = len(self.__server_id_mapper_dict)
        self.__server_id_mapper_dict[server_id] = mapped_server_id
        return mapped_server_id

    def get_mapped_server_id(self, server_id: str) -> int:
        return self.__server_id_mapper_dict[server_id]

    def write(self, content: str):
        content = content if content.endswith('\n') else content + '\n'

        if self.__is_console:
            print(content, end='')

        if self.__is_file:
            if self.__is_first:
                self.__is_first = False
                with open(self.__filename, 'w') as file:
                    file.write(content)
            else:
                with open(self.__filename, 'a') as file:
                    file.write(content)
