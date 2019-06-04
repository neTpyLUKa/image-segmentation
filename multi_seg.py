from scipy import misc

IMAGE = 'landscape.jpg'

color = list()
color.append([242, 242, 242]) # 0
color.append([173, 180, 199]) # 1
color.append([58, 97, 138]) # 2
color.append([59, 72, 89]) # 3
color.append([4, 21, 39]) # 4
color.append([166, 139, 94]) # 5

n_segments = 6

alpha = 1
beta = 1

def dist(x, y):
    return sum((x - y) ** 2)

def get_neighbours(i, j, max_i, max_j):
    result = []
    if i > 0:
        result.append((i - 1, j))
    if j > 0:
        result.append((i, j - 1))
    if (i + 1) < max_i:
        result.append((i + 1, j))
    if (j + 1) < max_j:
        result.append((i, j  + 1))

    return result

def flip(i, j, A, B):
    if (i, j) in A:
        A.remove((i, j))
        B.add((i, j))
    else:
        B.remove((i, j))
        A.add((i, j))

def cut(image):
    dim_x, dim_y, colors = image.shape
    segments = [[]] * n_segments
    which_segment = [[0 for j in range (dim_y)] for i in range(dim_x)]
    for k in range(n_segments):
        for i in range(dim_x * k // n_segments, dim_x * (k + 1) // n_segments):
            for j in range(dim_y):
                segments[k].append((i, j))
                which_segment[i][j] = k
    for p in range(3):
        for i in range(dim_x):
            for j in range(dim_y):
                cur_seg = which_segment[i][j]
                for k in range(n_segments):
                    if (cur_seg != k):
                        delta = (dist(color[k], image[i][j]) - dist(color[cur_seg], image[i][j])) * alpha
                        nbrs = get_neighbours(i, j, dim_x, dim_y)
                        for t in range(len(nbrs)):
                            if (which_segment[nbrs[t][0]][nbrs[t][1]] == cur_seg):
                                delta += dist(image[i][j], image[nbrs[t][0]][nbrs[t][1]]) * beta
                            elif (which_segment[nbrs[t][0]][nbrs[t][1]] == k):
                                delta -= dist(image[i][j], image[nbrs[t][0]][nbrs[t][1]]) * beta
                        if (delta < 0):
                            which_segment[i][j] = k
                            # flip(i, j, segments[k], segments[cur_seg])
        
    for i in range(dim_x):
        for j in range(dim_y):
                image[i, j, 0] = color[which_segment[i][j]][0]
                image[i, j, 1] = color[which_segment[i][j]][1]
                image[i, j, 2] = color[which_segment[i][j]][2]
    misc.imsave('out.png', image)


    return 0



def main():
    image = misc.imread(IMAGE)
    dim_x, dim_y, colors = image.shape
    print("Loaded image of shape {x}, {y}".format(x=dim_x, y=dim_y))

    cut(image)

   # for i in range(dim_x):
    #    for j in range(dim_y):
     #       for k in range(n_segments):
      #          if (i, j) in segments[k]:
       #             image[i, j, 0] = color[k][0]
        #            image[i, j, 1] = color[k][1]
         #           image[i, j, 2] = color[k][2]
    # misc.imsave('out.png', image)

if __name__ == '__main__':
    main()
