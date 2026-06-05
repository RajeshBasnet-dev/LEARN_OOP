"""Individual AST checks used by the OOP evaluator."""
import ast

from .engine import CheckResult


IGNORED_PUBLIC_ATTRS = {"args", "kwargs"}


def _class_nodes(tree):
    """Yield all class definitions in an AST."""
    return (node for node in ast.walk(tree) if isinstance(node, ast.ClassDef))


def _find_class(tree, class_name):
    """Return the class definition matching class_name, or None."""
    return next((node for node in _class_nodes(tree) if node.name == class_name), None)


def _base_name(base):
    """Return a readable base class name from a class definition base node."""
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    if isinstance(base, ast.Subscript):
        return _base_name(base.value)
    return None


def _method_node(class_node, method_name):
    """Return a function node defined directly inside a class."""
    if class_node is None:
        return None
    return next(
        (
            node
            for node in class_node.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == method_name
        ),
        None,
    )


def _decorator_name(decorator):
    """Return a decorator name from an AST decorator node."""
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        return decorator.attr
    if isinstance(decorator, ast.Call):
        return _decorator_name(decorator.func)
    return None


def check_class_exists(tree, class_name) -> CheckResult:
    """Verify class is defined: class Employee:"""
    found = _find_class(tree, class_name) is not None
    if found:
        return CheckResult(
            "has_class",
            True,
            "pass",
            f"✅ Great! {class_name} is defined as a class.",
        )
    return CheckResult(
        "has_class",
        False,
        "fail",
        f"❌ Missing: define a class named {class_name}.",
    )


def check_inheritance(tree, child_class, parent_class) -> CheckResult:
    """Verify class A(B) inheritance syntax is present."""
    child = _find_class(tree, child_class)
    if child is None:
        return CheckResult(
            "has_inheritance",
            False,
            "fail",
            f"❌ Missing: define {child_class} before checking inheritance.",
        )

    base_names = {_base_name(base) for base in child.bases}
    if parent_class in base_names:
        return CheckResult(
            "has_inheritance",
            True,
            "pass",
            f"✅ Great! {child_class} correctly inherits from {parent_class}.",
        )
    return CheckResult(
        "has_inheritance",
        False,
        "fail",
        f"❌ Missing: {child_class} must inherit from {parent_class}.",
    )


def check_method_exists(tree, class_name, method_name) -> CheckResult:
    """Verify method exists in the specified class."""
    class_node = _find_class(tree, class_name)
    if class_node is None:
        return CheckResult(
            "has_method",
            False,
            "fail",
            f"❌ Missing: define {class_name} before adding {method_name}().",
        )

    if _method_node(class_node, method_name):
        return CheckResult(
            "has_method",
            True,
            "pass",
            f"✅ Great! {class_name}.{method_name}() is defined.",
        )
    return CheckResult(
        "has_method",
        False,
        "fail",
        f"❌ Missing: add {method_name}() to {class_name}.",
    )


def check_method_override(tree, child_class, parent_class, method_name) -> CheckResult:
    """Verify method is redefined in a child class that inherits from a parent."""
    inheritance = check_inheritance(tree, child_class, parent_class)
    if not inheritance.passed:
        return CheckResult(
            "method_override",
            False,
            "fail",
            f"❌ Missing: {child_class} must inherit from {parent_class} before overriding {method_name}().",
        )

    child = _find_class(tree, child_class)
    parent = _find_class(tree, parent_class)
    child_method = _method_node(child, method_name)
    parent_method = _method_node(parent, method_name)

    if child_method and (parent_method or parent is None):
        return CheckResult(
            "method_override",
            True,
            "pass",
            f"✅ Great! {child_class} overrides {method_name}() from {parent_class}.",
        )
    return CheckResult(
        "method_override",
        False,
        "fail",
        f"❌ Missing: {child_class} must override '{method_name}' from {parent_class}.",
    )


def check_encapsulation(tree, class_name) -> CheckResult:
    """Warn if instance attributes lack an underscore prefix."""
    class_node = _find_class(tree, class_name)
    if class_node is None:
        return CheckResult(
            "encapsulation",
            False,
            "fail",
            f"❌ Missing: define {class_name} before checking encapsulation.",
        )

    public_attrs = set()
    private_attrs = set()
    for node in ast.walk(class_node):
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            if isinstance(node.value, ast.Name) and node.value.id == "self":
                if node.attr.startswith("_"):
                    private_attrs.add(node.attr)
                elif node.attr not in IGNORED_PUBLIC_ATTRS:
                    public_attrs.add(node.attr)

    if public_attrs:
        attr_list = ", ".join(sorted(public_attrs))
        return CheckResult(
            "encapsulation",
            False,
            "warning",
            f"⚠️ {attr_list} is publicly accessible — consider underscore-prefixed attributes with @property getters.",
        )
    if private_attrs:
        return CheckResult(
            "encapsulation",
            True,
            "pass",
            f"✅ Great! {class_name} uses underscore-prefixed attributes for encapsulation.",
        )
    return CheckResult(
        "encapsulation",
        False,
        "warning",
        f"⚠️ No instance attributes found in {class_name}; use self._name style fields when storing state.",
    )


def check_dunder_init(tree, class_name) -> CheckResult:
    """Verify __init__ is defined in the class."""
    class_node = _find_class(tree, class_name)
    if _method_node(class_node, "__init__"):
        return CheckResult(
            "dunder_init",
            True,
            "pass",
            f"✅ Great! {class_name} defines __init__().",
        )
    return CheckResult(
        "dunder_init",
        False,
        "fail",
        f"❌ Missing: add __init__() to {class_name}.",
    )


def check_super_call(tree, class_name, method_name) -> CheckResult:
    """Detect a super().method_name() call inside the named method."""
    class_node = _find_class(tree, class_name)
    method = _method_node(class_node, method_name)
    if method is None:
        return CheckResult(
            "super_call",
            False,
            "fail",
            f"❌ Missing: define {class_name}.{method_name}() before calling super().",
        )

    for node in ast.walk(method):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != method_name:
            continue
        value = node.func.value
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            if value.func.id == "super":
                return CheckResult(
                    "super_call",
                    True,
                    "pass",
                    f"✅ Great! {class_name}.{method_name}() calls super().{method_name}().",
                )

    return CheckResult(
        "super_call",
        False,
        "fail",
        f"❌ Missing: call super().{method_name}() inside {class_name}.{method_name}().",
    )


def check_property_decorator(tree, class_name) -> CheckResult:
    """Detect use of @property for encapsulation in a class."""
    class_node = _find_class(tree, class_name)
    if class_node is None:
        return CheckResult(
            "property_decorator",
            False,
            "fail",
            f"❌ Missing: define {class_name} before adding a @property getter.",
        )

    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorator_names = {_decorator_name(decorator) for decorator in node.decorator_list}
            if "property" in decorator_names:
                return CheckResult(
                    "property_decorator",
                    True,
                    "pass",
                    f"✅ Great! {class_name}.{node.name} uses @property for safe access.",
                )

    return CheckResult(
        "property_decorator",
        False,
        "warning",
        f"⚠️ Add a @property getter in {class_name} to expose encapsulated data safely.",
    )
