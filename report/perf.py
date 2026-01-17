#!/usr/bin/env python3
import matplotlib.pyplot as plt


def plot_results():
    # Data from the table
    n_values = [100, 500, 1000, 1500, 2000, 2500, 3000,
                3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]
    k_values = [478, 12454, 50014, 112775, 200558, 312954, 450266, 612632,
                800004, 1012166, 1248588, 1511421, 1799081, 2112017, 2450471]
    times = [0.004, 0.004, 0.020, 0.060, 0.143, 0.297, 0.513,
             0.841, 1.275, 1.815, 2.453, 3.270, 4.331, 5.418, 6.804]

    # Calculate theoretical complexity f(n,k) = n(n+k)
    complexity = [n * (n + k) for n, k in zip(n_values, k_values)]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 12), gridspec_kw={"height_ratios": [2, 1]}
    )

    # Plot Time vs Complexity
    ax1.plot(complexity, times, "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("Complexidade Teórica: n(n+k)", fontsize=12)
    ax1.set_ylabel("Tempo (s)", fontsize=12)
    ax1.set_title("Análise Experimental: Tempo vs Complexidade", fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Add value labels on points
    for x, y, n in zip(complexity, times, n_values):
        ax1.annotate(
            f"N={n}\n{y:.3f}s",
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
        )

    # Table
    # Columns: N, K, f(n,k), Time
    table_data = []
    for n, k, c, t in zip(n_values, k_values, complexity, times):
        table_data.append([n, k, f"{c:.2e}", f"{t:.3f}"])

    col_labels = ["N (Nós)", "K (Caminhos)", "f(n,k) = n(n+k)", "Tempo (s)"]

    ax2.axis("tight")
    ax2.axis("off")
    table = ax2.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)

    plt.tight_layout()
    plt.savefig("grafico_performance_p2.png")
    print("Gráfico salvo como 'grafico_performance_p2.png'")
    plt.show()


if __name__ == "__main__":
    plot_results()
