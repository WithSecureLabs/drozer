class TableFormatter(object):
    """
    Utility methods for formatting tabular data.
    """

    def print_table(self, rows, show_headers=True, vertical=False):
        """
        Print tabular data to stdout, given an array of rows, each containing
        an array of values.

        It is assumed that the first row contains column headers.
        """

        if vertical:
            self.print_table_vertical(rows)
        else:
            self.print_table_horizontal(rows, show_headers)

    def print_table_horizontal(self, rows, show_headers=True):
        """
        Print tabular data in a traditional, horizontal format:

        | a | b | c |
        | 1 | 2 | 3 |
        """

        widths = []

        if show_headers:
            self.stdout.write("|")

        for i in xrange(len(rows[0])):
            widths.append(max(map(lambda r: len(str(r[i])), rows)))

            if show_headers:
                self.stdout.write((" {:<" + str(widths[i]) + "} |").format(rows[0][i]))
        self.stdout.write("\n")

        for r in rows[1:]:
            self.stdout.write("|")
            for i in xrange(len(r)):
                self.stdout.write((" {:<" + str(widths[i]) + "} |").format(r[i]))
            self.stdout.write("\n")
        self.stdout.write("\n")

    def print_table_vertical(self, rows):
        """
        Print tabular data in a vertical format, which is easier to read with
        long fields names or values:

        a: 1
        b: 2
        c: 3
        """

        headers = rows.pop(0)

        width = max(map(lambda e: len(str(e)), headers))

        for row in rows:
            for i in xrange(len(headers)):
                self.stdout.write(("{:>" + str(width) + "}  {}\n").format(headers[i], row[i]))
            self.stdout.write("\n")
        self.stdout.write("\n")
