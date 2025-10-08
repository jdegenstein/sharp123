import inspect
from typing import Any

class BuildParameters:
    """
    A context manager that captures variables defined within its scope
    and attaches them as attributes to itself upon exit.
    
    Example:
        with BuildParameters() as params:
            my_var = 100
        print(params.my_var)  # Output: 100
    """
    def __init__(self):
        """Initializes the context manager's internal state."""
        self._caller_frame = None
        self._initial_locals_keys = set()

    def __enter__(self):
        """Captures the initial state of local variables when the block starts."""
        self._caller_frame = inspect.currentframe().f_back
        self._initial_locals_keys = set(self._caller_frame.f_locals.keys())
        return self

    def __getattr__(self, name: str) -> Any:
        """
        Dynamically looks up variables in the caller's scope. This allows
        nested contexts to access values from outer contexts in real-time.
        """
        if self._caller_frame and name in self._caller_frame.f_locals:
            return self._caller_frame.f_locals[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Captures new variables from the scope and attaches them as attributes
        to this instance.
        """
        if exc_type is not None:
            return False  # Propagate any exceptions

        final_locals = self._caller_frame.f_locals
        new_keys = set(final_locals.keys()) - self._initial_locals_keys
        
        # Filter out other context manager instances
        fields = {
            key: final_locals[key]
            for key in new_keys
            if not isinstance(final_locals[key], BuildParameters)
        }

        # *** KEY CHANGE ***
        # Directly update the instance's dictionary with the captured fields.
        self.__dict__.update(fields)

        # Clean up the frame reference to prevent reference cycles
        self._caller_frame = None
        return False

    def __repr__(self) -> str:
        """Provides a clean, dataclass-like representation of the object."""
        # Exclude internal attributes (those starting with '_') from the output
        core_attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        if not core_attrs:
            return f"<{self.__class__.__name__} (active)>"
        
        attrs_str = ', '.join(f"{k}={v!r}" for k, v in core_attrs.items())
        return f"{self.__class__.__name__}({attrs_str})"
