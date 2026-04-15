from parser import parser
from lexer import lexer

test_code = """
// 1. Definicja skrótu DOT-X
defshortcut <err> => -> [color=red, style=dashed, penwidth=2];

// 2. Definicja komponentu DOT-X
component Serwer(id, bgColor) {
    $id [shape=box, style=filled, fillcolor=$bgColor];
}

// 3. Główny graf
digraph System {
    node [fontname="Arial"];
    
    // Instancjonowanie komponentów
    Serwer(Backend, blue);
    Serwer(Database, green);
    
    // Standardowe krawędzie i makra DOT-X
    Frontend -> Backend [weight=5];
    Backend <err> Database;
}
"""

print("Rozpoczynam analizę składniową DOT-X...")
ast_tree = parser.parse(test_code, lexer=lexer)

print("\nWygenerowane drzewo AST (Lista definicji):")
i=0
for node in ast_tree:
    print(f"{i}.", node)
    i+=1
    print("-", node)