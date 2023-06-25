import numpy as np
import matplotlib.pyplot as plt

with open ("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")]

datarr = np.loadtxt ("data.txt", dtype=int)
datarr = datarr * tmp[0]
timarr = np.linspace (0, tmp[1] * datarr.size, datarr.size)

dathi = float(datarr.max()) + 0.5 - float(datarr.max()) % 0.5
datlo = float(datarr.min()) - float(datarr.min()) % 0.5
timhi = float(timarr.max()) + 1 - float(timarr.max()) % 1
timlo = float(timarr.min()) - float(timarr.min()) % 1

charge_time = tmp[1] * datarr.argmax()
discharge_time = tmp[1] * (datarr.size - datarr.argmax())

fig, ax = plt.subplots (figsize=(16, 10), dpi=400)
ax.plot (timarr, datarr, "-k", marker='+', markersize=12, linewidth=1, markevery=30, markeredgecolor="r", markeredgewidth=1, label="U(t)", scalex=False, scaley=False)
ax.set_ylabel ("Напряжение, В", fontsize=12)
ax.set_xlabel ("Время, с", fontsize=12)
ax.set_title ("Процесс зарядки и разрядки конденсатора в RC-цепи", fontsize=16, loc='center', pad=16, wrap=True)
ax.grid (which="major", linestyle="-", linewidth=0.8, color="k", alpha=0.4)
ax.grid (which="minor", linestyle="--", linewidth=0.5, color='y')
ax.set_xlim (timlo, timhi)
ax.set_ylim (datlo, dathi)
ax.minorticks_on ()
ax.legend ()
ax.text (0.6 * timarr.max(), 0.7 * datarr.max(), s=f"Полная длительность эксперимента: {(charge_time + discharge_time):.2f} с.\n\nДлительность зарядки: {charge_time:.2f} с.\n\nДлительность разрядки: {discharge_time:.2f} с.", fontsize=12)

fig.savefig ("text.png")
