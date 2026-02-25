import logging
from typing import Optional, Dict, Any, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.bases import Bases

logger = logging.getLogger(__name__)


# ------------------ Service Layer ------------------
class BasesService:
    """Service layer for Bases operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: Dict[str, Any]) -> Optional[Bases]:
        """Create a new bases"""
        try:
            obj = Bases(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Created bases with id: {obj.id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating bases: {str(e)}")
            raise

    async def get_by_id(self, obj_id: int) -> Optional[Bases]:
        """Get bases by ID"""
        try:
            query = select(Bases).where(Bases.id == obj_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching bases {obj_id}: {str(e)}")
            raise

    async def get_list(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        query_dict: Optional[Dict[str, Any]] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated list of basess"""
        try:
            query = select(Bases)
            count_query = select(func.count(Bases.id))
            
            if query_dict:
                for field, value in query_dict.items():
                    if hasattr(Bases, field):
                        query = query.where(getattr(Bases, field) == value)
                        count_query = count_query.where(getattr(Bases, field) == value)
            
            count_result = await self.db.execute(count_query)
            total = count_result.scalar()

            if sort:
                if sort.startswith('-'):
                    field_name = sort[1:]
                    if hasattr(Bases, field_name):
                        query = query.order_by(getattr(Bases, field_name).desc())
                else:
                    if hasattr(Bases, sort):
                        query = query.order_by(getattr(Bases, sort))
            else:
                query = query.order_by(Bases.id.desc())

            result = await self.db.execute(query.offset(skip).limit(limit))
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
            }
        except Exception as e:
            logger.error(f"Error fetching bases list: {str(e)}")
            raise

    async def update(self, obj_id: int, update_data: Dict[str, Any]) -> Optional[Bases]:
        """Update bases"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Bases {obj_id} not found for update")
                return None
            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Updated bases {obj_id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating bases {obj_id}: {str(e)}")
            raise

    async def delete(self, obj_id: int) -> bool:
        """Delete bases"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Bases {obj_id} not found for deletion")
                return False
            await self.db.delete(obj)
            await self.db.commit()
            logger.info(f"Deleted bases {obj_id}")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting bases {obj_id}: {str(e)}")
            raise

    async def get_by_field(self, field_name: str, field_value: Any) -> Optional[Bases]:
        """Get bases by any field"""
        try:
            if not hasattr(Bases, field_name):
                raise ValueError(f"Field {field_name} does not exist on Bases")
            result = await self.db.execute(
                select(Bases).where(getattr(Bases, field_name) == field_value)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching bases by {field_name}: {str(e)}")
            raise

    async def list_by_field(
        self, field_name: str, field_value: Any, skip: int = 0, limit: int = 20
    ) -> List[Bases]:
        """Get list of basess filtered by field"""
        try:
            if not hasattr(Bases, field_name):
                raise ValueError(f"Field {field_name} does not exist on Bases")
            result = await self.db.execute(
                select(Bases)
                .where(getattr(Bases, field_name) == field_value)
                .offset(skip)
                .limit(limit)
                .order_by(Bases.id.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching basess by {field_name}: {str(e)}")
            raise