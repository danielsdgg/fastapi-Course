from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash



router = APIRouter(
    prefix='/user',
    tags=['Users']
)





@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id:int, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return user

@router.post('/', response_model=schemas.ShowUser)
def create_user(request : schemas.User, db:Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db : Session = Depends(database.get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return 'User deleted successfully'