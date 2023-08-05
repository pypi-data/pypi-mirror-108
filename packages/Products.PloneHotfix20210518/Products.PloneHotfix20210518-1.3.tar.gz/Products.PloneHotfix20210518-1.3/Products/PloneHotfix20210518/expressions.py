from Products.PageTemplates import Expressions
from zExceptions import NotFound


# Set of names that start with an underscore but that we want to allow anyway.
ALLOWED_UNDERSCORE_NAMES = set([
    # dunder name is used in plone.app.caching, and maybe other places
    "__name__",
    # Zope allows a single underscore to avoid a test failure
    "_",
    # Special case for plone.protect.
    # Fixes a NotFound error when submitting a PloneFormGen form:
    # https://github.com/smcmahon/Products.PloneFormGen/pull/229
    "_authenticator",
])

_orig_boboAwareZopeTraverse = Expressions.boboAwareZopeTraverse


def boboAwareZopeTraverse(object, path_items, econtext):
    """Traverses a sequence of names, first trying attributes then items.

    This uses zope.traversing path traversal where possible and interacts
    correctly with objects providing OFS.interface.ITraversable when
    necessary (bobo-awareness).

    Our change: disallow any item starting with an underscore.
    """
    for name in list(path_items):
        if name in ALLOWED_UNDERSCORE_NAMES:
            continue
        if name.startswith("_"):
            raise NotFound(name)
    return _orig_boboAwareZopeTraverse(object, path_items, econtext)


Expressions.boboAwareZopeTraverse = boboAwareZopeTraverse
Expressions.ZopePathExpr._TRAVERSER = staticmethod(boboAwareZopeTraverse)

# But wait, in Zope 2 you can use five.pt,
# which has a BoboAwareZopeTraverse class.
# And in early Zope 4, the same is true for Products.PageTemplates
# You either have one or both.
try:
    from Products.PageTemplates.expression import BoboAwareZopeTraverse
    from Products.PageTemplates.expression import TrustedBoboAwareZopeTraverse
except ImportError:
    try:
        from five.pt.expressions import BoboAwareZopeTraverse
        from five.pt.expressions import TrustedBoboAwareZopeTraverse
    except ImportError:
        BoboAwareZopeTraverse = None
        TrustedBoboAwareZopeTraverse = None

if BoboAwareZopeTraverse is not None:
    # We do not want to change the trusted version.  It inherits the traverse method
    # from the untrusted class.  It may be better to give it its own method.
    # The @classmethod makes this tricky to get right.
    # But the following line essentially makes a copy of the traverse method
    # without needing inheritance anymore.
    TrustedBoboAwareZopeTraverse.traverse = TrustedBoboAwareZopeTraverse.traverse

    BoboAwareZopeTraverse._orig_traverse = BoboAwareZopeTraverse.traverse

    def traverse(cls, base, request, path_items):
        """See ``zope.app.pagetemplate.engine``."""
        if cls.traverse_method == "restrictedTraverse":
            for name in list(path_items):
                if name in ALLOWED_UNDERSCORE_NAMES:
                    continue
                if name.startswith("_"):
                    raise NotFound(name)
        return cls._orig_traverse(base, request, path_items)

    BoboAwareZopeTraverse.traverse = classmethod(traverse)

if TrustedBoboAwareZopeTraverse is not None:
    # This is the class from Zope 4.
    # This and the (untrusted) BoboAwareZopeTraverse class have a problem:
    # They have a "traverse_method" attribute, but the "traverse" method
    # calls "cls.traverseMethod" instead, so this fails.
    # This may mean these classes do not get called anymore, except in my tests.
    name1 = "traverse_method"
    name2 = "traverseMethod"
    # First do the trusted class, because it inherits from the untrusted class.
    # Otherwise the trusted class would have traverse_method=unrestrictedTraverse
    # and it would inherit traverseMethod=restrictedTraverse.
    for klass in (TrustedBoboAwareZopeTraverse, BoboAwareZopeTraverse):
        if hasattr(klass, name1) and not hasattr(klass, name2):
            setattr(klass, name2, getattr(klass, name1))
