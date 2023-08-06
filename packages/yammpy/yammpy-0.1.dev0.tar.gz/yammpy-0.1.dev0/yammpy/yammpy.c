#define PY_SSIZE_T_CLEAN

#include <Python.h>

#include "include/yammpy.h"

static PyMethodDef yammpy_methods[] = {
    {NULL}, /* sentinel */
};

static struct PyModuleDef yammpy = {
        PyModuleDef_HEAD_INIT,
        "yammpy",
        "Yet Another Math Module for Python",
        -1,
        yammpy_methods,
};

PyMODINIT_FUNC 
PyInit_yammpy(void) {
    return PyModule_Create(&yammpy);
}
