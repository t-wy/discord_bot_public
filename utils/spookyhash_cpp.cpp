// cppimport
#include <Python.h>
#include <SpookyV2.cpp>

static PyObject* hash128(PyObject* self, PyObject* args, PyObject* kwargs) {
    // NULL terminated keyword list
    PyObject* message;
    // cpp uses const char*
    static char* kwlist[] = {(char*)"message", NULL};
    // S: PyBytesObject 
    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs,
        "S",
        kwlist, &message
    ))
        return NULL;

    // main code
    const char* message_bytes = PyBytes_AsString(message);
    Py_ssize_t length = PyBytes_Size(message);
    uint64 digest[2] = {0ULL, 0ULL};
    SpookyHash::Hash128(
        message_bytes,
        static_cast<size_t>(length),
        &digest[0],
        &digest[1]
    );

    // return
    return PyBytes_FromStringAndSize(reinterpret_cast<const char*>(digest), 16);
}

// Method definition table
static PyMethodDef methods[] = { 
    {"hash128", (PyCFunction) hash128, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL} // Sentinel
};

// Module definition
static struct PyModuleDef module = {
#ifdef _MSC_VER
    PyModuleDef_HEAD_INIT,
    "spookyhash_cpp",
    NULL,
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
#else
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "spookyhash_cpp",
    .m_size = -1,
    .m_methods = methods
#endif
};

// Module initialization
PyMODINIT_FUNC PyInit_spookyhash_cpp(void) {
    return PyModule_Create(&module);
}