from scene import Mesh

class Loader(object):

    def __init__(self):
        pass

    def load_model(self, model_name):
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
                        model_mesh.vertex_array[iter_v][0] = float(line[1])     # X
                        model_mesh.vertex_array[iter_v][1] = float(line[2])     # Y
                        model_mesh.vertex_array[iter_v][2] = float(line[3])     # Z
                        iter_v += 1
                    elif line[0] == 'f':
                        model_mesh.index_array.append( int(line[1]))
                        model_mesh.index_array.append( int(line[2]))
                        model_mesh.index_array.append( int(line[3]))
                    elif line[1] == "#end":
                        print( "Model ", model_name, "was loaded" )
                        return model_mesh
        except IOError:
            print("Error: could not open model " + model_name)
            return -2
        print("Something go wrong ", model_name)
        return -3
