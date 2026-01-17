#!/usr/bin/env python3
import subprocess
import sys
import re
import random
import matplotlib.pyplot as plt


def generate_test_input(n, m, k):
    """Generate a random test case"""
    # print(f"n={n}, m={m}, k={k}")
    # if m < 2: m = random.randint(10, 100)
    m1 = random.randint(1,m-1)
    m2 = random.randint(m1, m);
    final = f"{n}\n{m}\n{m1} {m2}\n{k}"
    
    # Let's pretend it cant go back, but shuffle it first (assim nao eh circular)
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)
    
    for i in range(k):
         u_idx = random.randint(0, n-2)
         v_idx = random.randint(u_idx+1, n-1)
         final += f"\n{nodes[u_idx]} {nodes[v_idx]}"
             
    return final


def run_single_test(project, n, m, k):
    """Run a single test and measure execution time"""
    test_input = generate_test_input(n, m, k)

    cmd = [f"./{project}"]
    result = subprocess.run(
        cmd, input=test_input, capture_output=True, text=True, timeout=60
    )

    # Get execution time from /usr/bin/time or measure it ourselves
    import time

    start = time.time()
    result = subprocess.run(
        cmd, input=test_input, capture_output=True, text=True, timeout=60
    )
    elapsed = time.time() - start

    return elapsed





# ALTERAR AQUI A COMPLEXIDADE
def complexidade(n,m,k):
    return n*n + n*k

def plot_results(tests, times, project):
    """Create a plot of N vs execution time and a table"""
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [2, 1]}
    )

    x_values = [complexidade(n,m,k) for (n,m,k) in tests]

    # Plot
    ax1.plot(x_values, times, "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("n(n+k)", fontsize=12) # ALTERAR AQUI O TEXTO DA COMPLEXIDADE
    ax1.set_ylabel("Tempo (s)", fontsize=12)
    ax1.set_title(f"Análise experimental", fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Add value labels on points
    for n, t in zip(x_values, times):
        ax1.annotate(
            f"{t:.3f}s",
            (n, t),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=9,
        )

    # Table
    table_data = [[n, m, k, complexidade(n,m,k), f"{t:.4f}"] for (n,m,k), t in zip(tests, times)]
    print(f"LEN={len(table_data)}")
    ax2.axis("tight")
    ax2.axis("off")

    plt.tight_layout()
    plt.savefig(f"{project}_performance_graph.png", dpi=150)
    print(f"Graph saved as '{project}_performance_graph.png'")
    plt.show()

    # Create a new figure just for the table
    fig_table, ax_table = plt.subplots(figsize=(10, max(4, len(table_data) * 0.3)))
    ax_table.axis("off")

    table = ax_table.table(
        cellText=table_data,
        colLabels=["N", "M", "K", "N²", "Tempo (s)"],
        cellLoc="center",
        loc="center",
        colWidths=[0.15, 0.15, 0.15, 0.25, 0.3],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    num_cols = len(table_data[0])

    # Style header
    for i in range(num_cols):
        table[(0, i)].set_facecolor("#4CAF50")
        table[(0, i)].set_text_props(weight="bold", color="white")

    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(num_cols):
            if i % 2 == 0:
                table[(i, j)].set_facecolor("#f0f0f0")
    
    plt.tight_layout()
    plt.savefig(f"{project}_performance_table.png", dpi=150)
    print(f"Table saved as '{project}_performance_table.png'")
    plt.show()

def mklist(min, max, reps, elevated=1):
    if reps==1:
        return [min]
    def phase(i): # like uzi vert
        return (i*((max-min)**elevated)/(reps-1))**(1/elevated)
    print(f"phase(0)={phase(0)}, phase(1)={phase(1)}")
    return [min+phase(i) for i in range(reps)]

if __name__ == "__main__":
    if len(sys.argv) < 12 and len(sys.argv) != 8 and len(sys.argv) != 9:
        print(
            "Usage with reps for n: python3 perf.py <project> <avgreps> <Nmin> <Nmax> <Nreps> <M> <K> [seed]\n"
            "Usage with reps for all: python3 perf.py <project> <avgreps> <Nmin> <Nmax> <Nreps> <Mmin> <Mmax> <Mreps> <Kmin> <Kmax> <Kreps> [seed]"
        )
        print("Example1 (n^2): python3 perf.py projeto 3 100 5000 20 30 1000")
        print("Example2 (n*m*k): python3 perf.py projeto 3 100 1000 5 10 1000 2 10 1000 5")
        sys.exit(1)


    project = sys.argv[1]
    avgreps = int(sys.argv[2])
    nmin = int(sys.argv[3])
    nmax = int(sys.argv[4])
    nreps = int(sys.argv[5])
    if len(sys.argv)==8 or len(sys.argv)==9:
        mreps = kreps = 1
        mmin = mmax = int(sys.argv[6])
        kmin = kmax = int(sys.argv[7])
        seed = int(sys.argv[8]) if len(sys.argv) == 9 else None
    else:
        mmin = int(sys.argv[6])
        mmax = int(sys.argv[7])
        mreps = int(sys.argv[8])
        kmin = int(sys.argv[9])
        kmax = int(sys.argv[10])
        kreps = int(sys.argv[11])
        seed = int(sys.argv[12]) if len(sys.argv) > 12 else None

    nlist = mklist(nmin, nmax, nreps, 2)
    mlist = mklist(mmin, mmax, mreps)
    klist = mklist(kmin, kmax, kreps)
    print(f"nlist={nlist}, mlist={mlist}, klist={klist}")

    tests = []
    times = []

    for m in mlist:
        m = round(m)
        for k in klist:
            k = round(k)
            for n in nlist:
                n = round(n)
                tests.append((n,m,k))
    
    for (n,m,k) in tests:
        print(f"Testing n={n}, m={m}, k={k}")
        total = 0
        for i2 in range(avgreps):
            total += run_single_test(project, round(n), round(m), round(k))
        elapsed = total / avgreps
        times.append(elapsed)
        # print(f"{elapsed:.3f}s")
                
                

    
    # Sort tests according to complexity. (Imagine its k*n, we cant order by n)
    if tests and times:
        combined = sorted(zip(tests, times), key=lambda x: complexidade(x[0][0], x[0][1], x[0][2]))
        tests, times = zip(*combined)
        tests = list(tests)
        times = list(times)


    plot_results(tests, times, project)


