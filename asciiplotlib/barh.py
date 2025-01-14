import sys


def _trim_trailing_zeros(lst):
    k = 0
    for item in lst[::-1]:
        if item != 0:
            break
        k += 1
    return lst[:-k] if k > 0 else lst


def barh(
    counts, labels=None, max_width=40, bar_width=1, show_counts=True, force_ascii=False
):
    matrix = _get_matrix_of_eighths(counts, max_width, bar_width)

    if (
        hasattr(sys.stdout, "encoding")
        and sys.stdout.encoding in ["utf-8", "UTF-8", "UTF8"]
        and not force_ascii
    ):
        chars = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    else:
        chars = [" ", "*", "*", "*", "*", "*", "*", "*", "*"]

    fmt = []
    if labels:
        cfmt = "{{:{}s}}".format(max([len(str(label)) for label in labels]))
        fmt.append(cfmt)

    if show_counts:
        cfmt = "{{:{}d}}".format(max([len(str(c)) for c in counts]))
        fmt.append("[" + cfmt + "]")

    fmt.append("{}")
    fmt = "  ".join(fmt)

    out = []
    for k, (counts, row) in enumerate(zip(counts, matrix)):
        data = []
        if labels:
            data.append(labels[k])
        if show_counts:
            data.append(counts)

        # Cut off trailing zeros
        r = _trim_trailing_zeros(row)
        data.append("".join(chars[item] for item in r))
        out.append(fmt.format(*data))

    return out


def _get_matrix_of_eighths(counts, max_size, bar_width):
    max_count = max(counts)

    # translate to eighths of a textbox
    eighths = [int(round(count / max_count * max_size * 8)) for count in counts]

    # prepare matrix
    matrix = [[0] * max_size for _ in range(len(eighths))]
    for i, eighth in enumerate(eighths):
        num_full_blocks = eighth // 8
        remainder = eighth % 8
        for j in range(num_full_blocks):
            matrix[i][j] = 8
        if remainder > 0:
            matrix[i][num_full_blocks] = remainder

    # Account for bar width
    out = []
    for i in range(len(matrix)):
        for _ in range(bar_width):
            out.append(matrix[i])
    return out
