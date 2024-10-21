## 1. NLP-ASS-HCMUT-2024

Bài tập lớn môn Xử lí ngôn ngữ tự nhiên (CO3085) trường Đại học Bách Khoa TPHCM
Dự án này là một hệ thống trả lời thông tin về các chuyến du lịch sử dụng các kỹ thuật xử lý ngôn ngữ tự nhiên (NLP).

Đầu vào của hệ thống là một câu hỏi bằng ngôn ngữ tự nhiên (tiếng Anh). Câu hỏi này sẽ được phân tích để chuyển đổi thành dạng logic, sau đó cấu trúc logic này được phân tích tiếp thành dạng ngữ nghĩa thủ tục.

Với truy vấn đã được chuyển thành dạng ngữ nghĩa thủ tục, hệ thống sẽ tra cứu thông tin trong cơ sở dữ liệu và trả về kết quả dựa trên câu hỏi đầu vào.

## 2. Prerequisites:

- Python 3.8
- NLTK 3.9

## 3. System structure

- main.py: mã nguồn chính
- grammar.fcfg: văn phạm cho bài toán
- Dockerfile: chứa những thứ cần thiết để build và chạy image
- ./nlp/input/sentences.txt: input cho việc sinh câu
- ./nlp/output: folder chưa output

## 4. Cài đặt:

**Có 2 cách để chạy chương trình:**
Chạy trên máy host, kết quả được lưu trong ./nlp/output

```sh
$python3 main.py
```

Chạy thông qua Docker, kết quả được mount ra thư mục trong máy host:

```sh
docker build --network=host -t nlp241 .
docker run --rm -v output:/nlp/output -v input:/nlp/input nlp241
```

## 5. Kết quả:

- Phần 2.1: Viết văn phạm: file grammar.fcfg
- Phần 2.2: giải thuật sinh những câu được chấp nhận bởi grammar (giới hạn 10000 câu): input: none, output: ./nlp/output/samples.txt
- Phần 2.3: Xây dựng bộ phân tích cú pháp: input: sentences.txt, output: ./nlp/output/parse_result.txt
