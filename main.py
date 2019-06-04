from scipy import misc

IMAGE = 'samples/cat.png'

T = [150, 150, 150]
S = [255, 255, 255]

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
    A = set()
    B = {(i, j) for i in range(dim_x) for j in range(dim_y)}
    
    for i in range(dim_x):
        for j in range(dim_y):
            if ((i, j) in B):
                delta = (dist(T, image[i][j]) - dist(S, image[i][j])) * alpha
            nbrs = get_neighbours(i, j, dim_x, dim_y)
            for k in range(len(nbrs)):
                if (nbrs[k] in A):
                    delta += dist(image[i][j], image[nbrs[k][0]][nbrs[k][1]]) * beta
                else:
                    delta -= dist(image[i][j], image[nbrs[k][0]][nbrs[k][1]]) * beta
            if (delta < 0):
                flip(i, j, A, B)
    
    return A, B

def cut_png(image):
    dim_x, dim_y, colors = image.shape
    A = set()
    B = {(i, j) for i in range(dim_x) for j in range(dim_y)}
    
    for i in range(dim_x):
        for j in range(dim_y):
            if ((i, j) in B):
                delta = (dist(T, image[i][j][:3]) - dist(S, image[i][j][:3])) * alpha
            nbrs = get_neighbours(i, j, dim_x, dim_y)
            for k in range(len(nbrs)):
                if (nbrs[k] in A):
                    delta += dist(image[i][j][:3], image[nbrs[k][0]][nbrs[k][1]][:3]) * beta
                else:
                    delta -= dist(image[i][j][:3], image[nbrs[k][0]][nbrs[k][1]][:3]) * beta
            if (delta < 0):
                flip(i, j, A, B)
    
    return A, B



def main():
    image = misc.imread(IMAGE)
    dim_x, dim_y, colors = image.shape
    print("Loaded image of shape {x}, {y}".format(x=dim_x, y=dim_y))

    A, B = cut_png(image)

    for i in range(dim_x):
        for j in range(dim_y):
            if (i, j) in A:
                image[i, j, 0] = T[0]
                image[i, j, 1] = T[1]
                image[i, j, 2] = T[2]
            elif (i,j) in B:
                image[i, j, 0] = S[0]
                image[i, j, 1] = S[1]
                image[i, j, 2] = S[2]

    misc.imsave('out.png', image)

if __name__ == '__main__':
    main()
