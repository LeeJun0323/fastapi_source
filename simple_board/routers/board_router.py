from fastapi import APIRouter, HTTPException, status
from schemas.board import BoardUpdate, BoardCreate, BoardResponse, BoardPageResponse
from services.board import create, update, select_all, select_one, delete, recentPosts
from fastapi import Depends
from sqlalchemy.orm import Session
from repository.database import get_db
from exceptions.board import BoardNotFoundException
from core.dependencies import get_current_user
from repository.models.user import User
from exceptions.user import UserCredentialsException

board_router = APIRouter(tags=["Boards"])

# 최신글 조회 + GET : http://localhost:8000/boards/recents
@board_router.get("/recents", response_model=list[BoardResponse])
async def get_boards_recents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return recentPosts(db=db)


# 전체 조회 + GET : http://localhost:8000/boards
# 하나 조회 + GET : http://localhost:8000/boards/1
# 하나 수정 + PUT : http://localhost:8000/boards/1 + 수정데이터
# 하나 삭제 + DELETE : http://localhost:8000/boards/1
# 댓글 조회 + GET : http://localhost:8000/boards/1/comments

# 전체 조회 + GET : http://localhost:8000/boards
@board_router.get("", response_model=BoardPageResponse)
async def get_boards(db: Session = Depends(get_db), page: int=1, size:int = 10):
    result = select_all(db=db, page=page, size=size)
    return result

# 하나 조회 + GET : http://localhost:8000/boards/1
@board_router.get("/{id}", response_model=BoardResponse)
async def get_boards(id:int, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    try:
        board = select_one(db=db, id=id)
    except BoardNotFoundException:  
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="찾는 board가 없습니다.")
    return board

# # 댓글 조회 + GET : http://localhost:8000/boards/1/comments
# @board_router.get("/{id}/comments", response_model=list[Comment])
# async def get_board_comments(id:int):
#     return []

# 하나 수정 + PUT : http://localhost:8000/boards/1 + 수정데이터
@board_router.put("/{id}", response_model=dict)
async def put_board(id:int, update_board:BoardUpdate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    try:
        id = update(db=db, id=id,  data=update_board, current_user = current_user)
    except BoardNotFoundException:  
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="찾는 board가 없습니다.")
    return {"message": f"{id}번이 수정되었습니다."}

# 하나 삭제 + DELETE : http://localhost:8000/boards/1
@board_router.delete("/{id}", response_model=dict)
async def delete_board(id:int, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    try:
      id = delete(db=db, id=id, current_user = current_user)
    except BoardNotFoundException:  
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="찾는 board가 없습니다.")
    return {"message": f"{id}번이 삭제되었습니다."}

# 하나 추가 + POST : http://localhost:8000/boards/1
@board_router.post("", response_model=dict)
async def post_board(data:BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # boards => Board
    try:
        new_board = create(db=db, data=data, current_user = current_user)
    except UserCredentialsException:
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="유효하지 않은 사용자입니다."
       )
    return {"message": f'{new_board}번이 삽입되었습니다.'}

