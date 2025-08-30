from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.db.models.subscription import StreamSubscription


class SubscriptionService:
    async def list_symbols(
        self,
        db: AsyncSession,
        user_id: str,
        stream_type: str,
        book: Optional[str] = None,
    ) -> list[str]:
        query = select(StreamSubscription.symbol).where(
            StreamSubscription.user_id == user_id,
            StreamSubscription.stream_type == stream_type,
            StreamSubscription.is_active,
        )
        if book is not None:
            query = query.where(StreamSubscription.book == book)
        result = await db.execute(query)
        return [row[0] for row in result.fetchall()]

    async def add_symbols(
        self,
        db: AsyncSession,
        user_id: str,
        stream_type: str,
        symbols: Iterable[str],
        book: Optional[str] = None,
        is_active: bool = True,
    ) -> int:
        added = 0
        for symbol in symbols:
            symbol_up = symbol.upper()
            existing = await db.execute(
                select(StreamSubscription).where(
                    StreamSubscription.user_id == user_id,
                    StreamSubscription.stream_type == stream_type,
                    StreamSubscription.symbol == symbol_up,
                    StreamSubscription.book == book,
                )
            )
            sub = existing.scalar_one_or_none()
            if sub:
                # Always activate when adding symbols to an active stream
                if not sub.is_active:
                    await db.execute(
                        update(StreamSubscription)
                        .where(StreamSubscription.id == sub.id)
                        .values(is_active=True)
                    )
                    added += 1
                continue
            db.add(
                StreamSubscription(
                    user_id=user_id,
                    stream_type=stream_type,
                    symbol=symbol_up,
                    book=book,
                    is_active=True,  # Always create as active when adding to stream
                )
            )
            added += 1
        if added:
            await db.commit()
        return added

    async def remove_symbols(
        self,
        db: AsyncSession,
        user_id: str,
        stream_type: str,
        symbols: Iterable[str],
        book: Optional[str] = None,
    ) -> int:
        sym_upper = [s.upper() for s in symbols]

        # Build the where clause
        where_clause = [
            StreamSubscription.user_id == user_id,
            StreamSubscription.stream_type == stream_type,
            StreamSubscription.symbol.in_(sym_upper),
        ]
        if book is not None:
            where_clause.append(StreamSubscription.book == book)

        # Deactivate instead of deleting
        result = await db.execute(
            update(StreamSubscription)
            .where(*where_clause)
            .values(is_active=False)
            .execution_options(synchronize_session=False)
        )
        await db.commit()
        return result.rowcount or 0
