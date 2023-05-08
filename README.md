# Bludiště

Cílem projektu je vytvořit knihovnu funkcí, která bude schopna načíst libovolné čtvercové bludiště, najít v něm nějkratší cestu a tu následně i s bludištěm vykreslit. Dále je knihovna chopná také gnereovat nové bludiště, které má řešení, za použití různých vzorů. Knihovna je uložena v souboru maze.py a ukázka funkcionalit je v souboru examples.ipynb. Podrobnější zadání a testovací data jsou ve složce Bludiště_zadaní

## Řešení bludiště

Bludiště načteme a uložíme. Poté vytvoříme matici incidence reprezentující toto bludiště, která nám dává informaci o každém vrcholu a do jakého vrcholu se z něj můžeme dostat. Poté použijeme algoritmus průchodu do šířky z levého horního rohu do pravého dolního rohu a uložíme si graf tohoto průchodu do datové struktury dictionary. Následně projdeme graf od konce a sestavíme nejkratší cestu v podobě listu vrcholů a otočíme pořadí. Vrcholy převedeme na souřadnice v původním bludišti, které vykreslíme i s nejkratší cestou vyznačenou červeně.

## Generování bludiště

Vytvoříme prázné bludiště pouze s okrajema, které případně zaplníme zdmi dle zvoleného námi požadovaného typu. Bludiště se poté budeme snažit zaplnit v náhodných místech, kde ještě není zaplněné (pokud takové místo nenalezneme v určitém počtu pokusů, tak pokračujeme dále beze změny). Každé zaplnění si prvně zaznačíme do matice incidence a pomocí algoritmu průchodu do šířky otestujeme, jestli je bludiště stále průchozí. Pokud je, tak změnu zaznačíme i v bludišti a pokračujeme dále. Pokud bludiště průchozí není, tak změnu v matici vrátíme a zkusíme bludiště zaplnit znovu v náhodném místě. Po určitém počtu nezdařených pokusů pokračujeme beze změny v tomto kroku. Tento proces opakujeme dokud nevyčerpáme námi zvolený počet opakování. Bludiště vrátíme a můžeme si vykreslit či uložit do souboru.

## Funkce v knihovně

V této části najdete kompletní seznam všech funkcí pro řešení a generování bludiště, spolu s důležitými poznámkami k nim

**load_maze()**
Funkce načte a uloží bludiště do přiřazené proměnné. Fuknce předpokládá, že bludiště k načtení bude uloženo ve slžce s daty a bude zachována struktura repozitáře. V opačném případě je třeba funkci lehce upravit pro správné načtení z nové cesty.

**draw_unsolved_maze()**
Funkce pomocí knihovny matplotlib.pyplot vykreslí dané bludiště. Můžeme nastavit argument save=True pro uložení bludiště do souboru.

**create_incidence()**
Funkce vytvoří matici incidence daného bludiště pro pozdější práci

**find_shorstest_path()**
Funkce nalezne v bludišti nejkratší cestu za použití matice incidence a algoritmu porhledávání do šířky. Pokud je cesta naleze, algoritmus vrátí seznam vrcholů cesty od začátku do konce. Pokud se cesta nenajde, algoritmus vypíše "Bludiště nemá řešení" aprázdný seznam

**has_path()**
Funkce používá funguje stejně jako předchozí, ale pouze kontroluje, jestli je bludiště průchozí či nikoliv.

**get_shortest_path_coords**
Funkce využije funkci find_shorstest_path() a dále list vrcholů převede na souřadnice v původním bludišti. Pokud cesta neexistuje opět vrátí prázdný seznam.

**draw_solved_maze**
Funkce využije funkci find_shorstest_path_coords() a pomocí knihovny matplotlib.pyplot vykreslí bludiště i s jeho nejkratší cestou v podobě červené čáry. Pokud cesta neexistuje, funkce pouze vykreslí bludiště pomocí funkce draw_unsolved_maze(). Můžeme nastavit argument save=True pro uložení bludiště do souboru.

**maze_template()**
Funkce vytvoří bludiště zvolené velikosti a zvoleného typu
- empty: vytvoří prázdné bludiště pouze s okrajema
- S: vytvoří bludiště s průchodem ve tvaru obráceného S (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- N: vytvoří bludiště s průchodem ve tvaru obráceného N (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- Z: vytvoří bludiště s průchodem ve tvaru Z (při zadání velikosti <8 vrátí prázdné bludiště, protože tento typ nemá smysl)
- middle: vytvoří bludiště s průchodem uprostřed (při zadání velikosti <7 vrátí prázdné bludiště, protože tento typ nemá smysl)
- spiral: vytvoří bludiště ve tvaru spirály (při zadání velikosti <16 vrátí prázdné bludiště, protože tento typ nemá smysl)
Pokud je zadán neplatný typ, funkce vrátí prázdné bludiště

**fill_maze()**
Funkce při zavolání příjme bludiště a jeho matici incidence a snaží zaplnit bludiště v jednom náhodně zvoleném místě a vrátí nové bludiště a jeho matici incidence. Kontroluje jestli je nové bludiště průchozí, pokud není, vrátí se k původním hodnotám a zkusí bludiště zaplnit náhodně znovu. Po určitém počtu nezdařených pokusů vrátí původní bludiště a jeho matici incidence.

**generate_maze()**
Funkce používá funkci maze_template() k vytvoření nového bludiště a následně funkci fill_maze() k jeho zaplnění na základě zvolených parametrů

**save_maze()**
Funkce slouží k uložení matice bludiště do souboru ve formátu csv. Můžeme zvolit název.