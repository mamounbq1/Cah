"""
Base View Classes
Abstract base classes for all application views following MVC pattern
"""

from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any, Callable


class BaseView(ABC, ttk.Frame):
    """
    Abstract base class for all application views
    
    Provides:
    - Consistent lifecycle hooks
    - Event handling system
    - Data binding utilities
    - Navigation support
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """
        Initialize base view
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, style='TFrame')
        self.parent = parent
        self.controller = controller
        
        # View state
        self._is_initialized = False
        self._is_visible = False
        self._data: Dict[str, Any] = {}
        
        # Event handlers
        self._event_handlers: Dict[str, list] = {}
        
        # Lifecycle hooks
        self._on_create()
        self._build_ui()
        self._setup_bindings()
        self._on_ready()
        
        self._is_initialized = True
    
    def _on_create(self) -> None:
        """Called before UI building - override for setup"""
        pass
    
    @abstractmethod
    def _build_ui(self) -> None:
        """
        Build the user interface
        Must be implemented by subclasses
        """
        pass
    
    def _setup_bindings(self) -> None:
        """Setup event bindings - override if needed"""
        pass
    
    def _on_ready(self) -> None:
        """Called after UI is built - override for post-setup"""
        pass
    
    def show(self) -> None:
        """Show the view"""
        if not self._is_visible:
            self._on_show()
            self.tkraise()
            self._is_visible = True
            self._on_shown()
    
    def hide(self) -> None:
        """Hide the view"""
        if self._is_visible:
            self._on_hide()
            self.lower()
            self._is_visible = False
            self._on_hidden()
    
    def _on_show(self) -> None:
        """Called before view is shown - override if needed"""
        pass
    
    def _on_shown(self) -> None:
        """Called after view is shown - override if needed"""
        pass
    
    def _on_hide(self) -> None:
        """Called before view is hidden - override if needed"""
        pass
    
    def _on_hidden(self) -> None:
        """Called after view is hidden - override if needed"""
        pass
    
    def destroy(self) -> None:
        """Clean up and destroy view"""
        self._on_destroy()
        super().destroy()
    
    def _on_destroy(self) -> None:
        """Called before view is destroyed - override for cleanup"""
        pass
    
    def set_data(self, key: str, value: Any) -> None:
        """
        Set data in view state
        
        Args:
            key: Data key
            value: Data value
        """
        self._data[key] = value
        self._on_data_changed(key, value)
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get data from view state
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Data value
        """
        return self._data.get(key, default)
    
    def _on_data_changed(self, key: str, value: Any) -> None:
        """
        Called when data changes - override for reactive updates
        
        Args:
            key: Data key that changed
            value: New value
        """
        pass
    
    def register_handler(self, event_name: str, handler: Callable) -> None:
        """
        Register an event handler
        
        Args:
            event_name: Name of the event
            handler: Handler function
        """
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)
    
    def emit_event(self, event_name: str, *args, **kwargs) -> None:
        """
        Emit an event to all registered handlers
        
        Args:
            event_name: Name of the event
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(*args, **kwargs)
    
    def navigate_to(self, view_name: str, **params) -> None:
        """
        Navigate to another view
        
        Args:
            view_name: Name of the view to navigate to
            **params: Parameters to pass to the view
        """
        if hasattr(self.controller, 'show_view'):
            self.controller.show_view(view_name, **params)
    
    @property
    def is_visible(self) -> bool:
        """Check if view is currently visible"""
        return self._is_visible
    
    @property
    def is_initialized(self) -> bool:
        """Check if view is initialized"""
        return self._is_initialized


class ModalView(BaseView):
    """
    Base class for modal/dialog views
    
    Features:
    - Modal behavior (blocks parent window)
    - Result handling
    - OK/Cancel pattern
    """
    
    def __init__(self, parent: tk.Widget, controller: Any, title: str = ""):
        """
        Initialize modal view
        
        Args:
            parent: Parent widget
            controller: Application controller
            title: Modal title
        """
        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Result handling
        self._result: Optional[Any] = None
        self._result_callback: Optional[Callable] = None
        
        # Center the modal
        self._center_window()
        
        # Initialize base view in the toplevel
        super().__init__(self.window, controller)
        self.pack(fill='both', expand=True)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def _center_window(self) -> None:
        """Center the modal window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_result_callback(self, callback: Callable[[Any], None]) -> None:
        """
        Set callback for result handling
        
        Args:
            callback: Function to call with result
        """
        self._result_callback = callback
    
    def ok(self, result: Any = None) -> None:
        """
        Close modal with OK result
        
        Args:
            result: Result value
        """
        self._result = result
        if self._result_callback:
            self._result_callback(result)
        self.close()
    
    def cancel(self) -> None:
        """Close modal with cancel result"""
        self._result = None
        if self._result_callback:
            self._result_callback(None)
        self.close()
    
    def close(self) -> None:
        """Close the modal"""
        self.window.grab_release()
        self.window.destroy()
    
    def wait_for_result(self) -> Optional[Any]:
        """
        Wait for modal to close and return result
        
        Returns:
            Modal result
        """
        self.window.wait_window()
        return self._result
