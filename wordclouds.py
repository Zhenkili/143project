
class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


def generate_word_cloud_colors(df):
    ls = df['Colors'].to_list()
    w_ls = ''
    c_dict = {}
    for l in ls:
        l = l.replace('(', '').replace(')', '').split(',')
        for c in l:
            c = c.replace('\'', '').replace(' ', '')
            w_ls += " " + c
            if c not in c_dict:
                c_dict[c] = 0
            c_dict[c] += 1
    wc = WordCloud(max_font_size=100, max_words=20, background_color="white", collocations=False).generate(w_ls)
    color_to_words = {
        # words below will be colored with a green single color function
        # will be colored with a red single color function
        '#A9A9A9': ['Gray'],
        '#D2B48C' : ['Tan'],
        '#A0522D' : ['Sienna'],
        '#43302e' : ['OldBurgundy'],
        '#c19a6b' : ['Camel'],
        '#6f4e37' : ['Coffee'],
        '#fffacd' : ['LemonChiffon'],
        '#faebd7' : ['AntiqueWhite'],
        '#deb887' : ['Burlywood'],
        '#664228' : ['VanDyke'],
        '#FFFFF0' : ['Ivory'],
        '#3d2b1f' : ['Bistre'],
        '#856d4d' : ['FrenchBistre'],
        '#a99a86' : ['Grullo'],
        '#c8ad7f' : ['FrenchBeige'],
        '#f5deb3' : ['Wheat'],
        '#F2D2BD' : ['Bisque'],
        '#fff8dc' : ['Cornsilk'],
        '#dbd7d2' : ['Timberwolf'],
        '#100c08' : ['SmokyBlack'],
        '#ffffe0' : ['LightYellow']
    }
    default_color = '#f5deb3'

    # Create a color function with multiple tones
    grouped_color_func = GroupedColorFunc(color_to_words, default_color)

    # Apply our color function
    wc.recolor(color_func=grouped_color_func)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('WordCloud.png')
    plt.show()

def generate_word_cloud_genre(df):
    g_ls = ""
    g_dict = {}
    for g in df['Genre']:
        if g not in g_dict:
            g_dict[g] = 0
        g_dict[g] += 1
        g = g.replace(' ', '')
        g_ls += " " + g

    wc = WordCloud(max_font_size=100, max_words=10, background_color="white", collocations=False).generate(g_ls)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('Genre.png')
    plt.show()
    


