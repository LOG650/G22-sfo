#!/usr/bin/env python3
"""
Genererer WBS-diagram basert på MS Project-strukturen.
Produserer: wbs_diagram.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# --- WBS-data fra MS Project (screenshot) ---
wbs_data = {
    "root": {
        "code": "G22",
        "name": "LOG650 — Space Management\ni dagligvarebutikk",
        "color": "#1a1a2e",
    },
    "phases": [
        {
            "code": "1",
            "name": "FASE 2\nPLANLEGGING",
            "color": "#2d6a4f",
            "tasks": [
                {"code": "1.1", "name": "Prosjektplan"},
                {"code": "1.2", "name": "WBS og Gantt\n(MS Project)"},
                {"code": "1.3", "name": "Risikoanalyse"},
                {"code": "1.4", "name": "Litteratursøk"},
                {"code": "1.5", "name": "Rapportskjelett\ni Word-mal"},
                {"code": "1.6", "name": "M1: Godkjent\nprosjektplan"},
            ],
        },
        {
            "code": "2",
            "name": "FASE 3\nGJENNOMFØRING",
            "color": "#1d3557",
            "tasks": [
                {"code": "2.1", "name": "Innledning +\nproblemstilling"},
                {"code": "2.2", "name": "Lese referanser\n+ KI-oppsummering"},
                {"code": "2.3", "name": "Teorikapittel"},
                {"code": "2.4", "name": "Avklare\ndatatilgang"},
                {"code": "2.5", "name": "Signere\ntaushetserklæring"},
                {"code": "2.6", "name": "Innhente\nsalgs-/hylledata"},
                {"code": "2.7", "name": "Datarensing\n(pandas)"},
                {"code": "2.8", "name": "Case-\nbeskrivelse"},
                {"code": "2.9", "name": "Beskrive\nmetodevalg"},
                {"code": "2.10", "name": "Etterspørsels-\nanalyse (ABC)"},
                {"code": "2.11", "name": "Formulere\nLP-modell"},
                {"code": "2.12", "name": "Implementere\nmodell (PuLP)"},
                {"code": "2.13", "name": "Kjøre modell\n+ resultater"},
                {"code": "2.14", "name": "Metode-/\nmodellkapittel"},
                {"code": "2.15", "name": "Presentere\nresultater"},
                {"code": "2.16", "name": "Sensitivitets-\nanalyse"},
                {"code": "2.17", "name": "Resultat-\nkapittel"},
                {"code": "2.18", "name": "Diskusjons-\nkapittel"},
                {"code": "2.19", "name": "Samle\nhovedutk."},
                {"code": "2.20", "name": "Peer-to-peer\nreview"},
                {"code": "2.21", "name": "M2: Godkjent\nhovedutk."},
            ],
        },
        {
            "code": "3",
            "name": "FASE 4\nAVSLUTNING",
            "color": "#6d2e46",
            "tasks": [
                {"code": "3.1", "name": "Konklusjon"},
                {"code": "3.2", "name": "Ferdigstille\ninnledning"},
                {"code": "3.3", "name": "Kvalitetssikring\nkorrektur, ref."},
                {"code": "3.4", "name": "Python-kode +\ndokumentasjon"},
                {"code": "3.5", "name": "Forberede\npresentasjon"},
                {"code": "3.6", "name": "Muntlig\neksamen"},
                {"code": "3.7", "name": "M3: Innlevert\nrapport + kode"},
            ],
        },
    ],
}

# --- Gruppering av Fase 3 oppgaver i logiske klynger ---
fase3_groups = [
    {
        "name": "Teori & litteratur",
        "color": "#264653",
        "tasks": ["2.1", "2.2", "2.3"],
    },
    {
        "name": "Data & case",
        "color": "#2a6f97",
        "tasks": ["2.4", "2.5", "2.6", "2.7", "2.8"],
    },
    {
        "name": "Modell & analyse",
        "color": "#014f86",
        "tasks": ["2.9", "2.10", "2.11", "2.12", "2.13"],
    },
    {
        "name": "Rapportkapitler",
        "color": "#468faf",
        "tasks": ["2.14", "2.15", "2.16", "2.17", "2.18"],
    },
    {
        "name": "Samling & review",
        "color": "#61a5c2",
        "tasks": ["2.19", "2.20", "2.21"],
    },
]


def draw_box(ax, x, y, w, h, text, color, fontsize=7, text_color="white", bold=False):
    """Tegn en avrundet boks med tekst."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor="white",
        linewidth=0.8,
        alpha=0.95,
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize, color=text_color,
        fontweight=weight,
        linespacing=1.2,
    )
    return x + w / 2, y  # Return bottom center for connector


def draw_line(ax, x1, y1, x2, y2, color="#888888"):
    """Tegn forbindelseslinje."""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=0.7, zorder=0)


def main():
    fig, ax = plt.subplots(1, 1, figsize=(32, 16))
    ax.set_xlim(-0.5, 31.5)
    ax.set_ylim(-1, 11)
    ax.axis("off")
    fig.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#f8f9fa")

    # --- Nivå 0: Prosjektrot ---
    root_w, root_h = 4, 0.7
    root_x = (31 - root_w) / 2
    root_y = 9.5
    rx, ry = draw_box(ax, root_x, root_y, root_w, root_h,
                       "G22 — Datadrevet Space Management\nCoop Extra X",
                       wbs_data["root"]["color"], fontsize=9, bold=True)

    # --- Nivå 1: Faser ---
    phase_positions = []
    phase_w, phase_h = 5.5, 0.6
    phase_xs = [1.5, 12, 23.5]
    phase_y = 8.2

    for i, (phase, px) in enumerate(zip(wbs_data["phases"], phase_xs)):
        cx, cy = draw_box(ax, px, phase_y, phase_w, phase_h,
                          f"{phase['code']}  {phase['name'].replace(chr(10), ' — ')}",
                          phase["color"], fontsize=8, bold=True)
        phase_positions.append((px, phase_y, phase_w))
        # Linje fra rot til fase
        draw_line(ax, rx, ry, cx, phase_y + phase_h)

    # --- Nivå 2: Fase 2 oppgaver (flat) ---
    task_w, task_h = 1.6, 0.55
    fase2_tasks = wbs_data["phases"][0]["tasks"]
    f2_start_x = 0.1
    f2_y = 7.0
    f2_cx = phase_positions[0][0] + phase_positions[0][2] / 2

    for j, task in enumerate(fase2_tasks):
        tx = f2_start_x + j * (task_w + 0.15)
        color = "#40916c" if "M1" not in task["code"] else "#b5838d"
        cx, cy = draw_box(ax, tx, f2_y, task_w, task_h,
                          f"{task['code']}\n{task['name']}", color, fontsize=6)
        draw_line(ax, f2_cx, phase_y, cx, f2_y + task_h)

    # --- Nivå 2: Fase 3 — gruppert i klynger ---
    group_y = 7.0
    task_y_base = 5.2
    f3_cx = phase_positions[1][0] + phase_positions[1][2] / 2

    # Beregn x-posisjoner for grupper
    total_tasks_f3 = len(wbs_data["phases"][1]["tasks"])
    task_w3, task_h3 = 1.05, 0.5
    group_gap = 0.3
    task_gap = 0.08

    # Bygg task lookup
    f3_task_lookup = {t["code"]: t for t in wbs_data["phases"][1]["tasks"]}

    current_x = 0.1
    group_positions = []

    for g, group in enumerate(fase3_groups):
        n_tasks = len(group["tasks"])
        group_w = n_tasks * (task_w3 + task_gap) - task_gap + 0.2
        group_x = current_x

        # Gruppeboks (bakgrunn)
        group_box = FancyBboxPatch(
            (group_x - 0.1, task_y_base - 0.15), group_w + 0.2, task_h3 + 0.7,
            boxstyle="round,pad=0.05",
            facecolor=group["color"],
            edgecolor="white",
            linewidth=0.5,
            alpha=0.15,
        )
        ax.add_patch(group_box)

        # Gruppenavn
        ax.text(
            group_x + group_w / 2, task_y_base + task_h3 + 0.35,
            group["name"],
            ha="center", va="center",
            fontsize=6.5, color=group["color"],
            fontweight="bold",
            style="italic",
        )

        gcx = group_x + group_w / 2
        group_positions.append(gcx)
        draw_line(ax, f3_cx, phase_y, gcx, task_y_base + task_h3 + 0.55)

        # Oppgaver i gruppen
        for k, task_code in enumerate(group["tasks"]):
            task = f3_task_lookup[task_code]
            tx = group_x + k * (task_w3 + task_gap)
            is_milestone = "M2" in task["name"]
            color = group["color"] if not is_milestone else "#b5838d"
            cx, cy = draw_box(ax, tx, task_y_base, task_w3, task_h3,
                              f"{task['code']}\n{task['name']}", color, fontsize=5.5)

        current_x += group_w + group_gap

    # --- Nivå 2: Fase 4 oppgaver (2 rader: 4 + 3) ---
    fase4_tasks = wbs_data["phases"][2]["tasks"]
    f4_task_w, f4_task_h = 1.6, 0.55
    f4_y_row1 = 7.0
    f4_y_row2 = 6.2
    f4_start_x = 22.0
    f4_cx = phase_positions[2][0] + phase_positions[2][2] / 2
    cols_per_row = 4

    for j, task in enumerate(fase4_tasks):
        row = j // cols_per_row
        col = j % cols_per_row
        tx = f4_start_x + col * (f4_task_w + 0.15)
        ty = f4_y_row1 if row == 0 else f4_y_row2
        is_milestone = "M3" in task["code"]
        color = "#8a3054" if not is_milestone else "#b5838d"
        cx, cy = draw_box(ax, tx, ty, f4_task_w, f4_task_h,
                          f"{task['code']}\n{task['name']}", color, fontsize=6)
        draw_line(ax, f4_cx, phase_y, cx, f4_y_row1 + f4_task_h)

    # --- Tittel ---
    ax.text(
        15.5, 10.4,
        "WBS — LOG650 G22: Datadrevet vurdering av hyllekapasitet vs. etterspørsel",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color="#1a1a2e",
    )

    # --- Legende ---
    legend_y = 0.3
    legend_items = [
        ("#2d6a4f", "Fase 2 — Planlegging (ferdig)"),
        ("#1d3557", "Fase 3 — Gjennomføring (pågår)"),
        ("#6d2e46", "Fase 4 — Avslutning"),
        ("#b5838d", "Milepæl"),
    ]
    for i, (color, label) in enumerate(legend_items):
        lx = 10 + i * 4.5
        box = FancyBboxPatch(
            (lx, legend_y), 0.3, 0.25,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor="white", linewidth=0.5,
        )
        ax.add_patch(box)
        ax.text(lx + 0.45, legend_y + 0.12, label,
                fontsize=7, va="center", color="#333333")

    plt.tight_layout()
    output_path = "/Volumes/DevSSD/Projects/LOG650/G22-sfo/004 data/wbs_diagram.png"
    fig.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"WBS-diagram lagret: {output_path}")


if __name__ == "__main__":
    main()
