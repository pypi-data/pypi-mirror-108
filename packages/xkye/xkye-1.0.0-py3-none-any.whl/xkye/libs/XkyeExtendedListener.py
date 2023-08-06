# pylint: disable-msg=C0103, R0912, R1714, duplicate-code

"""
Extended Listener class for Xkye Language
"""
import ipaddress

from .XkyeParser import XkyeParser
from .XkyeListener import XkyeListener


class XkyeExtendedListener(XkyeListener):

    """Class to extend the auto generated Xkye Listener class"""

    def __init__(self, out_dict):
        self.out_dict = out_dict
        self.span_list = []

    # Enter a parse tree produced by XkyeParser#clutch.
    def enterGlobe(self, ctx: XkyeParser.GlobeContext):
        self.out_dict["global"] = {}
        self.span_list.append(("global", "1"))

    # Enter a parse tree produced by XkyeParser#globalgroup.
    def enterGlobalgroup(self, ctx: XkyeParser.GlobalgroupContext):
        for child in ctx.children:
            child.parent_ctx = "global"
            child.clutch_Set = 1

    # Enter a parse tree produced by XkyeParser#clutchspan.
    def enterClutchspan(self, ctx: XkyeParser.ClutchspanContext):
        entity = ctx.entity().getText()

        set_list = []

        for i in self.span_list:
            set_list.append(i[0])

        if entity not in set_list:
            number = ctx.number().getText()
            span_pair = (entity, number)

            self.span_list.append(span_pair)
            self.out_dict[entity] = {}

        else:
            raise Exception(
                'Clutch span for "'
                + entity
                + '" is already declared, kindly check your input .xky file'
            )

    # Enter a parse tree produced by XkyeParser#pairgroup.
    def enterPairgroup(self, ctx: XkyeParser.PairgroupContext):
        for child in ctx.children:
            child.parent_ctx = ctx.parent_ctx
            child.clutch_Set = ctx.clutch_Set

    # Enter a parse tree produced by XkyeParser#pair.
    def enterPair(self, ctx: XkyeParser.PairContext):
        key = ctx.key().entity().getText()
        value = ctx.value().getText()

        if ctx.clutch_Set > 1:
            ctx.parent_ctx = ctx.parent_ctx + str(ctx.clutch_Set)

        key_list = list(self.out_dict[ctx.parent_ctx].keys())

        first = value[0]
        last = value[-1]

        if first == "'" and last == "'":
            value = value[1:-1]

        elif value == "TRUE" or value == "FALSE":
            value = bool(value)

        elif value.isdigit():
            value = int(value)

        elif value.replace(".", "", 1).isdigit():
            value = float(value)

        elif (value.replace(".", "").isdigit()) is False:
            value = ipaddress.ip_network(value, False)

        else:
            value = ipaddress.ip_address(value)

        if key not in key_list:
            self.out_dict[ctx.parent_ctx][key] = value
        else:
            raise Exception(
                "Entity "
                + key
                + " for "
                + ctx.parent_ctx
                + " is already declared, kindly check your input .xky file"
            )

    # Enter a parse tree produced by XkyeParser#pairgroupset.
    def enterPairgroupset(self, ctx: XkyeParser.PairgroupsetContext):

        if ctx.clutchdefheader() is not None:
            child_ctx = ctx.clutchdefheader().entity().getText()
            clutch_set = 1

        if ctx.clutchsetheader() is not None:
            child_ctx = ctx.clutchsetheader().entity().getText()
            clutch_set = int(ctx.clutchsetheader().number().getText())

        ctx.pairgroup().clutch_Set = clutch_set
        ctx.pairgroup().parent_ctx = child_ctx

    # Enter a parse tree produced by XkyeParser#clutchdefheader.
    def enterClutchdefheader(self, ctx: XkyeParser.ClutchdefheaderContext):
        entity = ctx.entity().getText()
        dict_list = list(self.out_dict.keys())

        if entity not in dict_list:
            number = "1"
            span_pair = (entity, number)

            self.span_list.append(span_pair)
            self.out_dict[entity] = {}

    # Enter a parse tree produced by XkyeParser#clutchsetheader.
    def enterClutchsetheader(self, ctx: XkyeParser.ClutchsetheaderContext):
        entity = ctx.entity().getText()
        clutch_set = int(ctx.number().getText())
        set_list = []

        entitystr = entity + str(clutch_set)

        for i in self.span_list:
            set_list.append(i[0])

        if entity in set_list:
            # Testing set count value
            index = set_list.index(entity)
            count = self.span_list[index][1]

            if int(clutch_set) > int(count):
                raise Exception(
                    'Clutch set for "'
                    + entity
                    + '" is exceeding declared span limit, kindly check your input .xky file'
                )

            # Adding in out_dict
            self.out_dict[entitystr] = {}

        else:
            raise Exception(
                'Clutch set for "'
                + entity
                + '" is not declared with span limit, kindly check your input .xky file'
            )

    # Enter a parse tree produced by XkyeParser#subclutchset.
    def enterSubclutchset(self, ctx: XkyeParser.SubclutchsetContext):
        if ctx.clutchdefheader() is not None:
            child_ctx = ctx.clutchdefheader().entity().getText()
            clutch_set = 1
        else:
            child_ctx = ctx.clutchsetheader().entity().getText()
            clutch_set = int(ctx.clutchsetheader().number().getText())

        ctx.subclutchgroup().clutch_Set = clutch_set
        ctx.subclutchgroup().parent_ctx = child_ctx

    # Enter a parse tree produced by XkyeParser#subclutchgroup.
    def enterSubclutchgroup(self, ctx: XkyeParser.SubclutchgroupContext):
        for child in ctx.children:
            child.parent_ctx = ctx.parent_ctx
            child.clutch_Set = ctx.clutch_Set

    # Enter a parse tree produced by XkyeParser#subclutch.
    def enterSubclutch(self, ctx: XkyeParser.SubclutchContext):
        subclutch = ctx.entity().getText()
        parent_ctx = ctx.parent_ctx
        parent_set = ctx.clutch_Set

        clutch_set = ""
        dict_suffix = ""

        if ctx.number() is not None:
            clutch_set = ctx.number().getText()
            dict_suffix = ctx.number().getText()
        else:
            clutch_set = "1"

        set_list = []
        set_count = []

        for i in self.span_list:
            set_list.append(i[0])
            set_count.append(i[1])

        if subclutch not in set_list:
            raise Exception(
                'Clutch set for "'
                + subclutch
                + '" is not defined, kindly check your input .xky file'
            )

        index_no = set_list.index(subclutch)

        if int(set_count[index_no]) < int(clutch_set):
            raise Exception(
                'Clutch set for "'
                + subclutch
                + '" is exceeding declared span limit, kindly check your input .xky file'
            )

        dict_key = subclutch + dict_suffix

        if parent_set < 2:
            parent_set = ""

        result_dict_key = parent_ctx + str(parent_set)

        tmp_dict_keys = list(self.out_dict[dict_key].keys())

        for key in tmp_dict_keys:
            self.out_dict[result_dict_key][key] = self.out_dict[dict_key][key]

    # Enter a parse tree produced by XkyeParser#outstring.
    def enterOutstring(self, ctx: XkyeParser.OutstringContext):
        entity = ctx.entity().getText()
        substr = ""
        subnumber = ""

        if ctx.outstringsubset() is not None:
            substr = ctx.outstringsubset().entity().getText()

            if ctx.outstringsubset().number() is not None:
                subnumber = ctx.outstringsubset().number().getText()

        if substr == "" and subnumber == "":

            dict_list = list(self.out_dict["global"].keys())

            if entity not in dict_list:
                raise Exception(
                    'Requested entity "'
                    + entity
                    + '" not declared above. kindly check your input .xky file'
                )

            result = self.out_dict["global"][entity]
            print(result)

        elif subnumber == "":

            dict_list = list(self.out_dict.keys())

            if substr not in dict_list:
                raise Exception(
                    'Requested clutch "'
                    + substr
                    + '" is not declared above. kindly check your input .xky file'
                )

            if entity not in list(self.out_dict[substr].keys()):
                raise Exception(
                    'Requested entity "'
                    + entity
                    + '" not declared above. kindly check your input .xky file'
                )

            result = self.out_dict[substr][entity]
            print(result)

        else:
            substrnew = substr + subnumber

            dict_list = list(self.out_dict.keys())

            if substrnew not in dict_list:
                if substr in dict_list:

                    if entity in list(self.out_dict[substr].keys()):
                        result = self.out_dict[substr][entity]
                        print(result)

                    else:
                        raise Exception(
                            'Requested entity "'
                            + entity
                            + '" not declared above. kindly check your input .xky file'
                        )

                else:
                    raise Exception(
                        'Requested clutch "'
                        + substr
                        + '" is not declared above. kindly check your input .xky file'
                    )

            else:
                if entity not in list(self.out_dict[substrnew].keys()):
                    if entity in list(self.out_dict[substr].keys()):
                        result = self.out_dict[substr][entity]
                        print(result)
                    else:
                        raise Exception(
                            'Requested entity "'
                            + entity
                            + '" not declared above. kindly check your input .xky file'
                        )

                else:
                    result = self.out_dict[substrnew][entity]
                    print(result)
