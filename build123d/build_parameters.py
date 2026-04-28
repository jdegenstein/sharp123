import inspect
from typing import Any

class BuildParameters:
    """
    A context manager for building configuration objects.
    Variables must be explicitly assigned to the instance, but nested 
    builders are automatically attached to their parent upon exit.

    Args:
        frozen (bool): Defaults to True. When True, the object is locked 
            upon exiting the 'with' block, preventing accidental mutations. 
            If False, the object remains mutable.
            
            ⚠️ USE AT YOUR OWN RISK: If `frozen=False`, modifying a base 
            parameter later will NOT automatically update any dependent or 
            derived parameters. This builder evaluates calculations statically 
            at the time of execution; it does not create reactive bindings.

    Example:
        with BuildParameters(frozen=True) as p:
            p.radius = 1.5
            p.diameter = p.radius * 2

        # p.radius = 2.0  <-- Raises AttributeError (frozen)
        
        # If frozen=False, p.radius = 2.0 is allowed, but p.diameter 
        # will permanently remain 3.0.
    """
    
    # Class-level stack to keep track of nested context managers
    _stack: list['BuildParameters'] = []

    def __init__(self, frozen: bool = True):
        self._frozen = frozen
        self._is_building = False

    def __enter__(self):
        """Unlocks the instance and pushes it onto the context stack."""
        self._is_building = True
        BuildParameters._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Locks the instance, pops it from the stack, and auto-attaches to parent."""
        BuildParameters._stack.pop()
        self._is_building = False

        if exc_type is not None:
            return False

        if BuildParameters._stack:
            parent = BuildParameters._stack[-1]
            
            caller_frame = inspect.currentframe().f_back
            try:
                caller_locals = caller_frame.f_locals
                my_name = next(
                    (name for name, val in caller_locals.items() if val is self), 
                    None
                )
                
                if my_name:
                    setattr(parent, my_name, self)
            finally:
                del caller_frame 

        return False

    def __setattr__(self, name: str, value: Any) -> None:
        """Enforces the frozen state after the context manager exits."""
        if getattr(self, '_frozen', False) and not getattr(self, '_is_building', True):
            if not name.startswith('_'):
                raise AttributeError(f"Cannot assign to '{name}': {self.__class__.__name__} is frozen.")
        
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        core_attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        if not core_attrs:
            return f"<{self.__class__.__name__} (empty/active)>"
        
        attrs_str = ', '.join(f"{k}={v!r}" for k, v in core_attrs.items())
        return f"{self.__class__.__name__}({attrs_str})"
