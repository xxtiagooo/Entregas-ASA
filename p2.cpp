#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

using UI = unsigned int;
using Adjacents = vector<vector<UI>>;
using NumPaths = vector<vector<int>>;
using ReachabilityTable = vector<vector<short>>;
using PathResult = pair<int, bool>;  // <num_paths, is_reachable>
using TruckAssignments = map<UI, vector<string>>;

void readInput(UI k, UI n, Adjacents& adjacent) {
    adjacent.resize(n + 1);

    for (UI i = 0; i < k; i++) {
        UI a, b;
        // lê ai, bi
        cin >> a >> b;
        adjacent[a].push_back(b);
    }
}

vector<UI> computeTopologicalOrder(UI n, const Adjacents& adjacent) {
    vector<UI> in_degree(n + 1, 0);
    for (UI u = 1; u <= n; ++u) {
        for (UI v : adjacent[u]) {
            in_degree[v]++;
        }
    }

    vector<UI> queue;
    for (UI i = 1; i <= n; ++i) {
        if (in_degree[i] == 0) {
            queue.push_back(i);
        }
    }

    vector<UI> order;
    UI head = 0;
    while (head < (UI)queue.size()) {
        UI u = queue[head++];
        order.push_back(u);

        for (UI v : adjacent[u]) {
            in_degree[v]--;
            if (in_degree[v] == 0) {
                queue.push_back(v);
            }
        }
    }
    return order;
}

UI find_truck_number(UI num_paths, UI m) {
    UI paths = num_paths + 1;
    if (paths >= m)
        paths -= m;

    UI truck_number = paths % m;

    // Se (num_paths + 1) for múltiplo de m, o módulo é 0 e o camião é o m.
    if (truck_number == 0)
        return m;

    return truck_number;
}

void showResults(const TruckAssignments& truck_assignments, UI m1, UI m2) {
    for (UI truck_number = m1; truck_number <= m2; truck_number++) {
        cout << "C" << truck_number;
        auto it = truck_assignments.find(truck_number);
        if (it != truck_assignments.end()) {
            for (const string& assignment : it->second) {
                cout << " " << assignment;
            }
        }
        cout << "\n";
    }
}

void solve(UI n, UI m, UI m1, UI m2, const Adjacents& adjacent) {
    NumPaths count(n + 1, vector<int>(n + 1, 0));
    ReachabilityTable reach(n + 1, vector<short>(n + 1, 0));

    vector<UI> order = computeTopologicalOrder(n, adjacent);
    int i = (int)order.size() - 1;
    for (; i >= 0; --i) {
        UI u = order[i];

        for (UI w : adjacent[u]) {
            // u -> w
            count[u][w]++;
            if ((UI)count[u][w] >= m)
                count[u][w] -= m;
            reach[u][w] = 1; // true

            for (UI v = 1; v <= n; ++v) {
                // Sem 'if' para permitir vetorização
                int val = count[u][v] + count[w][v];
                if ((UI)val >= m)
                    val -= m;
                count[u][v] = val;
                // se um dos reach é 1, o resultado é 1 (true)
                reach[u][v] = reach[u][v] | reach[w][v];
            }
        }
    }

    TruckAssignments truck_assignments;

    for (UI a = 1; a <= n; a++) {
        for (UI b = 1; b <= n; b++) {
            if (a == b)
                continue;

            if (reach[a][b]) {
                UI num_paths = count[a][b];
                UI truck_number = find_truck_number(num_paths, m);

                if (truck_number >= m1 && truck_number <= m2) {
                    truck_assignments[truck_number].push_back(
                        to_string(a) + "," + to_string(b));
                }
            }
        }
    }
    showResults(truck_assignments, m1, m2);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    UI n, k, m, m1, m2;
    Adjacents adjacent;
    // lê n, m, m1, m2, k
    cin >> n >> m >> m1 >> m2 >> k;
    readInput(k, n, adjacent);
    solve(n, m, m1, m2, adjacent);
    return 0;
}