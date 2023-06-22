import matplotlib.pyplot as plt
import numpy as np

ar = np.random.rand(15)

cuts = ["V", "H", "H", "V"]

fig10 = plt.figure(tight_layout=True)
gs0 = fig10.add_gridspec(1, 1)

current_spec = gs0[0].subgridspec(1, 1)

for cut in cuts:
    print(cut)
    if cut == "V":
        new_spec = current_spec[0].subgridspec(2, 1, height_ratios=[2, 1])
    if cut == "H":
        new_spec = current_spec[0].subgridspec(1, 2, width_ratios=[2, 1])

    if max(current_spec.nrows, current_spec.ncols) > 1:
        ax_i = fig10.add_subplot(current_spec[1])

        ax_i.plot(ar)
    current_spec = new_spec

for i in current_spec:
    print(fig10.add_subplot(i))

plt.show()