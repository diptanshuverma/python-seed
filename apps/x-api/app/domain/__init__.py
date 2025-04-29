from .book.book_router import book_router
from .publisher.publisher_router import publisher_router
from .health.health_router import health_router
from .test.test_router import test_router


__all__ = ["book_router", "test_router", "health_router", "publisher_router"]
