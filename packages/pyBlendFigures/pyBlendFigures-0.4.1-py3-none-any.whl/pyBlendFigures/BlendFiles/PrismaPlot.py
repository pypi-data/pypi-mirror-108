from blendSupports.Meshs.text import make_text


from miscSupports import load_yaml


class PrismaPlot:
    def __init__(self):
        self._args = load_yaml(r"C:\Users\Samuel\PycharmProjects\pyBlendFigures\TestV2\PRISMA\Test.yaml")

        self.spacing = 1

        self.links = self._args["Links"]
        self.positions = self._args["Positions"]
        self.col_count = len(self.links["Columns"])
        self.row_count = len(self.links["Rows"])

        self.dimensions = self._set_dimensions()
        print(self.dimensions)

        # TODO: This won't work, we need to know the values of x and y for both columns before we start

        for i in range(self.col_count):
            previous_height = 0
            if i == 0:
                row_adjustment = 0
            else:
                row_adjustment = self.dimensions[str(i - 1)]

            for row_i in range(self.row_count):

                for name, position in self.positions.items():
                    col_id, row_id = name.split("-")
                    if col_id == str(i) and row_id == str(row_i):

                        make_text(name, i + row_adjustment, (-row_i - previous_height), position["Text"], 1, (255, 255, 255, 255), align="CENTER")
                        previous_height += (len(position["Text"].split("\n")) + self.spacing)

            print("")

    def _set_dimensions(self):

        widths = {}
        for i in range(self.col_count):
            col_widths = []
            for name, position in self.positions.items():

                col_id, row_id = name.split("-")
                if col_id == str(i):
                    # Isolate the text, and append the number of lines, as well as the maximum length of the line to
                    # their respective lists
                    text_split = position["Text"].split("\n")
                    col_widths.append(max([len(text) for text in text_split]))

            widths[str(i)] = int(max(col_widths) / 2) + 1

        return widths


# col_heights.append([name, len(text_split)])


#

PrismaPlot()