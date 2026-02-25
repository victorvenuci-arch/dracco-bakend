import logging
from typing import Optional, Dict, Any, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.pacotes import Pacotes

logger = logging.getLogger(__name__)


# ------------------ Service Layer ------------------
class PacotesService:
    """Service layer for Pacotes operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: Dict[str, Any]) -> Optional[Pacotes]:
        """Create a new pacotes"""
        try:
            obj = Pacotes(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Created pacotes with id: {obj.id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating pacotes: {str(e)}")
            raise

    async def get_by_id(self, obj_id: int) -> Optional[Pacotes]:
        """Get pacotes by ID"""
        try:
            query = select(Pacotes).where(Pacotes.id == obj_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching pacotes {obj_id}: {str(e)}")
            raise

    async def get_list(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        query_dict: Optional[Dict[str, Any]] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated list of pacotess"""
        try:
            query = select(Pacotes)
            count_query = select(func.count(Pacotes.id))
            
            if query_dict:
                for field, value in query_dict.items():
                    if hasattr(Pacotes, field):
                        query = query.where(getattr(Pacotes, field) == value)
                        count_query = count_query.where(getattr(Pacotes, field) == value)
            
            count_result = await self.db.execute(count_query)
            total = count_result.scalar()

            if sort:
                if sort.startswith('-'):
                    field_name = sort[1:]
                    if hasattr(Pacotes, field_name):
                        query = query.order_by(getattr(Pacotes, field_name).desc())
                else:
                    if hasattr(Pacotes, sort):
                        query = query.order_by(getattr(Pacotes, sort))
            else:
                query = query.order_by(Pacotes.id.desc())

            result = await self.db.execute(query.offset(skip).limit(limit))
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
            }
        except Exception as e:
            logger.error(f"Error fetching pacotes list: {str(e)}")
            raise

    async def update(self, obj_id: int, update_data: Dict[str, Any]) -> Optional[Pacotes]:
        """Update pacotes"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Pacotes {obj_id} not found for update")
                return None
            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Updated pacotes {obj_id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating pacotes {obj_id}: {str(e)}")
            raise

    async def delete(self, obj_id: int) -> bool:
        """Delete pacotes"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Pacotes {obj_id} not found for deletion")
                return False
            await self.db.delete(obj)
            await self.db.commit()
            logger.info(f"Deleted pacotes {obj_id}")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting pacotes {obj_id}: {str(e)}")
            raise

    async def get_by_field(self, field_name: str, field_value: Any) -> Optional[Pacotes]:
        """Get pacotes by any field"""
        try:
            if not hasattr(Pacotes, field_name):
                raise ValueError(f"Field {field_name} does not exist on Pacotes")
            result = await self.db.execute(
                select(Pacotes).where(getattr(Pacotes, field_name) == field_value)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching pacotes by {field_name}: {str(e)}")
            raise

    async def list_by_field(
        self, field_name: str, field_value: Any, skip: int = 0, limit: int = 20
    ) -> List[Pacotes]:
        """Get list of pacotess filtered by field"""
        try:
            if not hasattr(Pacotes, field_name):
                raise ValueError(f"Field {field_name} does not exist on Pacotes")
            result = await self.db.execute(
                select(Pacotes)
                .where(getattr(Pacotes, field_name) == field_value)
                .offset(skip)
                .limit(limit)
                .order_by(Pacotes.id.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching pacotess by {field_name}: {str(e)}")
            raise