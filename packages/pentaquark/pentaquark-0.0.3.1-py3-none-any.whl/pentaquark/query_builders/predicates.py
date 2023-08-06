import enum
import string
import random

from pentaquark.constants import SEPARATOR, START_NODE_ALIAS
from pentaquark.exceptions import PentaQuarkConfigurationError
from pentaquark.lookups import LOOKUP_REGISTRY
from pentaquark.query_builders.pattern_builder import PatternBuilder


class LogicalOperators(enum.Enum):
    AND = "AND"
    OR = "OR"


def random_key(key_size):
    return "".join(random.sample(string.ascii_lowercase, key_size))


class AbsC:
    def __and__(self, other):
        return CompositeC(self, other, LogicalOperators.AND)

    def __or__(self, other):
        return CompositeC(self, other, LogicalOperators.OR)

    def compile(self, model, param_store, variables=None):
        raise NotImplementedError()


class CompositeC(AbsC):
    def __init__(self, c1, c2, operator):
        """
        :param c: a dict with a single first-level key (AND or OR).
        """
        op = LogicalOperators(operator)
        self._conditions = {
            op: [c1, c2]
        }

    def compile(self, model, param_store, variables=None):
        res = ""
        for k, cs in self._conditions.items():
            q = []
            op = k.name
            for c in cs:
                q.append(c.compile(model, param_store, variables))
            res += "(" + f" {op} ".join(q) + ")"
        return res


class C(AbsC):
    """
    Constructors:

        C(x__gt=1)  # C, Exists
        C(x, y)  # Label

    """
    def __init__(self, **kwargs):
        if len(kwargs) > 1:
            raise Exception("only one kwarg accepted in C init (received: %s)", kwargs)
        if len(kwargs) == 1:
            self.variable, self.value = next(iter(kwargs.items()))
            if not self.variable.startswith(START_NODE_ALIAS):
                self.variable = START_NODE_ALIAS + SEPARATOR + self.variable

    def compile(self, model, param_store, variables=None):
        return self.to_cypher(model, param_store, variables)

    # C(x__y__gt=1) => variable=x, field=y, lookup='>', value=1
    def _to_cypher(self, lhs, lookup, value, param_store, variables=None):
        key = random_key(key_size=5)
        param_name = param_store.add(key, value)
        return f"{lhs} {lookup} ${param_name}"

    def to_cypher(self, model, param_store, variables=None):
        if SEPARATOR not in self.variable:
            if variables is not None and self.variable not in variables:
                raise Exception(f"Can not filter on {self.variable} not in scope {variables}")
            return self._to_cypher(self.variable, "=", self.value, param_store)
        var, prop = self.variable.rsplit(SEPARATOR, 1)
        if prop in LOOKUP_REGISTRY:
            lookup = LOOKUP_REGISTRY[prop].cypher_expr
            if SEPARATOR in var:
                var, prop = var.rsplit(SEPARATOR, 1)
            else:
                prop = var
                var = "this"
        else:
            lookup = "="
        if variables is not None and var not in variables:
            raise Exception(f"Can not filter on {var} not in scope {variables}")
        return self._to_cypher(f"{var}.{prop}", lookup, self.value, param_store)


class Label(C):
    # Label("this", "Movie")
    # value=Movie, variable=this
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        if not self.variable.startswith(START_NODE_ALIAS):
            self.variable = START_NODE_ALIAS + SEPARATOR + self.variable
        super().__init__()

    def to_cypher(self, model, param_store, variables=None):
        if variables and self.variable not in variables:
            raise Exception(f"Can not filter on {self.variable} not in scope {variables}")
        key = random_key(key_size=5)
        param_name = param_store.add(key, self.value)
        return f"${param_name} IN labels({self.variable})"


# class Exists(C):
#     # Exist(this__actors__name="test")
#     # variable=this__actors,
#     def __init__(self, *args, **kwargs):
#         self.variable = args[0] if args else None
#         if self.variable and not self.variable.startswith(START_NODE_ALIAS):
#             self.variable = START_NODE_ALIAS + SEPARATOR + self.variable
#         super().__init__()
#
#     def to_cypher(self, param_store, variables=None):
#         if variables and self.variable not in variables:
#             raise Exception(f"Can not filter on {self.variable} not in scope {variables}")
#         return f"EXISTS({self.variable})"
#

class Exists(C):
    """
    "EXISTS" Cypher predicate function, with pattern argument
    TODO: support for pattern without attributes, ie we need to be able to build the pattern from a string:
        eg: "movies__director" or "attribute_instance__attribute"
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        q = None
        if args and kwargs:
            raise PentaQuarkConfigurationError("Exists predicate only understand either args or kwargs")
        if args:
            if len(args) > 1:
                raise PentaQuarkConfigurationError(
                    "Exists predicate only understand one single argument. "
                    "Use several Exists if several conditions are required."
                )
            q = args[0]
        elif kwargs:
            q = kwargs
        self._queries = q

    def _get_pattern(self, model, param_store, variables):
        pb = PatternBuilder(
            model=model, param_store=param_store,
            variables_in_external_scope=variables,
            append_to_global_scope=False
        )
        return pb.build(data=self._queries, include_alias=False, include_label=True)

    def to_cypher(self, model, param_store, variables=None):
        pattern = self._get_pattern(model, param_store, variables)
        return f"EXISTS({pattern})"
