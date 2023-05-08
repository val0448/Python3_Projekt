import matplotlib.pyplot as plt
import scipy.sparse as sps
from queue import Queue
import numpy as np
from typing import Union

class Maze:
    def __init__(self, file_name: str = None, size: int = None, type: str = None, iter: int = None):
        """
        Konstruktor třídy Maze může buď načíst existující bludiště z csv souboru nebo vytvořit zcela nové dle zvolených parametrů.

        Args:
            self
            file_name (str): název souboru k načtení,
            size (int): velikost nového bludiště,
            type (str): typ nového bludiště(empty, S, N, Z, middle, spiral),

        """
        
        if (file_name is not None):
            self.maze = self.load_maze(file_name)
            self.incidence = None
            self.inc_size = None
            self.solvable = None
            self.graph = {}
        elif (size is not None):
            if(iter is None):
                self.maze = self.maze_template(size, type)
                self.incidence = None
                self.inc_size = None
                self.solvable = None
                self.graph = {}
            else:
                self.generate_maze(size, type, iter)
        else:
            raise ValueError("Either 'file_name' or 'size' parameter must be provided")
        self.path = []
        self.coords = []

    def load_maze(self, file_name: str) -> Union[np.ndarray, None]:
        """
        Metoda příjme jako argument název soubor, kde je uloženo čtvercové bludiště a vráti boolean matici reprezentující toto bludiště.
        Zároveň nastaví atribut shape na rozměr tohoto bludiště.

        Args:
            self
            file_name (str): název souboru k načtení,

        Returns:
            Union[np.ndarray, None]: bool matice reprezentující bludiště nebo None, pokud bylo načteno nevhodné bludiště,
        """

        # Načtení bludiště ze souboru
        maze = np.loadtxt("Bludiště_zadaní/data/"+file_name, delimiter=',')

        # ověření že je bludiště čtvrecové
        m, n = np.shape(maze)
        if(m != n):
            print("Bludiště není čtvercové!")
            return

        self.shape = n
        # Převedení na boolovskou matici
        maze = maze.astype(bool)

        return maze

    def create_incidence(self) -> sps.lil_matrix:
        """
        Metoda vytvoří matici incidence reprezentující dané bludiště.

        Args:
            self,

        Returns:
            sp.sparse.lil_matrix: matice incidence,
        """

        # vytvoříme matici incidence pro všechny buňky průchozí
        n = self.shape
        A = sps.lil_matrix((n*n, n*n), dtype=bool)
        self.inc_size = n*n
        for i in range(n):
            for j in range(n):
                index = i * n + j
                if j > 0:
                    A[index, index-1] = True
                if j < n-1:
                    A[index, index+1] = True
                if i > 0:
                    A[index, index-n] = True
                if i < n-1:
                    A[index, index+n] = True

        # převedeme bludiště na 1D pole pro nulování příslušných řádků a sloupců matice
        maze_cells = self.maze.copy().reshape(-1)
        A[maze_cells, :] = False
        A[:, maze_cells] = False

        return A

    def has_path(self) -> None:
        """
        Metoda vytvoří graf průchodu bludiště jako slovník a vyhodnotí, jesli má dané bludiště řešení za použití průchodu do šířky.
        Metoda řeší průchodnost bludištěm mezi levýmm horním rohem a pravým dolním rohem.

        Args:
            self,

        Returns:
            None: Metoda nastaví atribut graph na graf průchodu bludiště a atribut solvable na True pokud bludiště má cestu, v opačném případě na False,
        """

        # algoritmus prohledání do šířky
        n = self.inc_size
        queue = Queue()
        queue.put(0)
        parent = {0: None} # chceme uložit parent od každého vrcholu
        
        while (not queue.empty()):
            current_vertex = queue.get()
            if (current_vertex == n-1):
                break
            for neighbor in self.incidence.rows[current_vertex]: # list nenulových prvků odpovídajících aktuálnímu vrcholu
                if (neighbor not in parent):
                    parent[neighbor] = current_vertex
                    queue.put(neighbor)

        if n-1 not in parent:
            self.solvable = False
        else:
            self.solvable = True
            self.graph = parent

        return
    
    def find_shortest_path(self) -> list:
        """
        Metoda najde nejkratší cestu v bludišti za použití metody has_path() a vrátí list vrcholů této cesty.
        Funkce řeší průchodnost bludištěm mezi levýmm horním rohem a pravým dolním rohem.

        Args:
            self,

        Returns:
            list: funkce vrátí list obsahující vrcholy nejkratší cesty,
        """

        if(self.graph == {}):
            self.has_path()

        if(not self.solvable):
            print("Bludiětě nemá řešení")
            return []

        current_vertex = self.inc_size-1
        path = [current_vertex]
        while current_vertex != 0:
            current_vertex = self.graph[current_vertex]
            path.append(current_vertex)

        return path[::-1] # obrátíme seznam s path

    def get_shortest_path_coords(self) -> list:
        """
        Metoda převede nejkratší cestu v bludišti na souřadnice v bludišti této cesty.

        Args:
            self,

        Returns:
            list: list se souřadnicema nejkratší cesty v bludišti,
        """

        if(not self.path):
            return [] # cesta nenalzena
        shortest_path_coords = []
        for node in self.path:
            m, n = node // self.shape, node % self.shape # výpočet řádku a sloupce
            shortest_path_coords.append((m, n))

        return shortest_path_coords
    
    def solve_maze(self, draw: bool = False, save_png: bool = False, save_csv: bool = False, name: str = "maze") -> None:
        """
        Metoda slouží k vyřešení bludiště za použití matice incidence a algoritmu průchodu do hloubky.
        Metoda je schopná také zavolat metodu draw_maze a vykreslit tak vyřešené bludiště a případně ho uložit do souboru.

        Args:
            self
            draw (bool): True pokud chceme i bludiště vykreslit, v opačném případě False,
            save_png (bool): True pokud chceme vykreslené bludiště uložit do png souboru, v opačném případě False,
            save_csv (bool): True pokud chceme bludiště uložit do csv souboru, v opačném případě False,
            name (str): Název pod kterým bude bludiště uloženo,

        Return:
            None: Metoda nic nevrací, pouze upraví potřebné atributy a případně vykreslí a uloží bludiště,
        """

        if(self.incidence is None):
            self.incidence = self.create_incidence()
        self.path = self.find_shortest_path()
        self.coords = self.get_shortest_path_coords()

        if(draw):
            self.draw_maze(save = save_png, name = name)

        if(save_csv):
            self.save_maze(name = name)
    
    def draw_maze(self, save: bool = False, name: str = "maze", unsolved: bool = False) -> None:
        """
        Metoda vykreslí bludiště, případně ho i uloží do souboru dle parametru save pod názvem name.

        Args:
            self
            save (bool): V základu False, pokud nastaveno na True, tak bludiště uloží i do souboru,
            name (str): Název souboru k uložení,
            unsolved (bool): vykreslí nevyřešené bludiště

        Returns:
            None: funkce pouze vykreslí bludiště,
        """

        plt.imshow(self.maze, cmap=plt.cm.binary)
        if(not unsolved):
            if(self.coords):
                ys, xs = zip(*self.coords)
                plt.plot(xs, ys, 'r')
        if(save):
            plt.savefig(name, format='png')
        plt.show()

        return

    def maze_template(self, size: int, type: str = "empty") -> np.ndarray:
        """
        Metoda vytvoří vybraný template bludiště se zvolenou velikostí. Vrátí prázdné bludiště při nezvolení typu či zvolení neplatného typu.

        Args:
            self
            size (int): požadovaná velikost bludiště,
            type (str): požadováný vzor bludiště (empty, S, N, Z, middle, spiral),

        Returns:
            np.ndarray: template bludiště (bool),
        """

        self.shape = size
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


    def fill_maze(self) -> None:
        """
        Metoda zaplní bludiště na náhodném místě a zajistí, že je stále průchozí.

        Args:
            self,

        Returns:
            None: Metoda nic nevrací, pouze uprací potřebné atributy bludiště,
        """

        n = self.shape
        filled = False
        fill_attempts = 0

        while((not filled) and (fill_attempts < 10)):
            # vybereme náhoný vrchol k zaplnění
            i = np.random.randint(n)
            j = np.random.randint(n)

            free_attempts = 0
            while((self.maze[i,j]) and (free_attempts < 100)):    # generujeme znovu pokud je pole již zaplněné
                free_attempts += 1 
                i = np.random.randint(n)    
                j = np.random.randint(n)

            if (free_attempts >= 100):
                break

            index = (i * n) + j # odpovídající řádek a sloupec incidenční matice
            row = self.incidence[index, :]
            col = self.incidence[:, index]
            self.incidence[index, :] = False
            self.incidence[:, index] = False
            self.has_path()
            if(not self.solvable): # vyhodnotíme jestli bludiště má cestu
                fill_attempts += 1
                self.incidence[index, :] = row   # vrátíme matici incidence na původní hodnoty
                self.incidence[:, index] = col
                continue
                
            self.maze[i, j] = True
            filled = True

        return

    def generate_maze(self, size: int, type: str = "empty", iter: int = 100) -> None:
        """
        Metoda vygeneruje a nové bludiště na základě zadaných parametrů

        Args:
            self
            size (int): požadovaná velikost bludiště,
            type (str): požadováný vzor bludiště (empty, S, middle, N),
            iter (int): počet iterací generovacího cyklu,

        Returns:
            None: Metoda nic nevrací, pouze aktualizuje potřebné atributy,
        """

        self.maze = self.maze_template(size, type)
        self.incidence = self.create_incidence()

        # snažíme se bludiště zaplnit v každé iteraci
        for i in range(iter):
            self.fill_maze()

        return

    def save_maze(self, name: str = "maze.csv") -> None:
        """
        Metoda uloží bludiště do csv souboru. Můžeme zvolit název souboru.

        Args:
            self
            name (str): název souboru,

        Returns:
            None: Metoda pouze uloží bludiště,
        """

        np.savetxt(name, self.maze, delimiter=',', fmt='%d')
        return