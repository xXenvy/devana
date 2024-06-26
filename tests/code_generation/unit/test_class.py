import unittest
from devana.code_generation.printers.default.basictypeprinter import BasicTypePrinter
from devana.code_generation.printers.default.typeexpressionprinter import TypeExpressionPrinter
from devana.code_generation.printers.default.templateparameterprinter import TemplateParameterPrinter
from devana.code_generation.printers.default.typeexpressionprinter import GenericTypeParameterPrinter
from devana.code_generation.printers.default.functionprinter import ArgumentPrinter
from devana.code_generation.printers.default.classprinter import *
from devana.code_generation.printers.codeprinter import CodePrinter
from devana.syntax_abstraction.functioninfo import FunctionModification
from devana.syntax_abstraction.typeexpression import TypeModification, BasicType
from devana.syntax_abstraction.classinfo import *
from devana.syntax_abstraction.templateinfo import TemplateInfo, GenericTypeParameter


class TestClassElementsAlone(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(MethodPrinter, MethodInfo)
        printer.register(ConstructorPrinter, ConstructorInfo)
        printer.register(DestructorPrinter, DestructorInfo)
        printer.register(AccessSpecifierPrinter, AccessSpecifier)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(ArgumentPrinter, FunctionInfo.Argument)
        printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        printer.register(GenericTypeParameterPrinter, GenericTypeParameter)
        printer.register(FieldPrinter, FieldInfo)
        self.printer: CodePrinter = printer

    def test_print_simple_method_dec(self):
        source = MethodInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "long foo(float a, int* b = nullptr);\n")

    def test_print_simple_method_def(self):
        source = MethodInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.name = "b"
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        source.body = "float c = a * *b;\nif(c > 10.0f)\n    c *=0.5f;\nreturn c;"
        result = self.printer.print(source)
        self.assertEqual(result, """long foo(float a, int* b = nullptr)\n{\n    float c = a * *b;\n    if(c > 10.0f)\n        c *=0.5f;\n    return c;\n}\n""")

    def test_print_method_noexcept(self):
        source = MethodInfo.create_default()
        source.name = "foo"
        source.return_type = TypeExpression()
        source.return_type.details = BasicType.LONG
        source.modification = FunctionModification.NOEXCEPT
        result = self.printer.print(source)
        self.assertEqual(result, "long foo() noexcept;\n")

    def test_print_simple_constructor_dec(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "foo(float a, int* b = nullptr);\n")

    def test_print_simple_constructor_def(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.name = "b"
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        source.body = "float c = a * *b;\nif(c > 10.0f)\n    c *=0.5f;\nreturn c;"
        result = self.printer.print(source)
        self.assertEqual(result, """foo(float a, int* b = nullptr)\n{\n    float c = a * *b;\n    if(c > 10.0f)\n        c *=0.5f;\n    return c;\n}\n""")

    def test_print_simple_destructor_dec(self):
        source = DestructorInfo.create_default()
        source.name = "~foo"
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.default_value = "nullptr"
        arg2.name = "b"
        source.arguments = [arg1, arg2]
        result = self.printer.print(source)
        self.assertEqual(result, "~foo(float a, int* b = nullptr);\n")

    def test_print_simple_destructor_def(self):
        source = DestructorInfo.create_default()
        source.name = "~foo"
        arg1 = FunctionInfo.Argument()
        arg1.type = TypeExpression()
        arg1.type.details = BasicType.FLOAT
        arg1.name = "a"
        arg2 = FunctionInfo.Argument()
        arg2.type = TypeExpression()
        arg2.type.details = BasicType.INT
        arg2.type.modification = TypeModification.POINTER
        arg2.name = "b"
        arg2.default_value = "nullptr"
        source.arguments = [arg1, arg2]
        source.body = "float c = a * *b;\nif(c > 10.0f)\n    c *=0.5f;\nreturn c;"
        result = self.printer.print(source)
        self.assertEqual(result, """~foo(float a, int* b = nullptr)\n{\n    float c = a * *b;\n    if(c > 10.0f)\n        c *=0.5f;\n    return c;\n}\n""")

    def test_print_default_method(self):
        source = MethodInfo.create_default()
        source.modification |= FunctionModification.DEFAULT
        source.type = MethodType.OPERATOR
        source.name = "operator new"
        source.return_type.details = BasicType.VOID
        result = self.printer.print(source)
        self.assertEqual(result, "void operator new() = default;\n")

    def test_print_default_constructor(self):
        source = ConstructorInfo.create_default()
        source.modification |= FunctionModification.DEFAULT
        source.name = "Foo"
        result = self.printer.print(source)
        self.assertEqual(result, "Foo() = default;\n")

    def test_print_default_destructor(self):
        source = DestructorInfo.create_default()
        source.modification |= FunctionModification.DEFAULT
        source.name = "~Foo"
        result = self.printer.print(source)
        self.assertEqual(result, "~Foo() = default;\n")

    def test_print_delete_method(self):
        source = MethodInfo.create_default()
        source.modification |= FunctionModification.DELETE
        source.type = MethodType.OPERATOR
        source.name = "operator new"
        source.return_type.details = BasicType.VOID
        result = self.printer.print(source)
        self.assertEqual(result, "void operator new() = delete;\n")

    def test_print_delete_constructor(self):
        source = ConstructorInfo.create_default()
        source.modification |= FunctionModification.DELETE
        source.name = "Foo"
        result = self.printer.print(source)
        self.assertEqual(result, "Foo() = delete;\n")

    def test_print_delete_destructor(self):
        source = DestructorInfo.create_default()
        source.modification |= FunctionModification.DELETE
        source.name = "~Foo"
        result = self.printer.print(source)
        self.assertEqual(result, "~Foo() = delete;\n")

    def test_print_access_specifier(self):
        source = AccessSpecifier.PUBLIC
        result = self.printer.print(source)
        self.assertEqual(result, "public:\n")
        source = AccessSpecifier.PRIVATE
        result = self.printer.print(source)
        self.assertEqual(result, "private:\n")
        source = AccessSpecifier.PROTECTED
        result = self.printer.print(source)
        self.assertEqual(result, "protected:\n")

    def test_print_constructor_init_list(self):
        source = ConstructorInfo.create_default()
        source.initializer_list = []
        source.initializer_list.append(ConstructorInfo.InitializerInfo("a", "6.7f"))
        source.initializer_list.append(ConstructorInfo.InitializerInfo("b", "nullptr"))
        source.body = ""
        source.name = "Foo"
        result = self.printer.print(source)
        self.assertEqual(result, "Foo():\n    a(6.7f),\n    b(nullptr)\n{\n}\n")

    def test_print_mutable_field(self):
        source = FieldInfo.create_default()
        source.name = "a"
        source.type = TypeExpression()
        source.type.details = BasicType.FLOAT
        source.type.modification = TypeModification.MUTABLE
        result = self.printer.print(source)
        self.assertEqual(result, "mutable float a;\n")

    def test_print_inline_field(self):
        source = FieldInfo.create_default()
        source.name = "a"
        source.type = TypeExpression()
        source.type.details = BasicType.FLOAT
        source.type.modification = TypeModification.INLINE
        result = self.printer.print(source)
        self.assertEqual(result, "inline float a;\n")

    def test_print_three_way_comparison_operator(self):
        source = MethodInfo()
        source.name = "operator<=>"
        source.type = MethodType.OPERATOR
        source.return_type = BasicType.BOOL
        arg = FunctionInfo.Argument()
        arg.type = TypeExpression()
        arg.type.details = BasicType.INT
        arg.name = "a"
        source.arguments = [arg]
        result = self.printer.print(source)
        self.assertEqual(result, "bool operator<=>(int a);\n")


class TestClassComplex(unittest.TestCase):

    def setUp(self):
        printer = CodePrinter()
        printer.register(FunctionPrinter, FunctionInfo)
        printer.register(MethodPrinter, MethodInfo)
        printer.register(ConstructorPrinter, ConstructorInfo)
        printer.register(DestructorPrinter, DestructorInfo)
        printer.register(AccessSpecifierPrinter, AccessSpecifier)
        printer.register(VariablePrinter, Variable)
        printer.register(BasicTypePrinter, BasicType)
        printer.register(TypeExpressionPrinter, TypeExpression)
        printer.register(VariablePrinter, FunctionInfo.Argument)
        printer.register(ClassPrinter, ClassInfo)
        printer.register(FieldPrinter, FieldInfo)
        printer.register(TemplateParameterPrinter, TemplateInfo.TemplateParameter)
        printer.register(GenericTypeParameterPrinter, GenericTypeParameter)
        printer.register(SectionPrinter, SectionInfo)
        self.printer: CodePrinter = printer

    def test_simple_empty_struct(self):
        source = ClassInfo.create_default()
        source.name = "TestStruct"
        source.is_struct = True
        result = self.printer.print(source)
        self.assertEqual(result, "struct TestStruct\n{\n};\n")

    def test_decl_class(self):
        source = ClassInfo.create_default()
        source.name = "TestClass"
        source.is_class = True
        source.is_declaration = True
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass;\n")

    def test_simple_inheritance_class(self):
        parent = ClassInfo.create_default()
        parent.name = "ParentA"
        parent.is_class = True
        inheritance = InheritanceInfo()
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents[0].access_specifier = AccessSpecifier.PUBLIC
        inheritance.type_parents[0].is_virtual = False
        inheritance.type_parents[0].type = parent
        source = ClassInfo.create_default()
        source.is_class = True
        source.name = "TestClass"
        source.inheritance = inheritance
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass: public ParentA\n{\n};\n")

    def test_simple_multiple_inheritance_class(self):
        parent_1 = ClassInfo.create_default()
        parent_1.name = "ParentA"
        parent_1.is_class = True
        parent_2 = ClassInfo.create_default()
        parent_2.name = "ParentB"
        parent_2.is_class = True
        inheritance = InheritanceInfo()
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents[0].access_specifier = AccessSpecifier.PUBLIC
        inheritance.type_parents[0].is_virtual = False
        inheritance.type_parents[0].type = parent_1
        inheritance.type_parents[1].access_specifier = AccessSpecifier.PRIVATE
        inheritance.type_parents[1].is_virtual = False
        inheritance.type_parents[1].type = parent_2
        source = ClassInfo()
        source.is_class = True
        source.name = "TestClass"
        source.inheritance = inheritance
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass: public ParentA, private ParentB\n{\n};\n")

    def test_simple_virtual_inheritance_class(self):
        parent_1 = ClassInfo.create_default()
        parent_1.name = "ParentA"
        parent_1.is_class = True
        parent_2 = ClassInfo()
        parent_2.name = "ParentB"
        parent_2.is_class = True
        inheritance = InheritanceInfo()
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents[0].access_specifier = AccessSpecifier.PUBLIC
        inheritance.type_parents[0].is_virtual = False
        inheritance.type_parents[0].type = parent_1
        inheritance.type_parents[1].access_specifier = AccessSpecifier.PRIVATE
        inheritance.type_parents[1].is_virtual = True
        inheritance.type_parents[1].type = parent_2
        source = ClassInfo()
        source.is_class = True
        source.name = "TestClass"
        source.inheritance = inheritance
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass: public ParentA, private virtual ParentB\n{\n};\n")

    def test_namespace_inheritance(self):
        parent_1 = ClassInfo.create_default()
        parent_1.name = "ParentA"
        parent_1.is_class = True
        inheritance = InheritanceInfo()
        inheritance.type_parents.append(InheritanceInfo.InheritanceValue())
        inheritance.type_parents[0].access_specifier = AccessSpecifier.PUBLIC
        inheritance.type_parents[0].type = parent_1
        inheritance.type_parents[0].namespaces = ["test"]
        source = ClassInfo()
        source.is_class = True
        source.name = "TestClass"
        source.inheritance = inheritance
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass: public test::ParentA\n{\n};\n")

    def test_simple_struct(self):
        source = ClassInfo.create_default()
        source.name = "TestStruct"
        source.is_class = False
        source.content.append(FieldInfo())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.modification = TypeModification.POINTER
        source.content[0].type.details = BasicType.FLOAT
        source.content.append(FieldInfo())
        source.content[1].name = "b"
        source.content[1].type = TypeExpression()
        source.content[1].type.details = BasicType.U_INT
        source.content.append(FieldInfo())
        source.content[2].name = "c"
        source.content[2].type = TypeExpression()
        source.content[2].type.modification = TypeModification.STATIC
        source.content[2].type.details = BasicType.BOOL
        result = self.printer.print(source)
        self.assertEqual(result, "struct TestStruct\n{\n    float* a;\n    unsigned int b;\n    static bool c;\n};\n")

    def test_simple_self_ref_struct(self):
        source = ClassInfo.create_default()
        source.name = "TestStruct"
        source.is_class = False
        source.content.append(FieldInfo())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.modification = TypeModification.POINTER
        source.content[0].type.details = source
        result = self.printer.print(source)
        self.assertEqual(result, "struct TestStruct\n{\n    TestStruct* a;\n};\n")

    def test_simple_class_access(self):
        source = ClassInfo.create_default()
        source.name = "TestClass"
        source.is_class = True
        source.content.append(FieldInfo())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.details = BasicType.FLOAT
        source.content.append(AccessSpecifier.PUBLIC)
        source.content.append(FieldInfo())
        source.content[2].name = "b"
        source.content[2].type = TypeExpression()
        source.content[2].type.details = BasicType.U_INT
        source.content.append(FieldInfo())
        source.content[3].name = "c"
        source.content[3].type = TypeExpression()
        source.content[3].type.details = BasicType.BOOL
        source.content.append(AccessSpecifier.PRIVATE)
        source.content.append(FieldInfo())
        source.content[5].name = "d"
        source.content[5].type = TypeExpression()
        source.content[5].type.details = BasicType.DOUBLE
        result = self.printer.print(source)
        ref_result = "class TestClass\n"
        ref_result += "{\n"
        ref_result += "    float a;\n"
        ref_result += "public:\n"
        ref_result += "    unsigned int b;\n"
        ref_result += "    bool c;\n"
        ref_result += "private:\n"
        ref_result += "    double d;\n"
        ref_result += "};\n"
        self.assertEqual(ref_result, result)

    def test_simple_class_method(self):
        source = ClassInfo.create_default()
        source.name = "TestClass"
        source.is_class = True
        source.content.append(MethodInfo.create_default())
        source.content[0].name = "foo"
        source.content[0].return_type = TypeExpression()
        source.content[0].return_type.modification = TypeModification.POINTER
        source.content[0].return_type.details = BasicType.U_CHAR
        result = self.printer.print(source)
        self.assertEqual(result, "class TestClass\n{\n    unsigned char* foo();\n};\n")

    def test_nested_class(self):
        source = ClassInfo.create_default()
        source.name = "TestClass"
        source.is_class = True
        source.content.append(FieldInfo.create_default())
        source.content[0].name = "a"
        source.content[0].type = TypeExpression()
        source.content[0].type.details = BasicType.FLOAT
        nested_source = ClassInfo.create_default()
        nested_source.name = "NestedClass"
        nested_source.is_class = True
        nested_source.content.append(FieldInfo())
        nested_source.content[0].name = "x"
        nested_source.content[0].type = TypeExpression()
        nested_source.content[0].type.details = BasicType.DOUBLE
        nested_source.content.append(FieldInfo())
        nested_source.content[1].name = "y"
        nested_source.content[1].type = TypeExpression()
        nested_source.content[1].type.details = BasicType.DOUBLE
        source.content.append(nested_source)
        result = self.printer.print(source)
        ref_result = "class TestClass\n"
        ref_result += "{\n"
        ref_result += "    float a;\n"
        ref_result += "    class NestedClass\n"
        ref_result += "    {\n"
        ref_result += "        double x;\n"
        ref_result += "        double y;\n"
        ref_result += "    };\n"
        ref_result += "};\n"
        self.assertEqual(ref_result, result)

    def test_class_simple_template(self):
        source = ClassInfo.create_default()
        source.name = "TestClass"
        source.is_class = True
        source.content.append(MethodInfo.create_default())
        source.content[0].name = "foo"
        source.content[0].return_type = TypeExpression.create_default()
        source.content[0].return_type.modification = TypeModification.POINTER
        source.content[0].return_type.details = BasicType.U_CHAR
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nclass TestClass\n{\n    unsigned char* foo();\n};\n")

    def test_class_empty_template(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nstruct foo\n{\n};\n")

    def test_class_template_default_value(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        template_param.default_value = "int"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T = int>\nstruct foo\n{\n};\n")

    def test_class_template_standard(self):
        source = ClassInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        spec_1 = TypeExpression()
        spec_1.details = BasicType.INT
        spec_1.modification = TypeModification.REFERENCE
        spec_2 = TypeExpression.create_default()
        spec_2.details = BasicType.LONG
        spec_2.modification = TypeModification.CONST
        source.template.specialisation_values = [spec_1, spec_2]
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nstruct foo<int&,const long>\n{\n};\n")

    def test_constructor_simple_template(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nfoo();\n")

    def test_constructor_empty_template(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nfoo();\n")

    def test_constructor_template_argument(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        source.template.parameters = [template_param]
        argument = FunctionInfo.Argument()
        argument.type = TypeExpression.create_default()
        argument.type.details = GenericTypeParameter("T")
        argument.type.modification = TypeModification.CONST
        argument.name = "a"
        source.arguments = [argument]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T>\nfoo(const T a);\n")

    def test_constructor_template_default_value(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        template_param = TemplateInfo.TemplateParameter()
        template_param.name = "T"
        template_param.default_value = "int"
        source.template.parameters = [template_param]
        result = self.printer.print(source)
        self.assertEqual(result, "template<typename T = int>\nfoo();\n")

    def test_constructor_template_standard(self):
        source = ConstructorInfo.create_default()
        source.name = "foo"
        source.template = TemplateInfo()
        spec_1 = TypeExpression.create_default()
        spec_1.details = BasicType.INT
        spec_1.modification = TypeModification.REFERENCE
        spec_2 = TypeExpression.create_default()
        spec_2.details = BasicType.LONG
        spec_2.modification = TypeModification.CONST
        source.template.specialisation_values = [spec_1, spec_2]
        result = self.printer.print(source)
        self.assertEqual(result, "template<>\nfoo<int&,const long>();\n")

    def test_sections(self):
        source = ClassInfo.create_default()
        source.name = "Class"
        source.is_class = True
        source.content = [SectionInfo.create_default(source), FieldInfo.create_default(source)]
        result = self.printer.print(source)
        self.assertEqual(result, "class Class\n{\npublic:\n    int myVariable;\n};\n")
