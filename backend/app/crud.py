from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import User, Transaction, Category, TransactionType
from app.schemas import UserCreate, UserUpdate, TransactionCreate, TransactionUpdate, CategoryCreate, CategoryUpdate
from app.security import get_password_hash, verify_password


# User CRUD
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Transaction CRUD
def get_transactions(
    db: Session, user_id: int, skip: int = 0, limit: int = 100, type_filter: Optional[str] = None, category_filter: Optional[str] = None
) -> List[Transaction]:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if type_filter and type_filter != "all":
        query = query.filter(Transaction.type == type_filter)
    if category_filter and category_filter != "all":
        query = query.filter(Transaction.category == category_filter)
    return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()


def get_transaction_by_id(db: Session, transaction_id: int, user_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Transaction:
    db_transaction = Transaction(
        **transaction.model_dump(),
        user_id=user_id,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, user_id: int, transaction_update: TransactionUpdate) -> Optional[Transaction]:
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return None
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return False
    db.delete(db_transaction)
    db.commit()
    return True


def get_transaction_summary(db: Session, user_id: int) -> dict:
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(total_income - total_expenses),
    }


# Category CRUD
def get_categories(db: Session, user_id: int, type_filter: Optional[str] = None) -> List[Category]:
    query = db.query(Category).filter(Category.user_id == user_id)
    if type_filter and type_filter != "all":
        query = query.filter(Category.type == type_filter)
    return query.all()


def get_category_by_id(db: Session, category_id: int, user_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def create_category(db: Session, category: CategoryCreate, user_id: int) -> Category:
    db_category = Category(
        **category.model_dump(),
        user_id=user_id,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, user_id: int, category_update: CategoryUpdate) -> Optional[Category]:
    db_category = get_category_by_id(db, category_id, user_id)
    if not db_category:
        return None
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    db_category = get_category_by_id(db, category_id, user_id)
    if not db_category:
        return False
    db.delete(db_category)
    db.commit()
    return True


# Default categories for new users
DEFAULT_CATEGORIES = [
    {"name": "Salary", "type": TransactionType.INCOME, "color": "#10b981", "icon": "💼", "is_default": True},
    {"name": "Freelance", "type": TransactionType.INCOME, "color": "#059669", "icon": "💻", "is_default": True},
    {"name": "Investments", "type": TransactionType.INCOME, "color": "#047857", "icon": "📈", "is_default": True},
    {"name": "Food", "type": TransactionType.EXPENSE, "color": "#ef4444", "icon": "🍔", "is_default": True},
    {"name": "Transport", "type": TransactionType.EXPENSE, "color": "#f97316", "icon": "🚌", "is_default": True},
    {"name": "Entertainment", "type": TransactionType.EXPENSE, "color": "#ec4899", "icon": "🎮", "is_default": True},
    {"name": "Shopping", "type": TransactionType.EXPENSE, "color": "#8b5cf6", "icon": "🛍️", "is_default": True},
    {"name": "Bills", "type": TransactionType.EXPENSE, "color": "#6366f1", "icon": "📄", "is_default": True},
    {"name": "Healthcare", "type": TransactionType.EXPENSE, "color": "#14b8a6", "icon": "🏥", "is_default": True},
    {"name": "Education", "type": TransactionType.EXPENSE, "color": "#06b6d4", "icon": "📚", "is_default": True},
]


def create_default_categories(db: Session, user_id: int) -> List[Category]:
    categories = []
    for cat_data in DEFAULT_CATEGORIES:
        db_category = Category(
            **cat_data,
            user_id=user_id,
        )
        db.add(db_category)
        categories.append(db_category)
    db.commit()
    for cat in categories:
        db.refresh(cat)
    return categories