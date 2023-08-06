#define PY_SSIZE_T_CLEAN

#include <Python.h>

#include "include/_math.h" /* contains untouched <math.h> functions and constants */
#include "include/_mmath.h" /* contains modified <math.h> functions */
#include "include/yammpy.h" /* contains new functions implemented for yammpy module */
#include "include/constants.h" /* contains constants */

/* yammpy functions */

static PyObject *
yammpy_degree(PyObject *self, PyObject *arg) {
	return PyFloat_FromDouble(PyFloat_AsDouble(arg) * rad2deg);
}

static PyObject *
yammpy_radian(PyObject *self, PyObject *arg) {
	return PyFloat_FromDouble(PyFloat_AsDouble(arg) * deg2rad);
}

static PyObject *
yammpy_isfinite(PyObject *self, PyObject *arg) {
    return PyBool_FromLong((long)Py_IS_FINITE(PyFloat_AsDouble(arg)));
}

static PyObject *
yammpy_isinf(PyObject *self, PyObject *arg) {
    return PyBool_FromLong((long)Py_IS_INFINITY(PyFloat_AsDouble(arg)));
}

static PyObject *
yammpy_isnan(PyObject *self, PyObject *arg) {
    return PyBool_FromLong((long)Py_IS_NAN(PyFloat_AsDouble(arg)));
}

static PyObject *
yammpy_isperfsqr(PyObject *self, PyObject *arg) {
    double x;
    long long left, right, mid;

    x = PyFloat_AsDouble(arg);

    left = 1;
    right = (long long)x;

    while (left <= right) {
        mid = (left + right) / 2;

        if (mid * mid == x) {
            Py_RETURN_TRUE;
        }

        if (mid * mid < x) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    Py_RETURN_FALSE;
}

static PyObject *
yammpy_sum(PyObject *module, PyObject *arg) {
    double sum=0;
    Py_ssize_t i, len;

    if(!PyList_Check(arg)) {
        PyErr_SetString(PyExc_ValueError, "Expected a List."); /* invalid arg */
        return NULL;
    }

    len = PyList_Size(arg);
    
    for(i=0; i<len;i++)
        sum += PyFloat_AsDouble(PyList_GetItem(arg, i));

    return PyFloat_FromDouble(sum);
}

static PyObject *
yammpy_prod(PyObject *module, PyObject *arg) {
    double prod=1;
    Py_ssize_t i, len;

    if(!PyList_Check(arg)) {
        PyErr_SetString(PyExc_ValueError, "Expected a List."); /* invalid arg */
        return NULL;
    }

    len = PyList_Size(arg);
    
    for(i=0; i<len;i++)
        prod *= PyFloat_AsDouble(PyList_GetItem(arg, i));

    return PyFloat_FromDouble(prod);
}

/* _mmath functions */

static PyObject *
_mmath_fmod(PyObject *self, PyObject *args) {
	double x, y;

    if (!PyArg_ParseTuple(args, "dd", &x, &y))
        return NULL;

    if(y == 0) {
        PyErr_SetString(PyExc_ValueError, "Division by Zero."); /* invalid arg */
        return NULL;
    }

    return PyFloat_FromDouble(fmod(x, y));
}

static PyObject *
_mmath_remainder(PyObject *self, PyObject *args) {
	double x, y;

    if (!PyArg_ParseTuple(args, "dd", &x, &y))
        return NULL;

    if(y == 0) {
        PyErr_SetString(PyExc_ValueError, "Division by Zero."); /* invalid arg */
        return NULL;
    }

    return PyFloat_FromDouble(remainder(x, y));
}

static PyObject *
_mmath_sqrt(PyObject *self, PyObject *arg) {
	double x;

    x = PyFloat_AsDouble(arg);

    if(x < 0) {
        PyErr_SetString(PyExc_ValueError, "Negative values are not accepted."); /* invalid arg */
        return NULL;
    }

    return PyFloat_FromDouble(sqrt(x));
}

static PyMethodDef yammpy_methods[] = {
	/* untouched <math.h> functions */
    {"acos",            _math_acos,      METH_O,         _math_acos_doc},
    {"acosh",           _math_acosh,     METH_O,         _math_acosh_doc},
    {"asin",            _math_asin,      METH_O,         _math_asin_doc},
    {"asinh",           _math_asinh,     METH_O,         _math_asinh_doc},
    {"atan",            _math_atan,      METH_O,         _math_atan_doc},
    {"atanh",           _math_atanh,     METH_O,         _math_atanh_doc},
    {"cbrt",            _math_cbrt,      METH_O,         _math_cbrt_doc},
	{"ceil",			_math_ceil,		 METH_O,		 _math_ceil_doc},
    {"cos",             _math_cos,       METH_O,         _math_cos_doc},
    {"cosh",            _math_cosh,      METH_O,         _math_cosh_doc},
    {"erf",             _math_erf,       METH_O,         _math_erf_doc},
    {"erfc",            _math_erfc,      METH_O,         _math_erfc_doc},
    {"exp",             _math_exp,       METH_O,         _math_exp_doc},
    {"exp2",            _math_exp2,      METH_O,         _math_exp2_doc},
    {"expm1",           _math_expm1,     METH_O,         _math_expm1_doc},
	{"fabs",            _math_fabs,      METH_O,         _math_fabs_doc},
    {"floor",           _math_floor,     METH_O,         _math_floor_doc},
    {"gamma",           _math_gamma,     METH_O,         _math_gamma_doc},
    {"lgamma",          _math_lgamma,    METH_O,         _math_lgamma_doc},
    {"log",             _math_log,       METH_O,         _math_log_doc},
    {"log2",            _math_log2,      METH_O,         _math_log2_doc},
    {"log10",           _math_log10,     METH_O,         _math_log10_doc},
    {"log1p",           _math_log1p,     METH_O,         _math_log1p_doc},
    {"logb",            _math_logb,      METH_O,         _math_logb_doc},
    {"nearbyint",       _math_nearbyint, METH_O,         _math_nearbyint_doc},
    {"sin",             _math_sin,       METH_O,         _math_sin_doc},
    {"sinh",            _math_sinh,      METH_O,         _math_sinh_doc},
    {"tan",             _math_tan,       METH_O,         _math_tan_doc},
    {"tanh",            _math_tanh,		 METH_O,		 _math_tanh_doc},
    {"trunc",           _math_trunc,     METH_O,		 _math_trunc_doc},
    {"atan2",           _math_atan2,     METH_VARARGS,   _math_atan2_doc},
    {"copysign",        _math_copysign,  METH_VARARGS,   _math_copysign_doc},
    {"fdim",            _math_fdim,      METH_VARARGS,   _math_fdim_doc},
    {"hypot",           _math_hypot,     METH_VARARGS,   _math_hypot_doc},
    {"pow",             _math_pow,       METH_VARARGS,   _math_pow_doc},
	/* modified <math.h> functions */
    _MMATH_FMOD_METHODDEF
    _MMATH_REMAINDER_METHODDEF
    _MMATH_SQRT_METHODDEF
	/* yammpy functions */
    YAMMPY_DEGREES_METHODDEF
    YAMMPY_RADIANS_METHODDEF
    YAMMPY_SUM_METHODDEF
    YAMMPY_PROD_METHODDEF
    YAMMPY_ISFINITE_METHODDEF
    YAMMPY_ISINF_METHODDEF
    YAMMPY_ISNAN_METHODDEF
    YAMMPY_ISPERFSQR_METHODDEF
    {NULL}, /* sentinel */
};

PyDoc_STRVAR(yammpy_doc, "yammpy provides access to the mathematical functions");

static struct PyModuleDef yammpy = {
    PyModuleDef_HEAD_INIT,
    "yammpy",
    yammpy_doc,
    -1,
    yammpy_methods,
};

PyMODINIT_FUNC
PyInit_yammpy(void) {
	PyObject *yamm;

	yamm = PyModule_Create(&yammpy);

	if(yamm == NULL)
		return NULL;
	
	PyModule_AddObject(yamm, "pi", PyFloat_FromDouble(PI));
    PyModule_AddObject(yamm, "e", PyFloat_FromDouble(E));
    PyModule_AddObject(yamm, "tau", PyFloat_FromDouble(TAU));
	PyModule_AddObject(yamm, "phi", PyFloat_FromDouble(PHI));
    PyModule_AddObject(yamm, "wal", PyFloat_FromDouble(WAL));
	PyModule_AddObject(yamm, "inf", PyFloat_FromDouble(INFINITY));
    PyModule_AddObject(yamm, "nan", PyFloat_FromDouble(NAN));

    return yamm;
}
