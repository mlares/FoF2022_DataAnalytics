import matplotlib.pyplot as plt

def set_style(argv):
    if 'vivid' in argv:
        plt.style.use('./colors_vivid.mplstyle')
    elif 'pastel' in argv:
        plt.style.use('./colors_pastel.mplstyle')
    elif 'favourite' in argv:
        plt.style.use('./colors_favourite.mplstyle')

    if 'web' in argv:
        plt.style.use('./sizes_web.mplstyle')
    elif 'papers' in argv:
        plt.style.use('./sizes_papers.mplstyle')
