from lexer import lexer
from parser import parser

test_code = """
// 1. Importowanie zewnętrznych definicji
import "standard_theme.dotx";

// 2. Definicja stałych globalnych
const $PRIMARY_COLOR = "blue";
const $DEFAULT_WIDTH = 2.5;

// 3. Definicja makra krawędzi (Shortcut)
defshortcut <unstable> => -> [color=orange, style=dotted, label="timeout?"];

// 4. Definicja komponentu bazowego
component BaseNode(id) {
    $id [shape=circle, fontname="Arial"];
}

// 5. Dziedziczenie komponentów (Extends)
component ColoredNode(id, color) extends BaseNode($id) {
    $id [fillcolor=$color, style=filled, penwidth=$DEFAULT_WIDTH];
}

// 6. Główny graf z opcją strict
strict digraph ComplexSystem {
    // Atrybuty globalne
    node [fontsize=12];
    edge [arrowhead=vee];

    // Instancjonowanie komponentu
    ColoredNode(MainServer, $PRIMARY_COLOR);

    // Podgraf (Subgraph/Cluster)
    subgraph cluster_workers {
        label = "Worker Pool";
        color = grey;

        // 7. Pętla generująca topologię (For-Loop + Range)
        for $i in range(1 .. 3) {
            Worker_$i [label="Unit $i", shape=box];
            MainServer -> Worker_$i;
        }
    }

    // 8. Użycie makra krawędzi (Custom Operator)
    Database [shape=cylinder];
    MainServer <unstable> Database;

    // 9. Anonimowy podgraf (Scoping)
    {
        rank = same;
        Logger [shape=note];
        Worker_1 -> Logger;
    }
}
"""
print("Rozpoczynam analizę składniową DOT-X...")
ast_tree = parser.parse(test_code, lexer=lexer)

print("\nWygenerowane drzewo AST (Lista definicji):")
i = 0
for node in ast_tree:
    print(f"{i}.", node)
    i += 1
    print("-", node)
