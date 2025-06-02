import uuid
from fastapi import APIRouter,Depends,HTTPException,status,Body
from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schema.transactions import Transactions
from decimal import Decimal
test:APIRouter = APIRouter()


@test.post("/create_transaction")
async def create_transaction(
    data:dict,
    db:AsyncSession=Depends(get_db)
):
    try:
        transaction = Transactions(
            transaction_id=str(uuid.uuid4()),
            asset_name=data.get("asset_name"),
            asset_value=data.get("asset_value")
        )
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return {"message":"Transaction Successfull!","status":200,"transaction":transaction}
    except Exception as e:
        print(e)

@test.get("/read")
async def read(
    db:AsyncSession=Depends(get_db)
):
    try:
        result = await db.execute(select(Transactions))
        transactions = result.scalars().all()
        return {"status":200,"transactions":transactions}
    except Exception as e:
        print(e)


@test.patch("/update_transaction/{transaction_id}")
async def update_transaction(
    transaction_id: str,
    asset_value: Decimal,
    db: AsyncSession = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"Updating transaction {transaction_id} with value: {asset_value}")
    
    try:
        # Update the transaction value directly in the database
        stmt_update = (
            update(Transactions)
            .where(Transactions.transaction_id == transaction_id)
            .values(
                asset_value=Transactions.asset_value + Decimal(asset_value)
            )
            .returning(Transactions)
        )
        
        result = await db.execute(stmt_update)
        updated_transaction = result.scalar_one_or_none()
        
        if not updated_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
            
        await db.commit()
        
        return {
            "status": 200,
            "message": "Transaction updated successfully",
            "transaction": updated_transaction
        }
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=400, detail="Invalid asset value")
    except Exception as e:
        logger.error(f"Error updating transaction: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")