# DOT-X

**Dane studentów:** Ulianiya Mukha, Olaf Rózga  
**Dane kontaktowe:** ulianamukha@student.agh.edu.pl, orozga@student.agh.edu.pl

## Założenia programu

**Krótki opis i cele programu:** Celem projektu jest stworzenie języka DOT-X, będącego rozszerzeniem standardowego języka DOT. Język wprowadza mechanizmy abstrakcji: parametryzowane komponenty oraz skróty składniowe (makra), co pozwala na redukcję powtarzalnego kodu przy tworzeniu złożonych diagramów. Transpilator zachowuje przy tym kompatybilność z klasycznymi konstrukcjami języka DOT.

**Rodzaj translatora:** Kompilator (transpilator źródło-źródło).

**Planowany wynik działania programu:** Kompilator kodu w języku DOT-X do czystego kodu języka DOT.

**Planowany język implementacji:** Python 3.

**Sposób realizacji skanera/parsera:** Wykorzystanie generatora parserów LALR(1) – biblioteki PLY (Python Lex-Yacc).

## Opis tokenów

Poniżej znajduje się tabela tokenów:

| Nazwa tokenu | Wyrażenie regularne / Znak | Opis |
| :--- | :--- | :--- |
| `KW_COMPONENT` | `component` | Słowo kluczowe definicji komponentu (rozszerzenie) |
| `KW_DEFSHORTCUT`| `defshortcut` | Słowo kluczowe definicji makra (rozszerzenie) |
| `KW_STRICT` | `strict` | Słowo kluczowe określające graf bez krawędzi wielokrotnych |
| `KW_DIGRAPH` | `digraph` | Słowo kluczowe grafu skierowanego |
| `KW_GRAPH` | `graph` | Słowo kluczowe grafu nieskierowanego |
| `KW_SUBGRAPH` | `subgraph` | Słowo kluczowe podgrafu (klastra) |
| `KW_NODE` | `node` | Słowo kluczowe atrybutów globalnych węzłów |
| `KW_EDGE` | `edge` | Słowo kluczowe atrybutów globalnych krawędzi |
| `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Identyfikator węzła/grafu/parametru |
| `VAR_ID` | `\$[a-zA-Z_][a-zA-Z0-9_]*` | Zmienna wewnątrz komponentu (np. `$id`) |
| `STRING` | `\"[^\"]*\"` | Ciąg znaków |
| `NUMBER` | `\d+(\.\d+)?` | Liczba całkowita lub zmiennoprzecinkowa |
| `ARROW` | `->` | Skierowane połączenie krawędzi |
| `EDGE_UNDIR` | `--` | Nieskierowane połączenie krawędzi |
| `FAT_ARROW` | `=>` | Operator przypisania makra |
| `CUSTOM_OP` | `<[a-zA-Z0-9_\.\-]*>` | Niestandardowy operator użytkownika (np. `<..>`) |
| `LBRACE` / `RBRACE` | `{` / `}` | Nawiasy klamrowe |
| `LPAREN` / `RPAREN` | `(` / `)` | Nawiasy okrągłe |
| `LBRACKET` / `RBRACKET`| `[` / `]` | Nawiasy kwadratowe |
| `COMMA` | `,` | Przecinek |
| `EQUALS` | `=` | Znak równości (przypisanie atrybutów) |
| `SEMI` | `;` | Średnik (opcjonalny terminator instrukcji) |

## Gramatyka formatu

Uproszczona gramatyka w notacji EBNF, opisująca pełną strukturę uwzględniającą klasyczny standard DOT oraz rozszerzenia DOT-X:

```ebnf
Program ::= TopLevelList

TopLevelList ::= TopLevelStmt TopLevelList | empty

TopLevelStmt ::= ComponentDef 
               | ShortcutDef 
               | GraphDef

/* ROZSZERZENIA DOT-X */

ComponentDef ::= "component" ID "(" ParamList ")" "{" GraphBody "}"

ParamList ::= ID 
            | ID "," ParamList 
            | empty

ShortcutDef ::= "defshortcut" CUSTOM_OP "=>" EdgeOp AttrBlockOpt SemiOpt

/* STANDARD DOT */

GraphDef ::= StrictOpt GraphType ID "{" GraphBody "}"
           | StrictOpt GraphType "{" GraphBody "}"

StrictOpt ::= "strict" | empty

GraphType ::= "digraph" | "graph"

GraphBody ::= GraphStatement GraphBody | empty

GraphStatement ::= NodeInst 
                 | EdgeInst 
                 | Subgraph 
                 | GlobalAttr 
                 | NodeId AttrBlockOpt SemiOpt

NodeId ::= ID | VAR_ID

NodeInst ::= NodeId "(" ArgList ")" SemiOpt

ArgList ::= Value 
          | Value "," ArgList 
          | empty

EdgeInst ::= NodeId EdgeOp NodeId AttrBlockOpt SemiOpt

EdgeOp ::= "->" | "--" | CUSTOM_OP

Subgraph ::= "subgraph" ID "{" GraphBody "}"
           | "subgraph" "{" GraphBody "}"
           | "{" GraphBody "}"

GlobalAttr ::= GlobalType AttrBlockOpt SemiOpt

GlobalType ::= "graph" | "node" | "edge"

AttrBlockOpt ::= "[" AttrList "]" | empty

AttrList ::= Attr 
           | Attr "," AttrList 
           | empty

Attr ::= ID "=" Value

SemiOpt ::= ";" | empty

Value ::= STRING | ID | VAR_ID | NUMBER
```