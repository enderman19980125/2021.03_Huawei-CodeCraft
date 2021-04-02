class Reader:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__lines = []

        if filename == 'console':
            self.get_next_line = self.get_next_line_from_console()
        else:
            with open(filename, 'r') as file:
                self.__lines = file.readlines()
            self.get_next_line = self.get_next_line_from_file()

    @staticmethod
    def get_next_line_from_console() -> str:
        while True:
            line = input()
            yield line

    def get_next_line_from_file(self) -> str:
        for line in self.__lines:
            line = line.strip('\n')
            yield line
