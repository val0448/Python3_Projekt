import matplotlib.pyplot as plt
import scipy.sparse as sps
from queue import Queue
import numpy as np

def load_maze(file_name: str) -> np.ndarray:
    """
    Funkce příjme jako argument název soubor, kde je uloženo čtvercové bludiště a vráti boolean matici reprezentující toto bludiště

    Args:
        file_name (str): název souboru k načtení

    Returns:
        np.ndarray: bool matice reprezentující bludiště
    """

    # Načtení bludiště ze souboru
    maze = np.loadtxt("Bludiště_zadaní/data/"+file_name, delimiter=',')

    # ověření že je bludiště čtvrecové
    m, n = np.shape(maze)
    if(m != n):
        print("Bludiště není čtvercové!")
        return

    # Převedení na boolovskou matici
    maze = maze.astype(bool)

    return maze

def create_incidence(maze: np.ndarray) -> sps.lil_matrix:
    """
    Funkce příjme jako argument bludišttě a vytvoří matici incidence reprezentující toto bludiště

    Args:
        maze (np.ndarray): boolean matice s bludištěm

    Returns:
        sp.sparse.lil_matrix: matice incidence
    """

    # vytvoříme matici incidence pro všechny buňky průchozí
    m, n = np.shape(maze)
    A = sps.lil_matrix((m*n, m*n), dtype=bool)
    for i in range(m):
        for j in range(n):
            index = i * n + j
            if j > 0:
                A[index, index-1] = True
            if j < m-1:
                A[index, index+1] = True
            if i > 0:
                A[index, index-m] = True
            if i < n-1:
                A[index, index+m] = True

    # převedeme bludiště na 1D pole pro nulování příslušných řádků a sloupců matice
    maze_cells = maze.copy().reshape(-1)
    A[maze_cells, :] = False
    A[:, maze_cells] = False

    return A

def find_shortest_path(incidence: sps.lil_matrix) -> list:
    """
    Funkce příjme jako argument matici incidence a najde nejkratší cestu za použití průchodu do šířky
    Funkce řeší průchodnost bludištěm mezi levýmm horním rohem a pravým dolním rohem

    Args:
        incidence (sps.lil_matrix): matice incidence reprezentující bludiště

    Returns:
        list: funkce vrátí list obsahující nejkratší cestu
    """

    # algoritmus prochledání do šířky
    m, n = np.shape(incidence)
    queue = Queue()
    queue.put(0)
    parent = {0: None} # chceme uložit parent od každého vrcholu
    
    while (not queue.empty()):
        current_vertex = queue.get()
        if (current_vertex == n-1):
            break
        for neighbor in incidence.rows[current_vertex]: # list nenulových prvků odpovídajících aktuálnímu vrcholu
            if (neighbor not in parent):
                parent[neighbor] = current_vertex
                queue.put(neighbor)

    if n-1 not in parent:
        print("Bludiště nemá řešení")
        return [] # cesta nenalezena

    path = [n-1]
    current_vertex = n-1
    while current_vertex != 0:
        current_vertex = parent[current_vertex]
        path.append(current_vertex)

    return np.array(path[::-1]) # obrátíme seznam s path

def has_path(incidence: sps.lil_matrix) -> bool:
    """
    Funkce příjme jako argument matici incidence a vyhodnotí jestli má bludiště cestu či ne
    Funkce řeší průchodnost bludištěm mezi levýmm horním rohem a pravým dolním rohem

    Args:
        incidence (sps.lil_matrix): matice incidence reprezentující bludiště

    Returns:
        bool: True pokud bludiště má cestu, v opačném případě False
    """

    # algoritmus prohledání do šířky
    m, n = np.shape(incidence)
    queue = Queue()
    queue.put(0)
    parent = {0: None} # chceme uložit parent od každého vrcholu
    
    while (not queue.empty()):
        current_vertex = queue.get()
        if (current_vertex == n-1):
            break
        for neighbor in incidence.rows[current_vertex]: # list nenulových prvků odpovídajících aktuálnímu vrcholu
            if (neighbor not in parent):
                parent[neighbor] = current_vertex
                queue.put(neighbor)

    if n-1 not in parent:
        return False
    else:
        return True

def get_shortest_path_coords(maze: np.ndarray) -> list:
    """
    Funkce příjme jako argument bludišttě, najde v něm nejkratší cestu a vrátí souřadnice v bludišti této cesty.
    Funkce řeší průchodnost bludištěm mezi levýmm horním rohem a pravým dolním rohem

    Args:
        maze (np.ndarray): boolean matice s bludištěm
        start (int): počáteční bod bludiště
        end (int): počáteční bod bludiště

    Returns:
        list: list se souřadnicema nejkratší cesty v bludišti
    """

    incidence = create_incidence(maze)
    shortest_path = find_shortest_path(incidence)
    if(shortest_path == []):
        return # cesta nenalzena
    shortest_path_coords = []
    for node in shortest_path:
        m, n = node // maze.shape[1], node % maze.shape[0] # výpočet řádku a sloupce
        shortest_path_coords.append((m, n))

    return shortest_path_coords

def draw_solved_maze(maze: np.ndarray, save: bool = False) -> None:
    """
    Funkce příjme jako argument bludišttě a vykreslí jeho řešení, pokud existuje. Případně bludiště i uloží do souboru dle parametru save.

    Args:
        maze (np.ndarray): boolean matice s bludištěm
        save (bool): V základu False, pokud nastaveno na True, tak vyřešené bludiště uloží i do souboru

    Returns:
        None: funkce pouze vykreslí vyřešené bludiště
    """

    shortest_path_coords = get_shortest_path_coords(maze)
    if(shortest_path_coords == []):
        draw_unsolved_maze(maze, save)
        return

    # Vykreslení bludiště
    plt.imshow(maze, cmap=plt.cm.binary)

    # Vykreslení nejkratší cesty
    ys, xs = zip(*shortest_path_coords)
    plt.plot(xs, ys, 'r')
    if(save):
        plt.savefig("solved_maze")
    plt.show()

    return

def draw_unsolved_maze(maze: np.ndarray, save: bool = False) -> None:
    """
    Funkce příjme jako argument bludišttě a vykreslí ho, případně ho i uloží do souboru dle parametru save.

    Args:
        maze (np.ndarray): boolean matice s bludištěm
        save (bool): V základu False, pokud nastaveno na True, tak bludiště uloží i do souboru

    Returns:
        None: funkce pouze vykreslí bludiště
    """

    # Vykreslení bludiště
    plt.imshow(maze, cmap=plt.cm.binary)
    if(save):
        plt.savefig("unsolved_maze")
    plt.show()

    return

def maze_template(size: int, type: str = "empty") -> np.ndarray:
    """
    Funkce vytvoří vybraný template bludiště se zvolenou velikostí. Vrátí prázdné bludiště při nezvolení typu či zvolení neplatného typu.

    Args:
        size (int): požadovaná velikost bludiště
        type (str): požadováný vzor bludiště (empty, S, N, Z, middle, spiral)

    Returns:
        np.ndarray: template bludiště (bool)
    """

    maze = np.zeros((size, size), dtype=bool)

    # nastavení okrajů bludiště
    maze[2:,0] = True
    maze[0,1:] = True
    maze[:-2,-1] = True
    maze[-1,:-1] = True

    # prázdné bludiště
    if(type == "empty"):
        return maze
    
    # bludiště typu slalom ve tvaru obráceného S
    elif(type == "S"):
        if(size < 7):   # vrátíme prazné bludiště pokud pokud typ bludiště neemá smysl pro danou velikost
            return maze
        maze[size // 3, :-3] = True
        maze[(size // 3) * 2, 3:] = True
        return maze
    
    # bludiště typu slalom ve tvaru obráceného N
    elif(type == "N"):
        if(size < 7):   # vrátíme prazné bludiště pokud pokud typ bludiště neemá smysl pro danou velikost
            return maze
        maze[:-3, size // 3] = True
        maze[3:, (size // 3) * 2] = True
        return maze
    
    # bludiště s průchodem ve tvaru Z
    elif(type == "Z"):
        if(size < 10):   # vrátíme prazné bludiště pokud pokud typ bludiště neemá smysl pro danou velikost
            return maze
        maze[size // 4, :-3] = True
        maze[(size // 4) * 3, 3:] = True
        maze[size // 2, :] = True
        maze[size // 2, (size // 2) - 2 :(size // 2) + 2] = False
        return maze
    
    # bludiště s průchodem uprostřed
    elif(type == "middle"):
        if(size < 7):   # vrátíme prazné bludiště pokud pokud typ bludiště neemá smysl pro danou velikost
            return maze
        maze[size // 2, :] = True
        maze[size // 2, (size // 2) - 2 :(size // 2) + 2] = False
        return maze
    
    # bludiště ve tvaru spirály
    elif(type == "spiral"):
        if(size < 16):  # vrátíme prazné bludiště pokud pokud typ bludiště neemá smysl pro danou velikost
            return maze
        maze[:(size // 4)*3, size // 4] = True
        maze[(size // 4):, (size // 4) * 3] = True
        maze[size // 4, (size // 4) * 2:(size // 4)*3] = True
        maze[(size // 4) * 3, (size // 4):(size // 4) * 2] = True
        return maze
    
    # vrátíme prazné bludiště pokud uživatel zadá špatný typ
    else:
        return maze


def fill_maze(maze: np.ndarray, incidence: sps.lil_matrix) -> tuple[np.ndarray, sps.lil_matrix]:
    """
    Funkce zaplní bludiště na náhodných místech a zajistí, že je stále průchozí

    Args:
        maze (np.ndarray): bludiště
        incidence (sps.lil_matrix): matice incidence daného bludiště

    Returns:
        np.ndarray: zaplněné bludiště (bool)
        incidence (sps.lil_matrix): matice incidence zaplněného bludiště
    """

    m, n = np.shape(maze)
    filled = False
    fill_attempts = 0

    while((not filled) and (fill_attempts < 10)):
        # vybereme náhoný vrchol k zaplnění
        i = np.random.randint(m)
        j = np.random.randint(n)

        free_attempts = 0
        while((maze[i,j]) and (free_attempts < 100)):    # generujeme znovu pokud je pole již zaplněné
            free_attempts += 1 
            i = np.random.randint(m)    
            j = np.random.randint(n)

        if (free_attempts >= 100):
            break

        index = (i * n) + j # odpovídající řádek a sloupec incidenční matice
        row = incidence[index, :]
        col = incidence[:, index]
        incidence[index, :] = False
        incidence[:, index] = False
        if(not has_path(incidence)): # vyhodnotíme jestli bludiště má cestu
            fill_attempts += 1
            incidence[index, :] = row   # vrátíme matici incidence na původní hodnoty
            incidence[:, index] = col
            continue
            
        maze[i, j] = True
        filled = True

    return maze, incidence

def generate_maze(size: int, type: str = "empty", iter: int = 100) -> np.ndarray:
    """
    Funkce vytvoří vygeneruje a vrátí nové bludiště

    Args:
        size (int): požadovaná velikost bludiště
        type (str): požadováný vzor bludiště (empty, S, middle, N)
        iter (int): počet iterací generovacího cyklu

    Returns:
        np.ndarray: template bludiště (bool)
    """

    maze = maze_template(size, type)
    incidence = create_incidence(maze)

    # snažíme se bludiště zaplnit v každé iteraci
    for i in range(iter):
        maze, incidence = fill_maze(maze, incidence)

    return maze

def save_maze(maze: np.ndarray, name: str = "saved_maze.csv") -> None:
    """
    Funkce uloží bludiště do csv souboru. Můžeme zvolit název souboru

    Args:
        maze (np.ndarray): bludiště k uložení
        name (str): název souboru

    Returns:
        None: Funkce pouze uloží bludiště
    """

    np.savetxt(name, maze, delimiter=',', fmt='%d')
    return