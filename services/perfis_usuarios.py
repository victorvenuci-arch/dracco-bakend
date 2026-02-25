import logging
from typing import Optional, Dict, Any, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.perfis_usuarios import Perfis_usuarios

logger = logging.getLogger(__name__)


# ------------------ Service Layer ------------------
class Perfis_usuariosService:
    """Service layer for Perfis_usuarios operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[Perfis_usuarios]:
        """Create a new perfis_usuarios"""
        try:
            if user_id:
                data['user_id'] = user_id
            obj = Perfis_usuarios(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Created perfis_usuarios with id: {obj.id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating perfis_usuarios: {str(e)}")
            raise

    async def check_ownership(self, obj_id: int, user_id: str) -> bool:
        """Check if user owns this record"""
        try:
            obj = await self.get_by_id(obj_id, user_id=user_id)
            return obj is not None
        except Exception as e:
            logger.error(f"Error checking ownership for perfis_usuarios {obj_id}: {str(e)}")
            return False

    async def get_by_id(self, obj_id: int, user_id: Optional[str] = None) -> Optional[Perfis_usuarios]:
        """Get perfis_usuarios by ID (user can only see their own records)"""
        try:
            query = select(Perfis_usuarios).where(Perfis_usuarios.id == obj_id)
            if user_id:
                query = query.where(Perfis_usuarios.user_id == user_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching perfis_usuarios {obj_id}: {str(e)}")
            raise

    async def get_list(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        user_id: Optional[str] = None,
        query_dict: Optional[Dict[str, Any]] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated list of perfis_usuarioss (user can only see their own records)"""
        try:
            query = select(Perfis_usuarios)
            count_query = select(func.count(Perfis_usuarios.id))
            
            if user_id:
                query = query.where(Perfis_usuarios.user_id == user_id)
                count_query = count_query.where(Perfis_usuarios.user_id == user_id)
            
            if query_dict:
                for field, value in query_dict.items():
                    if hasattr(Perfis_usuarios, field):
                        query = query.where(getattr(Perfis_usuarios, field) == value)
                        count_query = count_query.where(getattr(Perfis_usuarios, field) == value)
            
            count_result = await self.db.execute(count_query)
            total = count_result.scalar()

            if sort:
                if sort.startswith('-'):
                    field_name = sort[1:]
                    if hasattr(Perfis_usuarios, field_name):
                        query = query.order_by(getattr(Perfis_usuarios, field_name).desc())
                else:
                    if hasattr(Perfis_usuarios, sort):
                        query = query.order_by(getattr(Perfis_usuarios, sort))
            else:
                query = query.order_by(Perfis_usuarios.id.desc())

            result = await self.db.execute(query.offset(skip).limit(limit))
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "skip": skip,
                "limit": limit,
            }
        except Exception as e:
            logger.error(f"Error fetching perfis_usuarios list: {str(e)}")
            raise

    async def update(self, obj_id: int, update_data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[Perfis_usuarios]:
        """Update perfis_usuarios (requires ownership)"""
        try:
            obj = await self.get_by_id(obj_id, user_id=user_id)
            if not obj:
                logger.warning(f"Perfis_usuarios {obj_id} not found for update")
                return None
            for key, value in update_data.items():
                if hasattr(obj, key) and key != 'user_id':
                    setattr(obj, key, value)

            await self.db.commit()
            await self.db.refresh(obj)
            logger.info(f"Updated perfis_usuarios {obj_id}")
            return obj
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating perfis_usuarios {obj_id}: {str(e)}")
            raise

    async def delete(self, obj_id: int, user_id: Optional[str] = None) -> bool:
        """Delete perfis_usuarios (requires ownership)"""
        try:
            obj = await self.get_by_id(obj_id, user_id=user_id)
            if not obj:
                logger.warning(f"Perfis_usuarios {obj_id} not found for deletion")
                return False
            await self.db.delete(obj)
            await self.db.commit()
            logger.info(f"Deleted perfis_usuarios {obj_id}")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting perfis_usuarios {obj_id}: {str(e)}")
            raise

    async def get_by_field(self, field_name: str, field_value: Any) -> Optional[Perfis_usuarios]:
        """Get perfis_usuarios by any field"""
        try:
            if not hasattr(Perfis_usuarios, field_name):
                raise ValueError(f"Field {field_name} does not exist on Perfis_usuarios")
            result = await self.db.execute(
                select(Perfis_usuarios).where(getattr(Perfis_usuarios, field_name) == field_value)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching perfis_usuarios by {field_name}: {str(e)}")
            raise

    async def list_by_field(
        self, field_name: str, field_value: Any, skip: int = 0, limit: int = 20
    ) -> List[Perfis_usuarios]:
        """Get list of perfis_usuarioss filtered by field"""
        try:
            if not hasattr(Perfis_usuarios, field_name):
                raise ValueError(f"Field {field_name} does not exist on Perfis_usuarios")
            result = await self.db.execute(
                select(Perfis_usuarios)
                .where(getattr(Perfis_usuarios, field_name) == field_value)
                .offset(skip)
                .limit(limit)
                .order_by(Perfis_usuarios.id.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching perfis_usuarioss by {field_name}: {str(e)}")
            raise