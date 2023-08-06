import os


class Visualizer:

    folder = u'\U0001F4C1'  # '📁'
    file = u'\U0001F4C3'  # '📃'

    def __init__(self, directory: str):
        """
        Initialize start visualizer to work with it\n
        :param directory: path to start visualizer
        """
        self.directory = os.path.abspath(directory)

    def _get_content(self) -> list:
        """
        Gets list of content of directory\n
        :return:
        """
        content = os.listdir(self.directory)
        content = self._sort(content)
        return content

    def _sort(self, content: list) -> list:
        """
        Sorts list with content of visualizer: first - folders, second - files\n
        :param content: list with content of visualizer
        :return: sorted list of directory content
        """
        for _ in range(len(content)):
            for j in range(len(content) - 1):
                if os.path.isfile(os.path.join(self.directory, content[j])) and \
                        os.path.isdir(os.path.join(self.directory, content[j + 1])):
                    content[j], content[j + 1] = content[j + 1], content[j]
        return content

    def dir(self) -> list:
        """
        Visualizes directory`s content in console\n
        :return: list of directory
        """
        directory = []
        print(self.folder, os.path.basename(self.directory))
        directory.append(os.path.basename(self.directory))
        content = self._get_content()
        for object in content:
            object = os.path.join(self.directory, object)
            if os.path.isdir(object):
                print('|_', self.folder, os.path.basename(object))
                directory.append('|_' + ' ' + self.folder + ' ' + os.path.basename(object))
            elif os.path.isfile(object):
                print('|_', self.file, os.path.basename(object))
                directory.append('|_' + ' ' + self.file + ' ' + os.path.basename(object))
        return directory

    def cd(self, to: str):
        """
        Changes visualizer\n
        :param to: path to folder
        """
        print('\n')
        content = self._get_content()
        if to == '..':
            self.directory = os.path.abspath(os.path.dirname(self.directory))
        elif to in content:
            self.directory = os.path.join(self.directory, to)
        elif os.path.exists(to):
            self.directory = os.path.abspath(to)
        elif not (os.path.exists(to)):
            raise FileExistsError
