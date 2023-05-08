# Bludiště

Cílem projektu je vytvořit knihovnu, která bude schopna načíst libovolné čtvercové bludiště, najít v něm nějkratší cestu a tu následně i s bludištěm vykreslit i s touto cestou. Dále je knihovna schopná také genereovat nové bludiště, které má řešení, za použití různých vzorů. Knihovna je uložena v souboru maze.py a ukázka funkcionalit je v souboru examples.ipynb. Podrobnější zadání a testovací data jsou ve složce Bludiště_zadaní. Řešení je pojato OOP, kde Maze je třída a jednotlivé funkce jsou její metody.

## Řešení bludiště

Bludiště načteme a uložíme. Poté vytvoříme matici incidence reprezentující toto bludiště, která nám dává informaci o každém vrcholu a do jakého vrcholu se z něj můžeme dostat. Poté použijeme algoritmus průchodu do šířky z levého horního rohu do pravého dolního rohu a uložíme si graf tohoto průchodu do datové struktury dictionary. Následně projdeme graf od konce a sestavíme nejkratší cestu v podobě listu vrcholů a otočíme pořadí. Vrcholy převedeme na souřadnice v původním bludišti. Bludiště pak vykreslíme i s nejkratší cestou vyznačenou červeně.

## Generování bludiště

Vytvoříme prázné bludiště pouze s okrajema, které případně zaplníme zdmi dle námi požadovaného typu. Bludiště se poté budeme snažit zaplnit v náhodných místech, kde ještě není zaplněné (pokud takové místo nenalezneme v určitém počtu pokusů, tak pokračujeme dále beze změny). Každé zaplnění si prvně zaznačíme do matice incidence a pomocí algoritmu průchodu do šířky otestujeme, jestli je bludiště stále průchozí. Pokud je, tak změnu zaznačíme i v bludišti a pokračujeme dále. Pokud bludiště průchozí není, tak změnu v matici vrátíme a zkusíme bludiště zaplnit znovu v náhodném místě. Po určitém počtu nezdařených pokusů pokračujeme beze změny v tomto kroku. Tento proces opakujeme dokud nevyčerpáme námi zvolený počet opakování. Bludiště vrátíme a můžeme si jej vykreslit či uložit do souboru.

## Obsah třídy Maze

V této části najdete kompletní seznam všech atributů a metod pro řešení a generování bludiště, spolu s důležitými poznámkami k nim.

### Atributy

**maze:**
Bludiště uložené jako numpy matice s hodnotami True (neprůchozí) a False (průchozí)

**shape:**
Rozměr čtvercového bludiště (int)

**incidence:**
Matice incidence daného bludiště uložená jako scipy.sparse.lil_matrix

**inc_size:**
Rozměr matice incidence (int)

**solvable:**
True pokud bludiště má řešení, v opačném případě False

**graph:**
Graf průchodu bludištěm do šířky, uložený jako slovník (vertex:parent)

**path:**
Seznam vrcholů nejkratší cesty v bludišťi

**coords:**
Seznam souřadnic vrcholů nejkratší cesty

### Metody

**load_maze():**

Metoda načte a uloží bludiště do přiřazené proměnné. Fuknce předpokládá, že bludiště k načtení bude uloženo ve slžce s daty a bude zachována struktura repozitáře. V opačném případě je třeba funkci lehce upravit pro správné načtení z nové cesty.

**draw_maze():**

Metoda pomocí knihovny matplotlib.pyplot vykreslí dané bludiště. Pokud je bludiště již vyřešené a má řešení, funkce zárověň vykreslí i nejkratší cestu červeně. Nevyřešené bludiště metoda pouze vykreslí bez cesty. Pokud máme bludiště již vyřené, ale chceme ho vykreslit nevyřešené, stačí nastavit parametr unsolved=True. Můžeme nastavit argument save=True pro uložení bludiště do souboru a vybrat i název pomocí parametru name.

**create_incidence():**

Metoda vytvoří matici incidence daného bludiště a zároveň uloží rozměry této matice.

**has_path():**

Metoda používá matici incidence a algortimus průchodu do šířky pro vytvoření grafu, Dále funkce rozhodne, jestli je bludiště průchozí či nikoliv a tuto informaci uloží do atributu solvable. Pokud je průchozí, metoda uloží i graf do atributu graph.

**find_shorstest_path():**

Metoda využívá přechozí metodu pro vytvoření grafu průchodu bludiště. Pokud je cesta naleze, metoda vrátí seznam vrcholů cesty od začátku do konce. Pokud se cesta nenajde, metoda vypíše "Bludiště nemá řešení" a vrátí prázdný seznam.

**get_shortest_path_coords():**

Metoda převede list vrcholů nejkratší cesty na souřadnice v původním bludišti. Pokud cesta neexistuje opět vrátí prázdný seznam.

**solve_maze():**

Metoda kombinuje předchozí metody pro vyřešení bludiště v jednom zavolání. Vytvoří matici incidence, rozhodne o řešitelnosti a najde nejkratší cestu. Metoda je také schopná zavolat metodu draw_maze() pro případné vykreslení a uložení řešení nebo bludiště.

**maze_template():**

Metoda vytvoří bludiště zvolené velikosti a zvoleného typu.
- empty: vytvoří prázdné bludiště pouze s okrajema
- S: vytvoří bludiště s průchodem ve tvaru obráceného S (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- N: vytvoří bludiště s průchodem ve tvaru obráceného N (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- Z: vytvoří bludiště s průchodem ve tvaru Z (při zadání velikosti <10 vrátí prázdné bludiště, protože tento typ nemá smysl)
- middle: vytvoří bludiště s průchodem uprostřed (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- spiral: vytvoří bludiště ve tvaru spirály (při zadání velikosti <16 vrátí prázdné bludiště, protože tento typ nemá smysl)
Pokud je zadán neplatný typ, funkce vrátí prázdné bludiště.

**fill_maze():**

Metoda se při zavolání snaží zaplnit bludiště v jednom náhodně zvoleném místě a aktualizuje bludiště a jeho matici incidence. Kontroluje jestli je nové bludiště průchozí, pokud není, vrátí se k původním hodnotám a zkusí bludiště zaplnit náhodně znovu. Po určitém počtu nezdařených pokusů vrátí původní bludiště a jeho matici incidence.

**generate_maze():**

Metoda používá metodu maze_template() k vytvoření nového bludiště a následně metodu fill_maze() k jeho zaplnění na základě zvolených parametrů.

**save_maze():**

Metoda slouží k uložení matice bludiště do souboru ve formátu csv. Můžeme zvolit název.