import logging
from typing import Optional, Dict, Any, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.cidades import Cidades

logger = logging.getLogger(__name__)


# ------------------ Service Layer ------------------
class CidadesService:
    """Service layer for Cidades operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: Dict[str, Any]) -> Optional[Cidades]:
        """Create a new cidades"""
        try:
            obj = Cidades(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Created cidades with id: {obj.id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating cidades: {str(e)}")
            raise

    async def get_by_id(self, obj_id: int) -> Optional[Cidades]:
        """Get cidades by ID"""
        try:
            query = select(Cidades).where(Cidades.id == obj_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching cidades {obj_id}: {str(e)}")
            raise

    async def get_list(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        query_dict: Optional[Dict[str, Any]] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated list of cidadess"""
        try:
            query = select(Cidades)
            count_query = select(func.count(Cidades.id))
            
            if query_dict:
                for field, value in query_dict.items():
                    if hasattr(Cidades, field):
                        query = query.where(getattr(Cidades, field) == value)
                        count_query = count_query.where(getattr(Cidades, field) == value)
            
            count_result = await self.db.execute(count_query)
            total = count_result.scalar()

            if sort:
                if sort.startswith('-'):
                    field_name = sort[1:]
                    if hasattr(Cidades, field_name):
                        query = query.order_by(getattr(Cidades, field_name).desc())
                else:
                    if hasattr(Cidades, sort):
                        query = query.order_by(getattr(Cidades, sort))
            else:
                query = query.order_by(Cidades.id.desc())

            result = await self.db.execute(query.offset(skip).limit(limit))
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
            }
        except Exception as e:
            logger.error(f"Error fetching cidades list: {str(e)}")
            raise

    async def update(self, obj_id: int, update_data: Dict[str, Any]) -> Optional[Cidades]:
        """Update cidades"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Cidades {obj_id} not found for update")
                return None
            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Updated cidades {obj_id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating cidades {obj_id}: {str(e)}")
            raise

    async def delete(self, obj_id: int) -> bool:
        """Delete cidades"""
        try:
            obj = await self.get_by_id(obj_id)
            if not obj:
                logger.warning(f"Cidades {obj_id} not found for deletion")
                return False
            await self.db.delete(obj)
            await self.db.commit()
            logger.info(f"Deleted cidades {obj_id}")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting cidades {obj_id}: {str(e)}")
            raise

    async def get_by_field(self, field_name: str, field_value: Any) -> Optional[Cidades]:
        """Get cidades by any field"""
        try:
            if not hasattr(Cidades, field_name):
                raise ValueError(f"Field {field_name} does not exist on Cidades")
            result = await self.db.execute(
                select(Cidades).where(getattr(Cidades, field_name) == field_value)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching cidades by {field_name}: {str(e)}")
            raise

    async def list_by_field(
        self, field_name: str, field_value: Any, skip: int = 0, limit: int = 20
    ) -> List[Cidades]:
        """Get list of cidadess filtered by field"""
        try:
            if not hasattr(Cidades, field_name):
                raise ValueError(f"Field {field_name} does not exist on Cidades")
            result = await self.db.execute(
                select(Cidades)
                .where(getattr(Cidades, field_name) == field_value)
                .offset(skip)
                .limit(limit)
                .order_by(Cidades.id.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching cidadess by {field_name}: {str(e)}")
            raise