## 1. NLP-ASS-HCMUT-2024
Bài tập lớn môn Xử lí ngôn ngữ tự nhiên (CO3085) trường Đại học Bách Khoa TPHCM
Dự án này là một hệ thống trả lời thông tin về các chuyến du lịch sử dụng các kỹ thuật xử lý ngôn ngữ tự nhiên (NLP).

Đầu vào của hệ thống là một câu hỏi bằng ngôn ngữ tự nhiên (tiếng Anh). Câu hỏi này sẽ được phân tích để chuyển đổi thành dạng logic, sau đó cấu trúc logic này được phân tích tiếp thành dạng ngữ nghĩa thủ tục.

Với truy vấn đã được chuyển thành dạng ngữ nghĩa thủ tục, hệ thống sẽ tra cứu thông tin trong cơ sở dữ liệu và trả về kết quả dựa trên câu hỏi đầu vào.

# 2. Prerequisites:
- Python 3.8
- NLTK 3.9

## 3. System structure
- main.py: mã nguồn chình
- grammar.fcfg: văn phạm cho bài toán  
