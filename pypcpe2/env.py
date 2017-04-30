import multiprocessing


class _Env(object):
    def __init__(self):
        self._temp_path = "./temp"
        self._buffer_size = 100 * 1024 * 1024
        self._io_buffer_size = 16 * 1024 * 1024
        self._output_min_len = 10
        self._compare_seq_size = 10000
        self._thread_size = multiprocessing.cpu_count()

    def temp_path():
        doc = "The temp_path property."
        def fget(self):
            return self._temp_path
        def fset(self, value):
            self._temp_path = value
        return locals()
    temp_path = property(**temp_path())

    def buffer_size():
        doc = "The buffer_size property."
        def fget(self):
            return self._buffer_size
        def fset(self, value):
            self._buffer_size = value
        return locals()
    buffer_size = property(**buffer_size())

    def io_buffer_size():
        doc = "The io_buffer_size property."
        def fget(self):
            return self._io_buffer_size
        def fset(self, value):
            self._io_buffer_size = value
        return locals()
    io_buffer_size = property(**io_buffer_size())

    def output_min_len():
        doc = "The output_min_len property."
        def fget(self):
            return self._output_min_len
        def fset(self, value):
            self._output_min_len = value
        return locals()
    output_min_len = property(**output_min_len())

    def compare_seq_size():
        doc = "The compare_seq_size property."
        def fget(self):
            return self._compare_seq_size
        def fset(self, value):
            self._compare_seq_size = value
        return locals()
    compare_seq_size = property(**compare_seq_size())

    def thread_size():
        doc = "The thread_size property."
        def fget(self):
            return self._thread_size
        def fset(self, value):
            self._thread_size = value
        return locals()
    thread_size = property(**thread_size())


_env_instance = None
def env():
    global _env_instance
    if _env_instance is not None:
        return _env_instance
    else:
        _env_instance = _Env()
        return _env_instance

