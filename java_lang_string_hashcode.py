def java_lang_string_hashcode(string):
    h = 0
    for c in string:
        h = h * 31 + ord(c) # java integer overflow
    return h
