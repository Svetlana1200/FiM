from symbolAndCommand import TOKEN_TYPES

class Const:
    SHOULD_IGNORE = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "
            ]
    SHOULD_REPLACE = [
            " was ", " is ", " has ",
            " had ", " like ", " likes ", " liked "]
    COMPARATORS = [
            ' no less than ', ' no more than ', ' no greater than ',
            ' not more ', ' not greater ', ' not less ',
            ' more than ', ' greater than ', ' less than ', ' not ',
            ]
    OPERATIONS_STR = [
            " plus ", " added to ", ' minus ',
            " without ", ' times ', ' multiplied with ',
            ' divided by ']
    DICT_REPLACE = {
        TOKEN_TYPES.PLUS: [" to ", " and "],
        TOKEN_TYPES.MINUS: [" from ", " and "],
        TOKEN_TYPES.MULTIPLY: [" and "],
        TOKEN_TYPES.DIVIDE: [" by ", " and "]
    }

    SHOULD_FIND_TYPE = ["the number", "the word"]

    CHECK_IF_CONDITION_DICT = {
        TOKEN_TYPES.MORE: lambda x, y: x > y,
        TOKEN_TYPES.LESS: lambda x, y: x < y,
        TOKEN_TYPES.EQLESS: lambda x, y: x <= y,
        TOKEN_TYPES.EQMORE: lambda x, y: x >= y,
        TOKEN_TYPES.EQUALS: lambda x, y: x == y,
        TOKEN_TYPES.NOTEQ: lambda x, y: x != y
    }

    OPERATION = {
        TOKEN_TYPES.PLUS: "+",
        TOKEN_TYPES.MINUS: "-",
        TOKEN_TYPES.MULTIPLY: "*",
        TOKEN_TYPES.DIVIDE: "/",
        TOKEN_TYPES.MORE: '>',
        TOKEN_TYPES.LESS: '<',
        TOKEN_TYPES.EQLESS: '<=',
        TOKEN_TYPES.EQMORE: ">=",
        TOKEN_TYPES.EQUALS: "==",
        TOKEN_TYPES.NOTEQ: "!="
    }
