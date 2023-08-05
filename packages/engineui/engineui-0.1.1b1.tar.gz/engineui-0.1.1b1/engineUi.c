#include "engineUi.h"

static PyObject *init(PyObject *self, PyObject *args)
{
    Py_XINCREF(Py_None);
    PyObject* none = Py_None;
    return none;
}

static PyMethodDef UIMethods[2] = {
    {"init",  init, METH_VARARGS,
     "Initialise Engine GUI."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef UIModule = {
    PyModuleDef_HEAD_INIT,
    "engineui",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    UIMethods
};

PyMODINIT_FUNC PyInit_engineui(void)
{
    PyObject *m;

    m = PyModule_Create(&UIModule);
    if (m == NULL)
        return NULL;

    UIError = PyErr_NewException("engineui.error", NULL, NULL);
    Py_XINCREF(UIError);
    if (PyModule_AddObject(m, "error", UIError) < 0) {
        Py_XDECREF(UIError);
        Py_CLEAR(UIError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
//
int main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    if (PyImport_AppendInittab("engineui", PyInit_engineui) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required.
       If this step fails, it will be a fatal error. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyObject *pmodule = PyImport_ImportModule("engineui");
    if (!pmodule) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'engineui'\n");
    }

    PyMem_RawFree(program);
    return 0;
}
