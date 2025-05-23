template<typename T>
struct simple_template_struct_1
{
    T template_field;
};

template<class T>
struct simple_template_struct_2
{
    T template_field;
};

template<typename T>
class simple_template_class_1
{
    T template_field;
};

template<class T>
class simple_template_class_2
{
    T template_field;
};

template<typename T, typename P = const float>
class template_class_complex
{
public:
    template_class_complex(T* a, char b);
    ~template_class_complex();
    const T parm_1;
    T& parm_2;
    float *parm_3;
    T* parm_4;
    const T& parm_5;
    const T* parm_6;
    static T parm_7;
    static T& parm_8;
    static T* parm_9;
    P* method_1(float a);
private:
    int method_2(const T a, const P& b)
    {
        return 8;
    }

    template<typename D>
    D* method_3(const T a, D* b)
    {
        return b;
    }
};

template<typename T, typename P, typename ...Ts>
struct struct_variadic_template
{
    int a;
};

template<typename... Args>
struct struct_variadic_template2;

template<typename T, typename P>
struct template_struct
{
    T a;
    P* b;
};

template<typename P>
struct template_struct<const double&, P>
{
    const double& a;
    P* b;
};

template<typename P>
struct template_struct<P*, P>
{
    P* a;
    P* b;
};


template<>
struct template_struct<double, char>
{
    double a;
    char* b;
};

template<typename T, typename P, typename Q>
struct multiple_types
{
    int a;
}

template<typename T, typename P>
struct multiple_types<P, T, P*>
{
    double a;
}

template<typename T>
struct multiple_pointer_struct
{
    T** a;
}

template<typename T>
concept TestConcept = true;

template<TestConcept T = bool, TestConcept ...Args>
class BasicConceptClass {
    T foo(T arg);
};

template<TestConcept T, class B = int> requires true
class ConceptClass {
public:
    T a;
    void process(T arg)
        requires TestConcept<B>;
};

template<typename A, TestConcept T>
    requires false or
    true and TestConcept< T>
struct ConceptStruct {
    T abc = 10;
    T foo() requires (TestConcept<T> || true);
    T barFoo(T arg1, A arg2);
};