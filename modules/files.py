class Files(object):
    def __init__(self):
        return

    @staticmethod
    def save_output(filename, content):
        try:
            with open('./' + filename, 'w') as out_file:
                out_file.write('\n'.join(content) + '\n')
            out_file.close()
        except IOError as err:
            print('Error writing file')