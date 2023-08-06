"""
Code inspection / review

TODO: include type checking using mypy
"""
from os import error
from pathlib import Path
import ast
from typing import Union, Dict, List, Optional
from collections import Counter
import re

from loguru import logger

from james.utils import cmd


class CodeInspection:

    FILENAME: str = 'codereview.log'
    EXCLUDE_PATTERN: str = '.git,.eggs,__pycache__,.tox,docs,test,tests,.pytest_cache'
    IGNORE_PATTERN: str = 'D200,D205,D212,D213,D415'
    TYPE_HINT_CHECKS: List[str] = [
        'Function is missing a type annotation',
        'Function is missing a return type annotation',
        'Function is missing a type annotation for one or more arguments',
        'Use "-> None" if function does not return a value'
    ]

    def __init__(self, path: Union[Path, str], check_types: bool = True) -> None:
        logger.info(f'Starting code inspection for directory {path}')
        self.path: Path = Path(path)
        self.flg_check_types = check_types
        self.counts: Dict = {}
        self.totals = {
            'classes': 0,
            'methods': 0,
            'functions': 0,
            'expressions': 0,
        }
        self.syntax_errors = {}
        self.error_counts = Counter()
        self.error_counts_per_file = Counter()


    def count(self) -> None:
        """
        Count code elements (i.e. classes, functions etc.) in directory
        """
        self.counts = CodeCounter(self.path, exclude_pattern=self.EXCLUDE_PATTERN.split(','))()
        for key in self.totals.keys():
            self.totals[key] = sum([x[key] for x in self.counts.values()])

        self.syntax_errors = {
            filename: counts['syntaxerrors']
            for filename, counts in self.counts.items()
            if counts['syntaxerrors']
        }

    def lint(self) -> None:
        """
        Lint code with flake8
        """
        output_file = (self.path / self.FILENAME).as_posix()

        # N.B. the --output-file option appends instead of replaces, so fix this manually by removing an old file
        if Path(output_file).exists():
            cmd(f'rm {output_file}')

        issues = []

        # run flake8
        lint_result = cmd(
            f'flake8 \
            --exit-zero \
            --exclude={self.EXCLUDE_PATTERN} \
            --ignore={self.IGNORE_PATTERN} \
            --max-line-length=120 \
            --docstring-convention=google \
            .', 
            no_error=True
        )
        
        # parse flake8 results
        for line in lint_result.split('\n'):
            try:
                parts = line.split(':')
                filename = parts[0]
                linenumber = parts[1]
                char = parts[2]
                msg = ':'.join(parts[3:])
                #filename, linenumber, char, msg = line.split(':')
                msg = msg.strip()
                # filter out specifics in message (they are between '' or ()) so that the counter sees them as the same type of message
                msg = re.sub(r'\'[^\']*\'', '<expr>', msg)
                msg = re.sub(r'\([^\)]*\)', '<expr>', msg)
                issues.append([filename, linenumber, msg])
            except ValueError:
                logger.error(f'Cannot parse line "{line}"')

        if self.flg_check_types:
            # check if type hints are present (not if they are valid!)
            type_hint_result = cmd(
                f"python -m mypy \
                --disallow-untyped-defs \
                --exclude '(setup\.py|site-packages|docs|tests|__pycache__|\..*)' \
                .", 
                no_error=True
            )

            # parse mypy results
            for line in type_hint_result.split('\n'):
                try:
                    filename, linenumber, _, msg = line.split(':')
                    filename = f'./{filename}'  # same format as flake8 filename
                    msg = msg.strip()
                    if msg in self.TYPE_HINT_CHECKS:  # only consider errors on missing type hints
                        issues.append([filename, linenumber, msg])
                except ValueError:
                    logger.error(f'Cannot parse line "{line}"')
        
        # write all results to file
        with open(output_file, 'w') as f:
            for filename, line, msg in issues:
                self.error_counts.update([msg])
                self.error_counts_per_file.update([filename])
                f.write(f'{filename}:{line}:{msg}\n')

    def __call__(self) -> str:
        """
        Run the actual code inspection

        Returns:
            str: inspection report
        """
        self.count()
        self.lint()

        output_file = (self.path / self.FILENAME).as_posix()
        total_issues = sum(self.error_counts.values())
        total_functions = sum(self.totals.values())
        total_score = total_issues / max(total_functions, 1)

        lines = [
            '='*79,
            f'Code Inspection of directory "{self.path}"',
            '='*79,
        ] + [
            '\nSyntax errors encountered! > Re-run review after fixing them:' if self.syntax_errors else ''
        ] + [
            f'❌ {filename}: {errors[0]}'
            for filename, errors in self.syntax_errors.items()
        ] + [
            '',
            'Code analyzed:'
        ] + [
            f'* {count:3d} {key}'
            for key, count in self.totals.items()
        ] + [
            '',
            f'{total_issues} Issues found:'
        ] + [
            f'{count:3d} {("cases" if count > 1 else "case ")} of {msg}'
            for msg, count in self.error_counts.most_common()
        ] + [
            '',
            f'Issues per file:'
        ] + [
            f'{count:3d} {("issues" if count > 1 else "issue ")} in {filename}'
            for filename, count in self.error_counts_per_file.most_common()
        ] + [
            '',
            'Your total IPE score (issues per element, lower is better) is:',
            f'[ {total_score:.1f} ]',
            '',
            f'For full report, see {output_file}'
        ]
        return '\n'.join(lines)


class CodeCounter:
    """
    Utility class for counting the number of code elements (classes, functions etc.) in a directory
    """

    def __init__(self, path: Union[Path, str], exclude_pattern: Optional[List[str]] = None) -> None:
        self.path: Path = Path(path)
        self.counts: Dict[str, Dict[str, int]] = {}
        self.exclude_pattern: List[str] = exclude_pattern

    def _should_exclude(self, filename: Path) -> bool:
        for part in filename.parts:
            if part in self.exclude_pattern:
                return True
        return False

    def __call__(self) -> Dict[str, Dict[str, int]]:
        for filename in self.path.rglob('*.py'):
            if self._should_exclude(filename):
                continue
            filename_str = filename.as_posix()
            self.counts[filename_str] = self.count(filename_str)
        return self.counts

    @staticmethod
    def count(filename: str) -> Dict[str, int]:
        with open(filename, 'r') as f:
            # parse the AST of the file
            logger.info(f'parsing {filename}')
            code = f.read()

        try:
            tree = ast.parse(code)
            classes = [e for e in tree.body if isinstance(e, ast.ClassDef)]
            methods = [f for c in classes for f in c.body if isinstance(f, ast.FunctionDef)]
            funcs = [f for f in tree.body if isinstance(f, ast.FunctionDef)]
            expressions = [f for f in tree.body if isinstance(f, ast.Expr)]
            syntaxerrors = []
        except SyntaxError as e:
            logger.error(f'Syntax error encountered in {filename}')
            logger.error(e)
            classes = []
            methods = []
            funcs = []
            expressions = []
            syntaxerrors = [str(e)]

        return {
            'classes': len(classes),
            'methods': len(methods),
            'functions': len(funcs),
            'expressions': len(expressions),
            'syntaxerrors': syntaxerrors
        }
