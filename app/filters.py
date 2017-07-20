def superwordwrap(text,  width=79, break_long_words=True):
    """
       Return a copy of the string passed to the filter wrapped after
       ``79`` characters.  You can override this default using the first
       parameter.  If you set the second parameter to `false` Jinja will not
       split words apart if they are longer than `width`.
       """
    import textwrap, re
    accumulator = []
    for component in re.split(r"\r?\n", text):
        # textwrap will eat empty strings for breakfirst. Therefore we route them around it.
        if len(component) is 0:
            accumulator.append(component)
            continue
        accumulator.extend(
            textwrap.wrap(component, width=width, expand_tabs=False,
                          replace_whitespace=False,
                          break_long_words=break_long_words)
        )
    return accumulator[0]
