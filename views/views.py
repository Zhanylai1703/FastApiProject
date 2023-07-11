from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from core.db import get_db

from models.models import City, Category
from shcemas.shemas import CityBase, CategoryBase

session = sessionmaker(autocommit=False, autoflush=False)

router = APIRouter(
    # prefix='/nashol',
    tags=['Nashol']
)


@router.get("/")
def hello():
    return "Hello world"


@router.post('/city', status_code=status.HTTP_201_CREATED)
def add_city(payload: CityBase, db: Session = Depends(get_db)):
    new_city = City(**payload.dict())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get('/cities', status_code=status.HTTP_200_OK)
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities


@router.get('/city/{city_id}', status_code=status.HTTP_200_OK)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).get(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail='City not found')
    return city


@router.put('/city/{city_id}', status_code=status.HTTP_201_CREATED)
def update_city(city_id: int, payload: CityBase, db: Session = Depends(get_db)):
    city = db.query(City).get(city_id)
    if city is None:
       raise HTTPException(status_code=404, detail='City not found')
    city.name = payload.name
    db.commit()
    db.refresh(city)
    return city


@router.post('/category', status_code=status.HTTP_201_CREATED)
def add_category(payload: CategoryBase, db: Session = Depends(get_db)):
    new_category = Category(**payload.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get('/categories', status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.put('/category/{category_id}', status_code=status.HTTP_201_CREATED)
def put_category(
        category_id: int,
        payload: CategoryBase,
        db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    category.name = payload.name
    db.commit()
    db.refresh(category)
    return category


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return category


@router.delete('/city/{city_id}')
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).get(city_id)
    if not city:
        raise HTTPException(status_code=404, detail='City not found')
    db.delete(city)
    db.commit()
    return {'message': 'City deleted successfully'}

