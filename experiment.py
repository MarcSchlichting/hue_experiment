import numpy as np
import matplotlib.pyplot as plt
from colormath.color_objects import sRGBColor, HSLColor
from colormath.color_conversions import convert_color
import itertools
import pickle

def patch_asscalar(a):
    return a.item()

setattr(np, "asscalar", patch_asscalar)

# generate sample data
n_points = 201
x = np.linspace(0,10,n_points)
y1 = np.exp(-x) + 0.05 * np.random.randn(n_points)
y2 = 2/(1+np.exp(x-3))  + 0.05 * np.random.randn(n_points)


colors = []
hue_values = []
choices = []
hues = np.arange(0,360,30)+15
# combinations_c1_c2 = list(itertools.combinations(hues,2))
combinations_c1_c2 = itertools.combinations(hues,2)
combinations_all = list(itertools.product(hues,combinations_c1_c2))
combinations_all = [(c[0],c[1][0],c[1][1]) for c in combinations_all if ((c[0]!=c[1][0]) and (c[0]!=c[1][1]))]
sat = 0.7
light = 0.5
for i, (anch_hue,col1_hue,col2_hue) in enumerate(combinations_all):
    anchor = convert_color(HSLColor(anch_hue,sat,light),sRGBColor).get_value_tuple()
    c1 = convert_color(HSLColor(col1_hue,sat,light),sRGBColor).get_value_tuple()
    c2 = convert_color(HSLColor(col2_hue,sat,light),sRGBColor).get_value_tuple()

    fig,axs = plt.subplots(1,2,figsize = (8,3))
    axs[0].plot(x,y1,c=anchor)
    axs[0].plot(x,y2,c=c1)
    axs[0].set_xticks([])
    axs[0].set_yticks([])
    axs[0].set_title("A")
    axs[1].plot(x,y1,c=anchor)
    axs[1].plot(x,y2,c=c2)
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_title("B")
    fig.suptitle(f"{len(colors)}")
    fig.tight_layout()
    # fig.savefig(f"candidate_colors_hsl/{len(colors)}.pdf")
    # print(i)
    plt.show(block=False)
    invalid_answer = True
    while invalid_answer:
        decision = input(f"{i+1}/{len(combinations_all)}: Do you prefer A or B? ")
        if decision in ["A","B"]:
            invalid_answer = False

            #save current progress
            np.save(f"results/colors_exp.npy",colors)
            np.save(f"results/hues_exp.npy",colors)
            with open(f"results/choices_exp.pkl","wb") as f:
                pickle.dump(choices,f)
        else:
            print("Answer must be A or B!")
    # decision = random.choice(["A","B"])
    plt.close()
    # plt.clf()


    colors.append((anchor,c1,c2))
    hue_values.append((anch_hue,col1_hue,col2_hue))
    choices.append(decision)
    # print(len(colors))

colors = np.stack(colors)
hues_values = np.stack(hue_values)

np.save(f"results/colors_exp.npy",colors)
np.save(f"results/hues_exp.npy",colors)
with open(f"results/choices_exp.pkl","wb") as f:
    pickle.dump(choices,f)
# print(choices)
print("Thank you for your participation!")
        




# plt.show()