class Reader:
    def __init__(self, mode: str, filename: str = None):
        self.__mode = mode
        self.__filename = filename
        self.__lines = []

        if mode == 'console':
            self.get_next_line = self.__get_next_line_from_console()
        elif mode == 'file':
            with open(filename, 'r') as file:
                self.__lines = file.readlines()
            self.get_next_line = self.__get_next_line_from_file()
        else:
            raise KeyError(f'"mode" must be "console" or "file".')

    @staticmethod
    def __get_next_line_from_console() -> str:
        while True:
            line = input().strip('\n').strip(' ')
            yield line

    def __get_next_line_from_file(self) -> str:
        for line in self.__lines:
            line = line.strip('\n').strip(' ')
            yield line
