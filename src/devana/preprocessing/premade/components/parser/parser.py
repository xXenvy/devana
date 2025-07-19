from typing import List, Dict, Type, Callable, Optional
import typing
from enum import Enum
from devana.preprocessing.premade.components.parser.extractor import IExtractor
from devana.preprocessing.premade.components.parser.argumentsparser import (ArgumentsParser, IParsable,
                                                                            ArgumentGenericTypeParser)
from devana.preprocessing.premade.components.parser.functionparser import FunctionParser, FunctionEntity
from devana.preprocessing.premade.components.parser.typechecker import is_arguments_valid
from devana.preprocessing.premade.components.executor.executable import CallFrame, Signature
from devana.preprocessing.preprocessor import ISource
from devana.syntax_abstraction.syntax import ISyntaxElement
from devana.preprocessing.premade.components.executor.environment import Environment


class Parser(ISource):
    """Parser of preprocessor functions given as string. Extractor must provide string of function, or example,
    from source code."""

    def __init__(self, extractor: IExtractor, signatures: List[Signature]):
        self._extractor = extractor
        self._signatures = signatures

        enum_types: List[IParsable] = []
        for signature in signatures:
            for arg in signature.arguments.positional:
                enum_types += self._find_enum(arg)
            for value in signature.arguments.named.values():
                enum_types += self._find_enum(value)

        self._arguments_parser = ArgumentsParser([ArgumentGenericTypeParser.create_from_enum(e) for e in enum_types])

    @classmethod
    def _find_enum(cls, hint) -> List[Type[Enum]]:
        try:
            if issubclass(hint, Enum):
                return [hint]
        except TypeError:
            pass
        hint_origin = typing.get_origin(hint)
        if hint_origin is None:
            return []
        args = typing.get_args(hint)
        result = []
        for arg in args:
            result += cls._find_enum(arg)
        return result

    def _create_calling_data(self, function: FunctionEntity, parent: ISyntaxElement) -> Environment.CallingData:
        arguments = self._arguments_parser.tokenize(function.arguments)
        positional_arguments: List[CallFrame.Arguments.Value] = []
        named_arguments: Dict[str, CallFrame.Arguments.Value] = {}

        # we need to search named arguments and unnamed to create the right arguments entry
        for argument in arguments:
            if isinstance(argument, dict):
                if len(argument.keys()) != 0:
                    raise ValueError("Internal error. Argument parser provide too many keys in dictionary.")
                key = list(argument.keys())[0]
                if not isinstance(key, str):
                    raise ValueError("Internal error. Argument parser provide wrong dictionary key type.")
                named_arguments[key] = CallFrame.Arguments.Value(argument[key])
            else:
                positional_arguments.append(CallFrame.Arguments.Value(argument))

        # find proper signature for this function.
        matched: List[Signature] = list(filter(
            lambda s: s.name == function.name and s.namespaces == function.namespaces,
            self._signatures
        ))
        if len(matched) > 1:
            raise ValueError(f"Duplicated signatures found for function: {function.namespaces}::{function.name}")
        if len(matched) == 0:
            raise ValueError(f"Cannot find signature for function: {function.namespaces}::{function.name}")
        signature: Signature = matched[0]

        arguments_fame = CallFrame.Arguments(positional_arguments, named_arguments)
        if not is_arguments_valid(arguments_fame, signature.arguments):
            raise ValueError(f"Cannot match arguments for signature: {function.namespaces}::{function.name}")
        return Environment.CallingData(arguments_fame, parent, signature)

    @classmethod
    def get_produced_type(cls) -> Type:
        return Environment.CallingData

    def feed(self) -> List[Environment.CallingData[ISyntaxElement]]:
        result = []
        function_parser = FunctionParser()
        for data in self._extractor.extract():
            functions = function_parser.parse(data.text)
            for function in functions:
                result.append(self._create_calling_data(function, data.parent))
        return result


class FilterableParser(Parser):
    """Extends Parser by invoking a user-provided callback for each parsed function entity.

    For each parsed function entity, the callback is invoked with:
    - function: the FunctionEntity instance.
    - parent: the ExtractedFunction parent (context for creating CallingData).

    The callback should return:
    - None to use the default call-frame logic.
    - A CallingData to assign a custom invocation (signature, arguments) to the function."""
    def __init__(
            self,
            extractor: IExtractor,
            signatures: List[Signature],
            calling_data_callback: Callable[[FunctionEntity, ISyntaxElement], Optional[Environment.CallingData[ISyntaxElement]]]
    ):
        super().__init__(extractor, signatures)
        self._calling_data_callback = calling_data_callback

    def feed(self) -> List[Environment.CallingData[ISyntaxElement]]:
        result = []
        function_parser = FunctionParser()
        for data in self._extractor.extract():
            functions = function_parser.parse(data.text)
            for function in functions:
                call_frame = self._calling_data_callback(function, data.parent) or self._create_calling_data(function, data.parent)
                result.append(call_frame)
        return result
