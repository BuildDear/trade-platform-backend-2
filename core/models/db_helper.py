from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        """
        Initializes DatabaseHelper class with a database URL and an option to enable or disable echoing SQL queries.

        :param url: Database connection URL.
        :param echo: Boolean indicating whether to echo SQL queries.
        """
        # Creating an asynchronous engine using create_async_engine method from sqlalchemy.ext.asyncio module
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Creating a session factory using async_sessionmaker from sqlalchemy.ext.asyncio module
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        Creates a scoped session for the current task.

        :return: Scoped session for the current task.
        """
        # Creating a scoped session using async_scoped_session from sqlalchemy.ext.asyncio module
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,  # Assigning current task as the scope function
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Asynchronous context manager for managing sessions.

        :return: Asynchronous session object.
        """
        # Creating an asynchronous session using self.session_factory context manager
        async with self.session_factory() as session:
            yield session  # Yielding the session
            await session.close()  # Closing the session after use

    async def scoped_session_dependency(self) -> AsyncSession:
        """
        Asynchronous generator function for scoped sessions.

        :return: Asynchronous session object.
        """
        # Getting a scoped session
        session = self.get_scoped_session()
        yield session  # Yielding the session
        await session.close()  # Closing the session after use


# Creating an instance of DatabaseHelper class with database URL and echo settings from the settings module
db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
