"""AST-only evaluation engine for OOP Practice Lab submissions."""
import ast
from dataclasses import dataclass
from typing import Iterable, List



@dataclass
class CheckResult:
    """Normalized result returned by every evaluator check."""

    check_name: str
    passed: bool
    level: str
    message: str



class OOPEvaluator:
    """Coordinate parsing and data-driven AST checks."""

    def _check_map(self):
        """Return evaluator check functions keyed by fixture check_type."""
        from . import checks

        return {
            "has_class": checks.check_class_exists,
            "class_exists": checks.check_class_exists,
            "has_inheritance": checks.check_inheritance,
            "inheritance": checks.check_inheritance,
            "has_method": checks.check_method_exists,
            "method_exists": checks.check_method_exists,
            "method_override": checks.check_method_override,
            "encapsulation": checks.check_encapsulation,
            "dunder_init": checks.check_dunder_init,
            "super_call": checks.check_super_call,
            "property_decorator": checks.check_property_decorator,
        }

    def evaluate(self, code: str, test_cases: Iterable) -> List[CheckResult]:
        """Parse code with ast and run all configured test cases."""
        try:
            tree = ast.parse(code)
        except SyntaxError as error:
            return [
                CheckResult(
                    "syntax",
                    False,
                    "fail",
                    f"❌ Syntax error: {error.msg} on line {error.lineno}",
                )
            ]

        results = []
        for test_case in test_cases:
            results.append(
                self._run_check(
                    tree,
                    test_case.check_type,
                    test_case.check_target,
                    test_case.check_args or {},
                )
            )
        return results

    def _run_check(self, tree, check_type, check_target, check_args):
        """Resolve a configured check and execute it with normalized arguments."""
        check_function = self._check_map().get(check_type)
        if check_function is None:
            return CheckResult(
                check_type,
                False,
                "fail",
                f"❌ Unknown evaluator check type: {check_type}",
            )

        try:
            return check_function(tree, check_target, **check_args)
        except TypeError as error:
            return CheckResult(
                check_type,
                False,
                "fail",
                f"❌ Invalid check configuration for {check_type}: {error}",
            )
