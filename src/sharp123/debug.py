import sys
from ocp_vscode import show


class DebugMixin:
    """Mixin that captures method locals and pipes them into ocp_vscode."""

    def capture_debug_locals(self, frame_depth: int = 1):
        """Captures local variables from the calling frame (e.g. inside __init__)."""
        caller_locals = sys._getframe(frame_depth).f_locals

        # Filter out internal/boilerplate variables
        skip_keys = {"self", "p", "__class__", "builder", "kwargs"}
        self._debug_locals = {
            k: v
            for k, v in caller_locals.items()
            if not k.startswith("_") and k not in skip_keys
        }

    def show_debug(
        self,
        include: list[str] = None,
        exclude: list[str] = None,
        **show_kwargs,
    ):
        """Pipes captured intermediate variables into ocp_vscode show()."""
        if not hasattr(self, "_debug_locals") or not self._debug_locals:
            print(
                f"[{self.__class__.__name__}] No debug locals stored. Call self.capture_debug_locals() inside __init__."
            )
            return

        objs = []
        names = []

        for name, val in self._debug_locals.items():
            if exclude and name in exclude:
                continue
            if include and name not in include:
                continue
            objs.append(val)
            names.append(name)

        if objs:
            show(*objs, names=names, **show_kwargs)