import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sps
import networkx as nx

def load_maze(file_name: str) -> np.ndarray:
    """
    Funkce příjme jako argument název soubor, kde je uloženo čtvercové bludiště a vráti boolean matici reprezentující toto bludiště

    Args:
        file_name (str): název souboru k načtení

    Returns:
        np.ndarray: bool matice reprezentující bludiště
    """

    # Načtení bludiště ze souboru
    maze = np.loadtxt("/home/student/Plocha/PYT/Bludiště/Python3_Projekt/Bludiště_zadaní/data/"+file_name, delimiter=',')

    # ověření že je bludiště čtvrecové
    m, n = np.shape(maze)
    if(m != n):
        print("Bludiště není čtvercové!")
        return

    # Převedení na boolovskou matici
    maze = maze.astype(bool)

    return maze

def create_incidence_csr(maze: np.ndarray) -> sps.csr_matrix:
    """
    Funkce příjme jako argument bludišttě a vytvoří matici incidence reprezentující toto bludiště

    Args:
        maze (np.ndarray): boolean matice s bludištěm

    Returns:
        sp.sparse.csr_matrix: matice incidence
    """

    # vytvoření matice sousednosti
    row, col = np.shape(maze)

    # Vnitřní horizontální hrany
    horizontal_up_idx = np.arange(0, (col*(row-1)), 1)
    horizontal_low_idx = np.arange(col, (row * col), 1)
    row_horizontal = np.hstack((horizontal_up_idx, horizontal_low_idx))
    col_horizontal = np.hstack((horizontal_low_idx, horizontal_up_idx))
    data_horizontal = np.ones(2 * (row * col - col))

    # Vnitřní vertikální hrany
    index_matrix_vertical = np.arange(row * col).reshape((row, col)).T.flatten() # indexy buněk přeházené pro vertikální hranu
    vertical_left_idx = index_matrix_vertical[:-row]
    vertical_right_idx = index_matrix_vertical[row:]
    row_vertical = np.hstack((vertical_left_idx, vertical_right_idx))
    col_vertical = np.hstack((vertical_right_idx, vertical_left_idx))
    data_vertical = np.ones(2 * (row * col - row))

    # spojíme všechny vnitřní hrany a diagonálu
    row_m = np.hstack((row_horizontal, row_vertical))
    col_m = np.hstack((col_horizontal, col_vertical))
    data = np.hstack((data_horizontal, data_vertical))

    # vyrobíme matici
    A = sps.csr_matrix((data, (row_m, col_m)), shape=(row*col, row*col))

    # vynulování neprůchozích buněk
    maze_cells = maze.copy().reshape(-1)
    A[maze_cells==1, :] = 0
    A[:, maze_cells==1] = 0
    #A.setdiag(1)
    
    return A

def create_incidence(maze: np.ndarray) -> sps.lil_matrix:
    """
    Funkce příjme jako argument bludišttě a vytvoří matici incidence reprezentující toto bludiště

    Args:
        maze (np.ndarray): boolean matice s bludištěm

    Returns:
        sp.sparse.lil_matrix: matice incidence
    """
    m, n = np.shape(maze)
    A = sps.lil_matrix((m*n, m*n))
    for i in range(m):
        for j in range(n):
            index = i * n + j
            if j > 0:
                A[index, index-1] = 1
            if j < m-1:
                A[index, index+1] = 1
            if i > 0:
                A[index, index-m] = 1
            if i < n-1:
                A[index, index+m] = 1

    maze_cells = maze.copy().reshape(-1)
    A[maze_cells==1, :] = 0
    A[:, maze_cells==1] = 0
    #A.setdiag(1)

    return A

def get_shortest_path_coords(maze: np.ndarray, start: int, end: int) -> list:
    """
    Funkce příjme jako argument bludišttě, počáteční a koncový bod bludiště.
    Funkce dále sestaví graf, najde v něm nejkratší cestu (pomocí dijikstrova algoritmu) a vrátí souřadnice této cesty.

    Args:
        maze (np.ndarray): boolean matice s bludištěm
        start (int): počáteční bod bludiště
        end (int): počáteční bod bludiště

    Returns:
        list: list se souřadnicema nejkratší cesty v bludišti
    """

    incidence = create_incidence(maze)
    graph = nx.DiGraph(incidence)
    shortest_path = nx.shortest_path(graph, start, end)
    shortest_path_coords = []
    for node in shortest_path:
        m, n = node % maze.shape[1], node // maze.shape[1]
        shortest_path_coords.append((m, n))

    return shortest_path_coords

def draw_solved_maze(maze: np.ndarray) -> None:
    """
    Funkce příjme jako argument bludišttě a vykreslí jeho řešení

    Args:
        maze (np.ndarray): boolean matice s bludištěm

    Returns:
        None: funkce pouze vykreslí vyřešené bludiště
    """
    shortest_path_coords = get_shortest_path_coords(maze, 0, maze.size - 1)

    # Vykreslení bludiště
    plt.imshow(maze, cmap=plt.cm.binary)

    # Vykreslení nejkratší cesty
    xs, ys = zip(*shortest_path_coords)
    plt.plot(xs, ys, 'r')
    plt.show()

    return

def maze_template(size: int, type: str) -> np.ndarray:
    """
    Funkce vytvoří vybraný template bludiště

    Args:
        size (int): požadovaná velikost bludiště
        type (str): požadováný vzor bludiště (empty, S)

    Returns:
        np.ndarray: template bludiště (bool)
    """
    maze = np.zeros((size, size), dtype=bool)

    # nastavení okrajů bludiště
    maze[2:,0] = True
    maze[0,1:] = True
    maze[:-2,-1] = True
    maze[-1,:-1] = True

    if(type == "empty"):
        return maze
    
    elif(type == "S"):
        maze[size // 3, :-5] = True
        maze[(size // 3) * 2, 5:] = True
        return maze

def fill_maze(maze: np.ndarray, graph: nx.DiGraph) -> tuple[np.ndarray, nx.DiGraph]:
    

    return maze, graph

def generate_maze(size: int, type: str = "empty", iter: int = 100) -> np.ndarray:
    """
    Funkce vytvoří vygeneruje a vrátí nové bludiště

    Args:
        size (int): požadovaná velikost bludiště
        type (str): požadováný vzor bludiště (empty, S)
        iter (int): počet iterací generovacího cyklu

    Returns:
        np.ndarray: template bludiště (bool)
    """

    maze = maze_template(size, type)
    incidence = create_incidence(maze)
    graph = nx.DiGraph(incidence)

    for i in range(iter):
        maze, graph = fill_maze(maze, graph)

    return maze
