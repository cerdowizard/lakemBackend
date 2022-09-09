from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.utils import jwt_encoder
from api import models, schema
from api.utils.database import get_db

router_tran = APIRouter(
    prefix="/api/v1/auth/transactions"
)


@router_tran.get("/get/all/transaction")
async def get_all_transactions(db: Session = Depends(get_db),
                               current_user: int = Depends(jwt_encoder.get_current_user)):
    return db.query(models.Transaction).all()


@router_tran.post("/create/transaction", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_create: schema.TransctionInfoIn, db: Session = Depends(get_db)):
    create_transaction_new = models.Transaction(
        **transaction_create.dict()
    )
    db.add(create_transaction_new)
    db.commit()
    db.refresh(create_transaction_new)
    return create_transaction_new


@router_tran.get('/get/transaction/{id}')
async def get_transaction_by_id(id: int, db: Session = Depends(get_db),
                                current_user: int = Depends(jwt_encoder.get_current_user)):
    get_transaction_by_id = db.query(models.Transaction).filter(models.Transaction.id == id).first()
    if not get_transaction_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with id '{id}' not found")
    return get_transaction_by_id
