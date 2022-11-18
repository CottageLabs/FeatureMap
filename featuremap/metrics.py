def completion_metric(annotations, total_lines):
    """
    A metric to determine how "complete" the annotation of a file is, with 1 being a file
    that is ONLY annotations, and 0 being a file with none, and all other files somewhere
    in between.  Note that no file, except extremely unusual annotation-only files, will
    ever score 1, most of them will score very low indeed, and that is correct.
    :param annotations:
    :param total_lines:
    :return:
    """
    if total_lines == 0:
        return 1.0
    if annotations == 0:
        return 0.0
    return annotations / total_lines