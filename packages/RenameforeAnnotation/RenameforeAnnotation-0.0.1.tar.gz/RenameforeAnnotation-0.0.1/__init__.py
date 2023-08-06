import os
class Rename_Fore_Anotate:
    def rename(self, path, starting_point):
        i = starting_point
        for filename in os.listdir(path):
            os.rename(os.path.join(path, filename),
                      os.path.join(path, 'image'+str(i)+'.jpg'))
            i = i+1
