namespace nom {
    struct A
    {
        int a;
        float b;
    };
}

using B = const nom::A*;

int foo(const B x) {
    return x->a / x->b;
}

template<typename T>
struct A_T
{
    float x;
    const T y;
};

using AT = const A_T<double>;

namespace num {
    struct A
    {
        char x;
        int y;
    };
}

template<typename T, class B>
struct TestStruct;

template<typename T>
concept TestConcept = true;

template<typename A, class B = float, typename ...Args>
using UsingTemplate = A;

template<typename T, typename C> requires true or TestConcept<T>
using UsingTemplateRequires = const TestStruct<C, T>;

template<TestConcept B = int>
using UsingConcept = const UsingTemplateRequires<float, B>*;