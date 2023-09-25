from scene import Vector3f
class Loader(object):

    def __init__(self):
        pass

    def load_model(self, model_name, model_pos:Vector3f = Vector3f(0, 10, 0)):
        from scene import Mesh

        scale = 0.05
        obj_center_vec = model_pos
        #position = Vector3f(0, 0, 0)
        try:
            with open(model_name, 'r') as file:
                lines = file.readlines()        # Read all data
                file.close()
                # if lines[0][0] != '#':
                #     print("Error obj format is invalid")
                #     return -1
                model_mesh = Mesh()
                model_mesh.mesh_position = obj_center_vec
                txtr__coord_array = []
                iter_v = 0
                for line in lines:
                    if line[0] == '\n':
                        continue
                    line = line.replace('\t', '')
                    line = line.replace('\n', '')
                    line = line.split(' ')
                    if line[0] == 'v':
                        obj_vec = Vector3f(  (obj_center_vec.x - float(line[1])) * scale,
                                            (obj_center_vec.y + float(line[2])) * scale,
                                            (obj_center_vec.z - float(line[3])) * scale)
                        model_mesh.vertex_array[iter_v][0] = obj_center_vec.x + obj_vec.x     # X
                        model_mesh.vertex_array[iter_v][1] = obj_center_vec.y + obj_vec.y     # Y
                        model_mesh.vertex_array[iter_v][2] = obj_center_vec.z + obj_vec.z     # Z
                        iter_v += 1
                    elif line[0] == 'vt':
                        line.pop(0)
                        txtr__coord_array.append(line)
                    elif line[0] == 'f':
                        for element in line[1::]:
                            element = element.split('/')
                            element = list(map(int, element))           # Conver str list to int list
                            model_mesh.index_array.append(int(element[0]) - 1)
                            model_mesh.vertex_array[element[0] - 1][6] = txtr__coord_array[element[1] - 1][0]
                            model_mesh.vertex_array[element[0] - 1][7] = txtr__coord_array[element[1] - 1][1]
                    elif line[0] == 'vn':
                        pass
                    elif line[1] == "#end":
                        print( "Model ", model_name, "was loaded" )
                    else:
                        print("Unknown start symbol ", line[0], "in", model_name)
                model_mesh.texture_name = "models/LeavesTransparent.png"
                return model_mesh
        except IOError:
            print("Error: could not open model " + model_name)
            return -2
        print("Something go wrong ", model_name)
        return -3
