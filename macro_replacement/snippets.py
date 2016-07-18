#Provides uncompiled regex "snippets" useful in processing LaTeX

from collections import defaultdict

whitespace = r'(?: |\\quad|\\qquad|\\!|\\,|\\t|\\n|\\:|\\;|\\\s|)'               #regex for matching whitespace
valid = r'(?:[^=s,;|])'                                                    #regex for matching valid characters within another element
open_paren = r'(?:\\left|\\Bigg|\\bigg|\\big|\\Big|\\bigl)'         #regex for matching opening parentheses
close_paren = r'(?:\\right|\\Bigg|\\bigg|\\big|\\Big|\\bigr)'       #regex for matching closing parentheses

_frequencies = defaultdict(int)

#matches a subscript where entire contents can be grouped
def subscript(num_args=1):

    pattern = r'_(?P<_' + str(_frequencies["subscript"]) + '_sub_open>{)?'
    pattern += _create_named_groups(_create_group_names(_frequencies["subscript"], "sub", end=num_args))
    pattern += r'(?(_' + str(_frequencies["subscript"]) + '_sub_open)})'

    _frequencies["subscript"] += 1

    return pattern

#matches a superscript with num_args comma-delimited arguments
def superscript(num_args=1):

    pattern = r'\^(?P<_' + str(_frequencies["superscript"]) + r'_sup_open>{)?'
    pattern +=  r'(?:' + _create_named_groups(_create_group_names(_frequencies["superscript"], "sup", end=num_args)) + r'|' + simple_arg_list(num_args) + r')'
    pattern += r'(?_' + str(_frequencies["superscript"]) + r'_sup_open)})'

    _frequencies["superscript"] += 1

    return pattern


#matches a simple argument list (no ; or |)
def simple_arg_list(num_args=1, all_paren=False):
   
    o_paren = open_paren
    c_paren = close_paren
    if not all_paren:
        o_paren = r'\('
        c_paren = r'\)'

    pattern = o_paren
    pattern += _create_named_groups(_create_group_names(_frequencies["simple_arg_list"], "arg", end=num_args))
    pattern += c_paren

    _frequencies["simple_arg_list"] += 1

    return pattern

#matches argument lists with elements delimited by , | and ;
#parameters ending in _ex signify exclusivity (i.e. semi_first_ex means a ; ONLY comes after the first argument)
def semi_bar_arg_list(num_args, all_paren=False, semi_first_ex=False, semi_first=False, semi_last=False, semi_last_ex=False, num_groups=1, group_size=2, bar_first=False, bar_last=False):
 
    o_paren = open_paren + r'?\('
    c_paren = close_paren + r'?\)'
    if not all_paren:
        o_paren = r'\('
        c_paren = r'\)'

    #make sure that semi_first is set if semi_first_ex is set
    if semi_first_ex:
        semi_first = True

    if semi_last_ex:
        semi_last = True

    #ensure ; and | are not both first or last
    if (semi_first and bar_first) or (semi_last and bar_last):
        raise ValueError("semicolon and bar cannot be in the same place")


    pattern = o_paren

    start_loc = 0

    #; or | is going at the front or end
    if any([semi_first, semi_last, bar_first, bar_last]):

        if bar_first:       #bar is after first argument ONLY

            pattern += _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", end=1)) + r'\|' + _whitespace + r'*'  
            start_loc += 1


        elif semi_first:    #semicolon is after first argument
           
           pattern += _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", end=1)) + r';' + _whitespace + r'*'  
           start_loc += 1

           if semi_first_ex:#semicolon is ONLY after first argument
               pattern += _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=start_loc, end=num_args-1))
               start_loc = num_args - 1

    #semicolon is ONLY before last argument
    if semi_last_ex:
        
        pattern += _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=start_loc, end=num_args-1))

    #unecessary if only first or last has ;
    if not (semi_first_ex or semi_last_ex):

        expected = num_args - start_loc

        #figure out how many items there are to be grouped
        if semi_last or bar_last:
            expected -= 1    

        #ensure that the number of groups, size of each one, and the number of arguments all make sense
        if num_groups * group_size != expected:
            raise ValueError("{0} * {1} != {2}".format(num_groups, group_size, expected))


        #go through however many ;-separated groups there are
        for group in range(num_groups):

            pattern += _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=start_loc, end=start_loc+group_size))
            pattern += _whitespace + r'*;'

            start_loc += group_size

    pattern = pattern[:-1]

    #remove trailing ; if something comes after
    if semi_last or bar_last:
        if semi_last:       #semicolon is before last argument

            pattern += _whitespace + r'*;' + _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=num_args-1, end=num_args)) + r')'

        elif bar_last:      #bar is before last argument

            pattern += _whitespace + r'*\|' + _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=num_args-1, end=num_args)) + r')'

    else:                   #list ends normally
    
        pattern += r'),' + _create_named_groups(_create_group_names(_frequencies["semi_bar_arg_list"], "arg", start=start_loc, end=num_args))

    pattern += c_paren

    _frequencies["semi_bar_arg_list"] += 1

    return pattern

#creates a list of numbered group names to use in _create_named_groups
def _create_group_names(index_num, name, start=0, end=1):

    groups = []

    for i in range(start + 1, end + 1):
        groups.append("_{0}_{1}_{2}".format(index_num, name, i))

    return groups

#creates a pattern that matches function arguments as named groups
def _create_named_groups(*groups):

    pattern_string = ""

    for group in groups[0]:
        pattern_string += r'{whitespace}*(?P<{group}>{valid}+),'.format(whitespace=_whitespace, group=group, valid=valid)


    return pattern_string[:-1]


#returns the number of times a given function has been called
def get_freq(name):
    return _frequencies[name]

def main():
    
    print("")
    print(r'R' + subscript() + semi_bar_arg_list(5,semi_first_ex=True, bar_last=True, all_paren=True))
    print("")
    print("")
if __name__ == "__main__":
    main()
