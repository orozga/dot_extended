# DOT-X (DOT Extended)

DOT-X to rozszerzenie języka DOT, wprowadzające mechanizmy abstrakcji znane z języków programowania wyższego poziomu.

Celem projektu jest redukcja powtarzalnego kodu (boilerplate) podczas tworzenia złożonych grafów, takich jak diagramy architektoniczne czy schematy sieci, poprzez wprowadzenie reużywalnych komponentów oraz makr.

## Główne założenia

1. Parametryzowane komponenty: Możliwość definicji własnych typów węzłów i podgrafów, które przyjmują parametry wejściowe, a następnie mogą być wielokrotnie wywoływane w kodzie.
2. Skróty składniowe (makra): Mechanizm umożliwiający definicję aliasów dla długich i często powtarzających się zestawów atrybutów lub typów połączeń.
3. Transpilacja: Narzędzie kompiluje kod ze składni `.dotx` do standardowego formatu `.dot`, zachowując pełną kompatybilność z narzędziami z pakietu Graphviz.

## Składnia i przykłady

Poniższy przykład demonstruje jednoczesne użycie własnych skrótów składniowych oraz parametryzowanych komponentów w jednym pliku. Komponenty pozwalają na hermetyzację właściwości, a zmienne wewnątrz nich poprzedzone są znakiem `$`.

**Plik wejściowy (example.dotx):**
```dot
// Definicja skrótów składniowych (makr)
defshortcut <..> => -> [dir=none, style=dotted, color=gray];
defshortcut <err> => -> [color=red, penwidth=2.0];

// Definicja komponentu z trzema parametrami
component ServiceNode(id, label_text, color_name) {
    $id [
        shape=box, 
        style="rounded,filled", 
        fillcolor=$color_name, 
        label=$label_text,
        fontname="Helvetica"
    ];
}

digraph System {
    // Instancjonowanie komponentów
    ServiceNode(auth_svc, "Usługa Autoryzacji", "lightblue");
    ServiceNode(db_svc, "Baza Danych", "lightgreen");
    ServiceNode(cache_svc, "Pamięć Podręczna", "lightpink");
    
    // Definiowanie relacji (standardowych i z użyciem makr)
    auth_svc -> db_svc;
    auth_svc <..> cache_svc;
    cache_svc <err> db_svc;
}
```