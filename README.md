# Projeto 2 - Atribuição de Rotas em Camiões

## Descrição

Programa que resolve o problema de atribuição de rotas (pares origem-destino) a camiões baseado no número de caminhos existentes entre cada par de nós numa rede de cruzamentos.

## Compilação

```bash
g++ -std=c++11 -O3 -Wall p2.cpp -o p2 -lm
```

## Execução

```bash
./p2 < teste.in
```

## Gerador Instâncias

compilar:

g++ -std=c++11 -O3 -Wall gerador_p2.cpp -o gerador_p2 -lm

testar:

./gerador_p2 N M D

N = nº vertices
M = nº camiões
D = edge prob (0-100)
S = random seed umer (optional)

## Formato de Entrada

```
N
M
m1 m2
K
u1 v1
u2 v2
...
uK vK
```

Onde:
- `N`: Número de cruzamentos (nós)
- `M`: Número total de camiões
- `m1`: ID do primeiro camião a atribuir rotas
- `m2`: ID do último camião a atribuir rotas
- `K`: Número de arestas no grafo
- `ui vi`: Aresta de cruzamento ui para cruzamento vi

## Formato de Saída

```
C<id_camiao> a1,b1 a2,b2 ... an,bn
```

Para cada camião de m1 a m2:
- `C<id_camiao>`: Identificador do camião
- `a,b`: Rotas atribuídas (pares origem-destino)

## Testes

Executar todos os testes:

```bash
clear && g++ -std=c++11 -O3 -Wall p2.cpp -o p2 -lm && \
for f in tests/*.in; do 
    base="${f%.in}"
    sol="${base}.sol.out"
    if [ -f "$sol" ]; then
        printf "== %s ==\n" "$f"
        timeout 10s ./p2 < "$f" > /tmp/my_out 2>/dev/null
        if diff -q "$sol" /tmp/my_out > /dev/null 2>&1; then
            echo "MATCH"
        else
            echo "DIFF"
        fi
    fi
done
```