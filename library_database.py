"""
Library Database 
Công nghệ: Python & SQLAlchemy ORM & MySQL
"""

import sys
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func, or_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# --- 1. CONNECTION CONFIGURATION ---
DATABASE_URI = 'mysql+mysqlconnector://librarian_user:StrongPass_Lib2026!@127.0.0.1:3306/lib'

try:
    engine = create_engine(DATABASE_URI, echo=False, connect_args={"use_pure": True})
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f"\n[LỖI] Không thể kết nối CSDL: {e}")
    sys.exit()

Base = declarative_base()

# --- 2. MODELS ---
class Category(Base):
    __tablename__ = 'Categories'
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(100), nullable=False)

class Author(Base):
    __tablename__ = 'Authors'
    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    AuthorName = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'Books'
    BookID = Column(Integer, primary_key=True, autoincrement=True)
    BookName = Column(String(255), nullable=False)
    AuthorID = Column(Integer, ForeignKey('Authors.AuthorID'))
    PublishYear = Column(Integer)
    AvailableQuantity = Column(Integer) 
    TotalQuantity = Column(Integer)     
    CategoryID = Column(Integer, ForeignKey('Categories.CategoryID'))
    
    author = relationship("Author", back_populates="books")
    category = relationship("Category")

class Reader(Base):
    __tablename__ = 'Readers'
    ReaderID = Column(Integer, primary_key=True, autoincrement=True)
    ReaderName = Column(String(100), nullable=False)
    Address = Column(String(255))
    PhoneNumber = Column(String(15))

class Borrowing(Base):
    __tablename__ = 'Borrowing'
    BorrowID = Column(Integer, primary_key=True, autoincrement=True)
    ReaderID = Column(Integer, ForeignKey('Readers.ReaderID'))
    BookID = Column(Integer, ForeignKey('Books.BookID'))
    BorrowDate = Column(Date)
    ReturnDate = Column(Date)
    
    book = relationship("Book")
    reader = relationship("Reader")


# ==========================================
# MODULE 1: BOOK MANAGEMENT 
# ==========================================
def view_all_books():
    print("\n--- DANH SÁCH TOÀN BỘ SÁCH ---")
    books = session.query(Book).join(Author).join(Category).all()
    if not books:
        print("Kho sách hiện đang trống.")
        return
    for b in books:
        print(f"ID: {b.BookID:<3} | Tựa: {b.BookName[:30]:<30} | Tác giả: {b.author.AuthorName[:20]:<20} | Kho: {b.AvailableQuantity}/{b.TotalQuantity}")

def search_books():
    keyword = input("Nhập tên sách hoặc tác giả: ")
    results = session.query(Book).join(Author).filter(
        or_(Book.BookName.ilike(f"%{keyword}%"), Author.AuthorName.ilike(f"%{keyword}%"))
    ).all()
    
    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    if not results: print("Không tìm thấy sách!")
    for b in results:
        print(f"ID: {b.BookID} | Sách: {b.BookName} | Tác giả: {b.author.AuthorName} | Kho: {b.AvailableQuantity}/{b.TotalQuantity}")

def add_book():
    title = input("Tựa sách: ").strip()
    author_name = input("Tên tác giả: ").strip()
    category_name = input("Tên thể loại: ").strip()
    try:
        year = int(input("Năm xuất bản: "))
        qty = int(input("Số lượng: "))
        
        author = session.query(Author).filter(Author.AuthorName.ilike(author_name)).first()
        if not author:
            author = Author(AuthorName=author_name)
            session.add(author)
            session.flush()
            
        category = session.query(Category).filter(Category.CategoryName.ilike(category_name)).first()
        if not category:
            category = Category(CategoryName=category_name)
            session.add(category)
            session.flush()
            
        existing = session.query(Book).filter(Book.BookName.ilike(title), Book.AuthorID == author.AuthorID).first()
        if existing:
            print("❌ Lỗi: Sách này đã tồn tại!")
            session.rollback()
            return

        new_book = Book(BookName=title, AuthorID=author.AuthorID, CategoryID=category.CategoryID, PublishYear=year, AvailableQuantity=qty, TotalQuantity=qty)
        session.add(new_book)
        session.commit()
        print(f"✅ Đã thêm sách ID {new_book.BookID}!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        session.rollback()

def edit_book():
    try:
        b_id = int(input("Nhập ID sách cần sửa: "))
        book = session.query(Book).filter(Book.BookID == b_id).first()
        if not book:
            print("❌ Không tìm thấy sách!")
            return
            
        print(f"Đang sửa: {book.BookName} (Năm: {book.PublishYear}, Tổng: {book.TotalQuantity})")
        new_name = input("Tựa sách mới (bỏ trống để giữ nguyên): ").strip()
        new_year = input("Năm XB mới (bỏ trống để giữ nguyên): ").strip()
        new_qty = input("Tổng số lượng mới (bỏ trống để giữ nguyên): ").strip()

        if new_name: book.BookName = new_name
        if new_year: book.PublishYear = int(new_year)
        if new_qty:
            new_total = int(new_qty)
            delta = new_total - book.TotalQuantity
            book.TotalQuantity = new_total
            book.AvailableQuantity += delta
            if book.AvailableQuantity < 0:
                print("❌ Lỗi: Số lượng mới thấp hơn số sách đang cho mượn!")
                session.rollback()
                return

        session.commit()
        print("✅ Đã cập nhật sách thành công!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        session.rollback()

def delete_book():
    try:
        b_id = int(input("Nhập ID sách cần xóa: "))
        book = session.query(Book).filter(Book.BookID == b_id).first()
        if not book:
            print("❌ Không tìm thấy sách!")
            return
            
        history = session.query(Borrowing).filter(Borrowing.BookID == b_id).first()
        if history:
            print("❌ Từ chối: Sách này đang có lịch sử mượn/trả. Không thể xóa để bảo toàn dữ liệu báo cáo!")
            return
            
        confirm = input(f"Bạn có chắc muốn xóa cuốn '{book.BookName}'? (y/n): ")
        if confirm.lower() == 'y':
            session.delete(book)
            session.commit()
            print("✅ Đã xóa sách thành công!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        session.rollback()


# ==========================================
# MODULE 2: AUTHOR AND CATEGORIES
# ==========================================
def view_authors_cats():
    print("\n--- DANH SÁCH TÁC GIẢ ---")
    for a in session.query(Author).all(): print(f"ID: {a.AuthorID:<3} | Tên: {a.AuthorName}")
    print("\n--- DANH SÁCH THỂ LOẠI ---")
    for c in session.query(Category).all(): print(f"ID: {c.CategoryID:<3} | Tên: {c.CategoryName}")

def edit_author():
    try:
        a_id = int(input("Nhập ID tác giả cần sửa: "))
        author = session.query(Author).filter(Author.AuthorID == a_id).first()
        if author:
            new_name = input(f"Đổi tên '{author.AuthorName}' thành: ")
            author.AuthorName = new_name
            session.commit()
            print("✅ Thành công!")
        else: print("❌ Không tìm thấy!")
    except Exception as e: session.rollback()


# ==========================================
# MODULE 3: READER AND BORROWING 
# ==========================================
def view_all_readers():
    print("\n--- DANH SÁCH ĐỘC GIẢ ---")
    readers = session.query(Reader).all()
    if not readers:
        print("Chưa có độc giả nào.")
        return
    for r in readers:
        print(f"ID: {r.ReaderID:<3} | Tên: {r.ReaderName:<20} | SĐT: {r.PhoneNumber}")

def add_reader():
    name = input("Tên độc giả: ")
    session.add(Reader(ReaderName=name, Address=input("Địa chỉ: "), PhoneNumber=input("SĐT: ")))
    session.commit()
    print("✅ Đã thêm độc giả!")

def borrow_book():
    r_id = input("ID Độc giả: ")
    b_id = input("ID Sách: ")
    book = session.query(Book).filter(Book.BookID == b_id).first()
    if book and book.AvailableQuantity > 0:
        session.add(Borrowing(ReaderID=r_id, BookID=b_id, BorrowDate=date.today()))
        session.commit()
        print(f"✅ Đã cho mượn cuốn '{book.BookName}'. (Số lượng trong kho tự động giảm)")
    else: print("❌ Sách không tồn tại hoặc đã hết!")

def return_book():
    borrow_id = input("ID Mượn sách (Borrow ID): ")
    record = session.query(Borrowing).filter(Borrowing.BorrowID == borrow_id, Borrowing.ReturnDate == None).first()
    if record:
        record.ReturnDate = date.today()
        session.commit()
        print("✅ Đã nhận trả sách! (Số lượng trong kho tự động tăng lên)")
    else: print("❌ Mã mượn không hợp lệ hoặc sách đã được trả!")


# ==========================================
# MODULE 4:(REPORTS)
# ==========================================
def currently_borrowed():
    print("\n--- SÁCH ĐANG ĐƯỢC MƯỢN ---")
    records = session.query(Borrowing).filter(Borrowing.ReturnDate == None).all()
    if not records: print("Không có sách nào đang được mượn.")
    for r in records:
        print(f"Mã Mượn: {r.BorrowID} | Độc giả: {r.reader.ReaderName} | Sách: {r.book.BookName} | Ngày mượn: {r.BorrowDate}")

def overdue_report():
    print("\n--- SÁCH QUÁ HẠN (>14 NGÀY) ---")
    records = session.query(Borrowing).filter(Borrowing.ReturnDate == None, func.datediff(func.current_date(), Borrowing.BorrowDate) > 14).all()
    if not records: print("Tuyệt vời, không có sách quá hạn!")
    for r in records:
        days = (date.today() - r.BorrowDate).days - 14
        print(f"Mã Mượn: {r.BorrowID} | Độc giả: {r.reader.ReaderName} | Sách: {r.book.BookName} | Quá hạn: {days} ngày")

def view_statistics():
    print("\n" + "="*45 + "\n DASHBOARD THỐNG KÊ THƯ VIỆN\n" + "="*45)
    
    # 1. Thống kê Sách
    total_books = session.query(func.sum(Book.TotalQuantity)).scalar() or 0
    avail_books = session.query(func.sum(Book.AvailableQuantity)).scalar() or 0
    borrowed_books = total_books - avail_books
    book_pct = (borrowed_books / total_books * 100) if total_books > 0 else 0
    
    print(f"📚 TỔNG KHO SÁCH: {total_books} cuốn")
    print(f"   -> Đang nằm trên kệ: {avail_books} cuốn")
    print(f"   -> Đang được độc giả mượn: {borrowed_books} cuốn")
    print(f"   -> Tỷ lệ sách rời khỏi thư viện: {book_pct:.1f}%\n")
    
    # 2. Thống kê Độc giả
    total_readers = session.query(Reader).count()
    active_readers = session.query(Borrowing.ReaderID).filter(Borrowing.ReturnDate == None).distinct().count()
    reader_pct = (active_readers / total_readers * 100) if total_readers > 0 else 0
    
    print(f"👤 TỔNG SỐ ĐỘC GIẢ ĐÃ ĐĂNG KÝ: {total_readers} người")
    print(f"   -> Số người đang cầm sách: {active_readers} người")
    print(f"   -> Tỷ lệ người dùng hoạt động: {reader_pct:.1f}%")
    print("="*45)


# ============
# (MAIN MENU)
# ============
def main_menu():
    while True:
        print("\n" + "-"*40)
        print(" HỆ THỐNG QUẢN LÝ THƯ VIỆN - TRANG CHỦ")
        print("-"*40)
        print("1. 📚 Quản lý Sách (Xem, Tìm, Thêm, Sửa, Xóa)")
        print("2. 👤 Quản lý Độc giả & Mượn Trả")
        print("3. ✍️  Quản lý Tác giả & Thể loại")
        print("4. 📊 Báo cáo & Thống kê Thư viện")
        print("0. 🚪 Thoát chương trình")
        
        choice = input("Chọn menu chính (0-4): ")
        
        if choice == '1':
            print("\n-- QUẢN LÝ SÁCH --")
            print("1: Xem tất cả | 2: Tìm kiếm | 3: Thêm mới | 4: Sửa | 5: Xóa")
            sub = input("Chọn: ")
            if sub == '1': view_all_books()
            elif sub == '2': search_books()
            elif sub == '3': add_book()
            elif sub == '4': edit_book()
            elif sub == '5': delete_book()
                
        elif choice == '2':
            print("\n-- GIAO DỊCH & ĐỘC GIẢ --")
            print("1: Xem DS Độc giả | 2: Thêm Độc giả | 3: Mượn Sách | 4: Trả Sách")
            sub = input("Chọn: ")
            if sub == '1': view_all_readers()
            elif sub == '2': add_reader()
            elif sub == '3': borrow_book()
            elif sub == '4': return_book()
                
        elif choice == '3':
            print("\n-- TÁC GIẢ & THỂ LOẠI --")
            print("1: Xem danh sách | 2: Đổi tên Tác giả")
            sub = input("Chọn: ")
            if sub == '1': view_authors_cats()
            elif sub == '2': edit_author()
                
        elif choice == '4':
            print("\n-- BÁO CÁO & THỐNG KÊ --")
            print("1: Xem sách đang cho mượn | 2: Xem sách quá hạn | 3: Thống kê số liệu %")
            sub = input("Chọn: ")
            if sub == '1': currently_borrowed()
            elif sub == '2': overdue_report()
            elif sub == '3': view_statistics()
                
        elif choice == '0':
            print("Đang thoát hệ thống. Chúc bạn một ngày làm việc hiệu quả!")
            break

if __name__ == '__main__':
    main_menu()