#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef _linux__
  #define __USE_POSIX199309
  #include <time.h>
#elif _WIN32
  #include <Windows.h>
#endif

#include "bmw.h"
#include "b64.c/b64.h"

static PyObject* archash(PyObject* self, PyObject* args)
{
    const char* _prehash_str;
    size_t _argc = 1;

    // Get arguments passed in & check type of the argument
    if (!PyArg_ParseTuple(args, "s", &_prehash_str))
        return NULL;
        
    if (_argc != 1)
        Py_RETURN_NONE;

    // Make time millisecond
    uint64_t _timespan = 0;

#ifdef __linux__

    struct timespec _timespec;
    clock_gettime(0, &_timespec);

    _timespan = _timespec.tv_sec * 1000 +
                _timespec.tv_nsec / 1000000;
#else _WIN32

    GetSystemTimeAsFileTime((LPFILETIME)&_timespan);

    // time starts since 1601.
    _timespan /= 10000;
    _timespan -= 11644473600000;

#endif

    // Make bytes for hash
    uint32_t _arglen_body;
    uint32_t _hash_length;
    char *_hash_bytes = NULL;
    {
        // Measure string length
        _arglen_body = strlen(_prehash_str);

        // Allocate string buffer
        _hash_length = 8 + 32 + _arglen_body;
        _hash_bytes = malloc(_hash_length);
        {
            if (!_hash_bytes)
            {
                return PyErr_NoMemory();
            }
            memset(_hash_bytes, 0x00, _hash_length);
        }

        // Copy the timespan to buffer
        memcpy(_hash_bytes, &_timespan, 8);

        // Copy the bytes to buffer
        memcpy(_hash_bytes + 8, _prehash_str, _arglen_body);

        // Copy the salt to buffer
        for (int i = 0x00; i < 0x1F; ++i)
            *(_hash_bytes + _hash_length - 1 - i) = 0x1F - i;
    }

    // All done! Let's do hash
    HashReturn _hash_return;
    HashState _hash_state = {0};
    BitSequence _hash_value[0x30] = {0};

    if (Init(&_hash_state, 256) != SUCCESS
    || Update(&_hash_state, _hash_bytes, _hash_length * 8) != SUCCESS
    || Final(&_hash_state, _hash_value) != SUCCESS)
    {
        free(_hash_bytes);
        PyErr_SetString(PyExc_RuntimeError,"Generate hash failed.");
        Py_RETURN_NONE;
    }

    uint32_t _base64_length = 8 + sizeof(_hash_value);
    char *_base64_bytes = malloc(_base64_length);
    {
        if (!_base64_bytes)
        {
            free(_hash_bytes);
            return PyErr_NoMemory();
        }
        memset(_base64_bytes, 0x00, _base64_length);

        // Copy the timespan to buffer
        memcpy(_base64_bytes, &_timespan, 8);

        // Copy the hash result to buffer
        memcpy(_base64_bytes + 8, _hash_value, sizeof(_hash_value));
    }

    // Encode results to base64
    char *_result = b64_encode(_base64_bytes, _base64_length);

    // Cleanup resources
    free(_hash_bytes);
    free(_base64_bytes);

    return Py_BuildValue("s", _result);
}

// Module Methods
static PyMethodDef module_method =
{
    .ml_name  = "archash",
    .ml_meth  = archash,
    .ml_flags = METH_VARARGS,
    .ml_doc   = "archash(<string>)\n"
};

// Module Info
static PyModuleDef module_info =
{
    PyModuleDef_HEAD_INIT,
    .m_name    = "archash4all",
    .m_doc     = "Generate x-random-challenge for arcapi requests",
    .m_size    = 1,
    .m_methods = &module_method,
};

// Init
PyMODINIT_FUNC PyInit_archash4all(void){
    return PyModule_Create(&module_info);
}
