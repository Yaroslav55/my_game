from scene import Mesh

class Loader(object):

    def __init__(self):
        pass

    def load_model(self, model_name):
        scale = 1
        try:
            with open(model_name, 'r') as file:
                lines = file.readlines()        # Read all data
                file.close()
                if lines[0][0] != '#':
                    print("Error obj format is invalid")
                    return -1
                model_mesh = Mesh()
                iter_v = 0
                for line in lines:
                    if line[0] == '\n':
                        continue
                    line = line.replace('\t', '')
                    line = line.replace('\n', '')
                    line = line.split(' ')
                    if line[0] == 'v':
                        model_mesh.vertex_array[iter_v][0] = float(line[1]) * scale    # X
                        model_mesh.vertex_array[iter_v][1] = float(line[2]) * scale     # Y
                        model_mesh.vertex_array[iter_v][2] = float(line[3]) * scale     # Z
                        iter_v += 1
                    elif line[0] == 'f':
                        line[1] = line[1].split('/')
                        line[2] = line[2].split('/')
                        line[3] = line[3].split('/')
                        model_mesh.index_array.append( int(line[1][0]) -1)
                        model_mesh.index_array.append( int(line[2][0]) -1)
                        model_mesh.index_array.append( int(line[3][0]) -1)
                        # #       Tex coord
                        # model_mesh.index_array.append( int(line[1][1]) )
                        # model_mesh.index_array.append( int(line[2][1]) )
                        # model_mesh.index_array.append( int(line[3][1]) )

                    elif line[1] == "#end":
                        print( "Model ", model_name, "was loaded" )
                return model_mesh
        except IOError:
            print("Error: could not open model " + model_name)
            return -2
        print("Something go wrong ", model_name)
        return -3
