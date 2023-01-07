# python-history-blog-project
Đồ án cuối kì môn Kỹ Thuật Lập Trình Python

- Phiên bản Python sử dụng: 3.11
- Database sử dụng: Postgresql và PgAdmin 4
- IDE: Visual Studio Code

Các thao tác để có thể run được project trên localhost:

*Với database Postgresql:
- Bước 1: Tạo Server trong database Postgresql:
	+ Click chuột phải vào Server -> Register -> Server:
	+ Ở mục General để Name là history-blog-project (hoặc có thể đổi tên nếu muốn)
	+ Ở mục Connection hostname là localhost, port giữ nguyên là 5432, password thì đặt tùy ý. 
	+ Tạo database trong server phía trên đặt tên history-blog-project (hoặc đổi tên nếu muốn)

- Bước 2: Thay đổi configure database trong file settings.py:
	+ Vào folder History_Blog_Project -> settings.py kéo xuống kiếm phần DATABASES.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'history-blog-project',
        'USER':'postgres',
        'PASSWORD': 'hocanhcong1996',
        'PORT':'5432',
        'HOST':'localhost'
    }
}	
		Tại đây:
		--'NAME' là tên của database
		--'USER' mặc định là 'postgresql'(hay chính là username của server tạo phía trên)
		--'PASSWORD' là password đặt phía trên
		--'PORT' mặc định là 5432 (hoặc tên port đã đổi)
		--'HOST' là localhost (chính là hostname)


*Thao tác với các thư viện của project
- Bước 1: Kiểm tra version python bằng cách mở terminal có path vào đến thư mục root python-history-blog-project 
và gõ lệnh python xem có hiển thị version hay không? Nếu không được thì kiểm tra lại cho đến khi nào có biến môi trường python
- Bước 2: Chạy các lệnh sau để cập nhật một số thư viện cho project
	- "python -m pip install Django" 
	- "python.exe -m pip install --upgrade pip"
	- "pip install django-crispy-forms"
	- "pip install psycopg2"
	- "python -m pip install --upgrade pip"
	- "python -m pip install --upgrade Pillow"
	- "pip install Unidecode"

*Thao tác để kết nối project và database và runserver
- Bước 1: Chạy lệnh "py manage.py makemigrations" để cập nhật tất cả các sự thay đổi của model
- Bước 2: Chạy lệnh "python manage.py migrate --run-syncdb" để run database postgresql có tất cả các model
- Bước 3: Chạy lệnh "python manage.py createsuperuser" để tạo account superuser để truy cập vào trang admin của django
- Bước 4: Chạy lệnh py manage.py runserver để run website trên localhost
- Bước cuối: Vào trình duyệt web gõ url: http://127.0.0.1:8000/blog/ để truy cập vào website viết blog
