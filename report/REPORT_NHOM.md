# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** G13 — K4-L3A — Đăng ký & điều chỉnh học phần
**Thành viên:** Đinh Ngọc Đức (R1), Đoàn Tuấn Long (R2), Nguyễn Việt Thành (R3), Nguyễn Đình Phúc (R4 — Demo & Report Lead)
**Ngày:** 19/09/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Quy định và dịch vụ đăng ký học phần tại trường Đại học VinUni (VinUni Course Registration & Academic Regulations) — Lớp K4-L3A.

**Tại sao nhóm chọn chủ đề này?**

> Đăng ký học phần là quy trình học vụ thiết yếu, có nhiều quy định ràng buộc chặt chẽ (hạn thêm/hủy môn, điều kiện tiên quyết, giới hạn tín chỉ rút). Quy trình này có sự phân biệt rõ ràng giữa các đối tượng người dùng (`student`, `faculty`, `all`), là ngữ liệu lý tưởng để xây dựng hệ thống hỏi đáp RAG và kiểm chứng hiệu quả của việc lọc siêu dữ liệu (metadata filtering).

### Danh sách tài liệu (Data Inventory)

| #   | Tên tài liệu                                               | Nguồn (Source URL)                                                                                         | Ngày lấy / Phiên bản    | Số ký tự | Metadata đã gán                                                       |
| --- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------- | -------- | --------------------------------------------------------------------- |
| 1   | Biểu mẫu và đơn từ học vụ                                  | https://registrar.vinuni.edu.vn/vi/hoc-thuat-dich-vu/bieu-mau-don-tu/                                      | 2026-09-19 / not-stated | 1,846    | `audience: student`, `department: registrar`, `category: academic-requests`      |
| 2   | Câu hỏi thường gặp về đăng ký học phần                     | https://registrar.vinuni.edu.vn/vi/nhung-cau-hoi-thuong-gap/                                               | 2026-09-19 / not-stated | 1,220    | `audience: student`, `department: registrar`, `category: faq`                    |
| 3   | Hướng dẫn giảng viên kiểm tra lịch dạy kỳ Spring 2026      | https://registrar.vinuni.edu.vn/vi/2026/01/28/thong-bao-quan-trong-cho-hoc-ky-mua-xuan-2026/               | 2026-09-19 / 2026-01-28 | 778      | `audience: faculty`, `department: registrar`, `category: teaching-schedule`      |
| 4   | Hướng dẫn thời khóa biểu và đăng ký học phần               | https://registrar.vinuni.edu.vn/vi/hoc-thuat-dich-vu/thoi-khoa-bieu-dang-ky-hoc-phan/                      | 2026-09-19 / not-stated | 1,746    | `audience: student`, `department: registrar`, `category: registration-guide`     |
| 5   | Lịch đăng ký học phần kỳ Spring 2026                       | https://registrar.vinuni.edu.vn/vi/2025/12/15/thong-bao-chinh-thuc-ve-lich-dang-ky-mon-hoc-ky-spring-2026/ | 2026-09-19 / 2025-12-15 | 1,465    | `audience: student`, `department: registrar`, `category: registration-schedule`  |
| 6   | Quy định học thuật chương trình đại học toàn thời gian     | https://policy.vinuni.edu.vn/all-policies/academic-regulations-for-full-time-undergraduate-programs/       | 2026-09-19 / V8.1       | 3,369    | `audience: student`, `department: academic-affairs`, `category: academic-policy` |
| 7   | Hướng dẫn sinh viên Add, Drop và Withdrawal kỳ Spring 2026 | https://registrar.vinuni.edu.vn/vi/2026/01/28/thong-bao-quan-trong-cho-hoc-ky-mua-xuan-2026/               | 2026-09-19 / 2026-01-28 | 1,617    | `audience: student`, `department: registrar`, `category: add-drop-withdraw`      |
| 8   | Vai trò Phòng Quản lý Đào tạo VinUni                       | https://registrar.vinuni.edu.vn/vi/trang-chu/                                                              | 2026-09-19 / not-stated | 583      | `audience: all`, `department: registrar`, `category: registrar-services`         |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**

- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.
- [x] Có 8 file Markdown và 8 dòng trong `sources.csv`; `doc_id` duy nhất và khớp một-một với tên file.
- [x] Corpus có ba giá trị `audience` (`student`, `faculty`, `all`) và mỗi tài liệu còn có `department`, `category`, `language`.
- [x] Quy trình thu thập dùng crawler có kiểm tra `robots.txt`, đặt User-Agent và giãn cách request; nội dung được làm sạch menu, footer và tin liên quan trước khi benchmark.
- [x] Trang thông báo Spring 2026 chứa cả nội dung sinh viên và giảng viên được tách thành hai file theo `audience`, giúp metadata filter có tác dụng thực tế.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata    | Kiểu   | Ví dụ giá trị                                  | Tại sao hữu ích cho truy xuất (retrieval)?                                                            |
| ------------------ | ------ | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `audience`         | string | `student`, `faculty`, `all`                    | Lọc chính xác đối tượng áp dụng quy định, tránh nhầm lẫn giữa lịch trình của sinh viên và giảng viên. |
| `department`       | string | `registrar`, `academic-affairs`                | Giúp thu hẹp phạm vi tìm kiếm theo đơn vị phụ trách (Phòng Đào tạo vs Phòng Học vụ).                  |
| `category`         | string | `registration-guide`, `faq`, `academic-policy` | Phân loại loại hình tài liệu (hướng dẫn thao tác, câu hỏi thường gặp, hay quy chế chính thức).        |
| `document_version` | string | `2026-01-28`, `V8.1`, `not-stated`             | Xác thực tính hiệu lực và phiên bản cập nhật mới nhất của quy định.                                   |
| `retrieved_at`     | string | `2026-09-19`                                   | Ghi nhận thời điểm thu thập dữ liệu phục vụ truy xuất nguồn gốc (provenance).                         |
| `doc_id`           | string | `lich-dang-ky-spring-2026`                     | Định danh ổn định tài liệu gốc và liên kết mọi chunk về đúng nguồn.                                   |
| `source_url`       | string | URL chính thức của VinUni                      | Cho phép kiểm chứng nội dung và truy vết provenance.                                                  |
| `language`         | string | `vi`, `en`                                     | Hỗ trợ chọn hoặc đánh giá embedding đa ngữ.                                                           |
| `license_or_permission` | string | `public-source`                           | Ghi căn cứ sử dụng trong `sources.csv`, tránh đưa nguồn không rõ quyền vào corpus.                     |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 3 tài liệu đại diện (đã loại bỏ frontmatter YAML trước khi đo):

**Tham số chạy baseline:**
- `FixedSizeChunker`: `chunk_size=500`, `overlap=50` (`overlap = chunk_size // 10`)
- `SentenceChunker`: `max_sentences_per_chunk=3`
- `RecursiveChunker`: `chunk_size=500`, `separators=["\n\n", "\n", ". ", " ", ""]`

| Tài liệu                                                   | Chiến lược (Strategy)                     | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không?                                                 |
| ---------------------------------------------------------- | ----------------------------------------- | -------------- | ----------------- | ------------------------------------------------------------------------ |
| `huong-dan-dang-ky-hoc-phan.md` (1,746 ký tự)              | FixedSizeChunker (`fixed_size`, size=500, overlap=50) | 4 | 474.0 | Trung bình — chunk dài ổn định nhưng có thể cắt ngang ý. |
|                                                            | SentenceChunker (`by_sentences`, max=3)   | 11             | 157.4             | Khá — giữ trọn câu nhưng đôi khi thiếu ngữ cảnh toàn mục. |
|                                                            | RecursiveChunker (`recursive`, size=500)  | 5              | 347.6             | Tốt — giữ đoạn/mục tự nhiên hơn fixed size. |
| `lich-dang-ky-spring-2026.md` (1,465 ký tự)                | FixedSizeChunker (`fixed_size`, size=500, overlap=50) | 4 | 403.8 | Trung bình — giữ đủ độ dài nhưng không theo cấu trúc lịch. |
|                                                            | SentenceChunker (`by_sentences`, max=3)   | 5              | 291.0             | Tốt — phù hợp với thông báo ngắn theo câu. |
|                                                            | RecursiveChunker (`recursive`, size=500)  | 4              | 364.8             | Tốt — số chunk vừa phải, giữ các đoạn liên quan. |
| `quy-dinh-hoc-thuat-dai-hoc.md` (3,369 ký tự)              | FixedSizeChunker (`fixed_size`, size=500, overlap=50) | 8 | 464.9 | Trung bình — dễ cắt ngang điều khoản dài. |
|                                                            | SentenceChunker (`by_sentences`, max=3)   | 11             | 304.4             | Khá — dễ đọc nhưng có thể tách rời tiêu đề và nội dung. |
|                                                            | RecursiveChunker (`recursive`, size=500)  | 10             | 335.1             | Tốt — cân bằng giữa độ dài chunk và ranh giới đoạn. |

### Chiến lược của từng thành viên

**Thành viên 1 — Đinh Ngọc Đức (R1)**

- **Loại chiến lược:** FixedSizeChunker (`chunk_size=500`, `overlap=50`)
- **Mô tả & lý do chọn cho chủ đề này:** Cắt văn bản theo độ dài ký tự cố định và trượt cửa sổ overlap để tránh mất mát thông tin tại ranh giới cắt. Phù hợp làm baseline đơn giản, dễ kiểm soát độ dài vector. Tuy nhiên nhược điểm lớn là cắt bất chấp ranh giới câu, danh sách liệt kê quy định bị đứt đoạn.
- **Code snippet:**

```python
chunker = FixedSizeChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk(document_text)
```

**Thành viên 2 — Đoàn Tuấn Long (R2)**

- **Loại chiến lược:** SentenceChunker (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn:** Tách sau dấu kết thúc câu bằng regex lookbehind `(?<=[.!?])(?: |\n)`, giữ lại dấu câu và gom tối đa 3 câu vào một chunk. Chiến lược này giữ câu hoàn chỉnh nhưng vẫn nhạy với bullet không có dấu kết thúc, chữ viết tắt và số thập phân.
- **Code snippet:**

```python
chunker = SentenceChunker(max_sentences_per_chunk=3)
chunks = chunker.chunk(document_text)
```

**Thành viên 3 — Nguyễn Việt Thành (R3)**

- **Loại chiến lược:** Heading / Markdown Section Chunker (Custom)
- **Mô tả & lý do chọn:** Tách tài liệu theo các tiêu đề cấp bậc (`#`, `##`, `###`) của Markdown. Section dài hơn 500 ký tự được chia tiếp bằng `RecursiveChunker`, sau đó heading ban đầu được gắn lại vào từng chunk con. Cách này giữ ngữ cảnh mục mà vẫn khống chế kích thước chunk; hạn chế quan sát được là ở Q1, chunk giới thiệu cùng chủ đề đứng trên chunk chứa thời điểm chính xác.
- **Code snippet:**

```python
for heading, body in split_by_heading(document_text):
    parts = [body] if len(heading) + len(body) <= 500 else RecursiveChunker(500).chunk(body)
    chunks.extend(f"{heading}\n{part}".strip() for part in parts)
```

**Thành viên 4 — Nguyễn Đình Phúc (R4 — Demo & Report Lead)**

- **Loại chiến lược:** RecursiveChunker (`chunk_size=300`, `separators=["\n\n", "\n", " ", ""]`)
- **Mô tả & lý do chọn:** Sử dụng thuật toán chia đệ quy ưu tiên bảo toàn tính phân tầng của tài liệu: thử tách theo đoạn văn (`\n\n`), nếu quá dài chuyển sang tách dòng (`\n`), rồi đến từ (` `) và ký tự (`""`). Chiến lược này phù hợp với văn bản học vụ vì vừa tôn trọng cấu trúc Markdown, vừa khống chế kích thước chunk dưới 300 ký tự.
- **Code snippet:**

```python
chunker = RecursiveChunker(chunk_size=300, separators=["\n\n", "\n", " ", ""])
chunks = chunker.chunk(document_text)
```

### So Sánh Giữa Các Thành Viên

| Thành viên             | Chiến lược (Strategy)       | Số chunks | Điểm truy xuất (/10)           | Top-1 Score trung bình | Điểm mạnh                                                                                             | Điểm yếu                                                                                                   |
| ---------------------- | --------------------------- | --------- | ------------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Đinh Ngọc Đức (R1)     | FixedSizeChunker (`500/50`) | 31        | 8 / 10                         | 0.8229 (Q1–Q5)         | Dễ cài đặt, kiểm soát kích thước chặt chẽ, điểm cosine cao nhất ở Q1 (0.8787).                        | Cắt ngang câu; Q5 gold chunk không lọt top-3 dù có metadata filter.                                        |
| Đoàn Tuấn Long (R2)    | SentenceChunker (`max=3`)   | 43        | 9 / 10                         | 0.4970 (Q1–Q5)         | Giữ trọn vẹn ngữ nghĩa câu, không bị rách từ; Q2 gold ở hạng 2.                                       | Nhạy cảm với bullet points; kích thước chunk không đều; score tương đối thấp hơn do dùng lexical embedder. |
| Nguyễn Việt Thành (R3) | HeadingChunker (`500` + recursive fallback) | 49 | 9 / 10 | 0.5001 (Q1–Q5) | Giữ heading trong mọi chunk con; 5/5 câu có chunk liên quan trong top-3; Q5 lên top-1 sau filter. | Q1 chunk chứa giờ mở SIS chỉ ở hạng 2 nên mất 1 điểm. |
| Nguyễn Đình Phúc (R4)  | RecursiveChunker (`300`)    | 65        | 9 / 10                         | 0.7533 (Q1–Q5)         | Chunk cân đối, tôn trọng cấu trúc Markdown; Q1–Q4 đều lấy gold ở top-1.                               | Q5 gold ở hạng 2 nên chỉ đạt 1/2; cần định nghĩa bộ separators hợp lý.                                     |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**

> Theo kết quả retrieval đã ghi nhận, **SentenceChunker, HeadingChunker và RecursiveChunker đồng hạng 9/10**, nhưng lỗi ở các câu khác nhau: Sentence đưa đáp án Q2 lên hạng 2, Heading đưa đáp án Q1 lên hạng 2, còn Recursive đưa đáp án Q5 lên hạng 2. Heading phù hợp cấu trúc tài liệu học vụ và xử lý section dài bằng recursive fallback, nhưng dữ liệu hiện tại không chứng minh một chiến lược thắng tuyệt đối.

> **Giới hạn phép so sánh:** các thành viên đã dùng embedding backend khác nhau, trái với điều kiện kiểm soát lý tưởng là chỉ thay chunker. Vì vậy raw cosine không được dùng để khẳng định tác động riêng của chiến lược chunking; kết luận trên chỉ dựa vào điểm retrieval, hạng của chunk chứa đáp án và độ mạch lạc quan sát được. Muốn kết luận nhân quả, nhóm phải chạy lại cả bốn chiến lược với cùng một embedder.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| #   | Câu hỏi (Query)                                                                                             | Câu trả lời chuẩn (Gold Answer)                                                                                                                                                                                       | Chunk nào chứa thông tin?                    |
| --- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| 1   | Cổng đăng ký SIS kỳ Spring 2026 mở lúc nào?                                                                 | Cổng đăng ký SIS mở lúc **14:00 ngày 18/12/2025**.                                                                                                                                                                    | `lich-dang-ky-spring-2026.md`                |
| 2   | Đăng ký học phần trên SIS gồm những bước nào? Trạng thái nào mới là đăng ký thành công?                     | Đăng nhập SIS → Academics → Course Registration → chọn học kỳ → Register khi Open → Add rồi Register. Trạng thái phải là **Registered** (`Selected` = chưa thành công).                                               | `huong-dan-dang-ky-hoc-phan.md`              |
| 3   | Nếu môn trùng giờ hoặc chưa đủ điều kiện tiên quyết thì SIS xử lý thế nào?                                  | SIS **không cho đăng ký môn trùng giờ** và **tự động chặn** khi chưa đạt tiên quyết. Nếu bị chặn dù nghĩ đủ điều kiện → liên hệ Phòng Quản lý Đào tạo.                                                                | `huong-dan-dang-ky-hoc-phan.md`              |
| 4   | Sinh viên được rút (withdraw) tối đa bao nhiêu tín chỉ trong cả chương trình? Sau khi đạt giới hạn thì sao? | Rút tối đa **18 tín chỉ** trong toàn chương trình. Khi đạt giới hạn phải tiếp tục học và nhận điểm cho môn đã đăng ký.                                                                                                | `sinh-vien-add-drop-withdraw-spring-2026.md` |
| 5   | Trước ngày bắt đầu giảng dạy Spring 2026, tôi cần kiểm tra những gì? _(Lọc: `audience: student`)_           | Sinh viên phải xác nhận thời gian, địa điểm học và kiểm tra các môn đã đăng ký trên SIS được đồng bộ, hiển thị đúng trên Canvas. Nếu môn có trên SIS nhưng không xuất hiện trên Canvas thì báo Phòng Quản lý Đào tạo. | `sinh-vien-add-drop-withdraw-spring-2026.md` |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| #   | Câu hỏi                                                   | Kết quả tốt nhất theo hạng gold chunk                 | Kết quả giữa các chiến lược                                    | Ghi chú                                                                                   |
| --- | --------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | Cổng đăng ký SIS kỳ Spring 2026 mở lúc nào?               | Fixed, Sentence và Recursive                          | Ba chiến lược top-1; Heading có chunk trả lời ở hạng 2         | Heading nhận 1/2; không so raw cosine vì các backend embedding khác nhau.                 |
| 2   | Các bước đăng ký trên SIS & trạng thái thành công?        | Fixed, Heading, Recursive                             | Ba chiến lược top-1; Sentence có gold ở hạng 2                 | Sentence nhận 1/2 theo rubric dù vẫn có chunk trả lời trong top-3.                       |
| 3   | Môn trùng giờ hoặc chưa đủ điều kiện tiên quyết?          | Đồng hạng: cả 4 chiến lược                            | Cả 4 đều đưa gold chunk lên top-1                              | Câu hỏi có từ khóa và điều kiện rõ ràng.                                                   |
| 4   | Rút (withdraw) tối đa bao nhiêu tín chỉ?                  | Đồng hạng: cả 4 chiến lược                            | Cả 4 đều đưa chunk chứa `18 tín chỉ` lên top-1                 | Con số và thuật ngữ `withdraw` giúp truy xuất ổn định.                                    |
| 5   | Trước ngày bắt đầu giảng dạy Spring 2026 cần kiểm tra gì? | Sentence và Heading + metadata filter                 | Sentence/Heading top-1; Recursive top-2; Fixed vắng top-3      | Đây là câu phân biệt rõ nhất tác dụng của audience filter và ranh giới chunk.             |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**

> **Có, metadata filter giúp rõ nhất ở Câu hỏi 5**, vì query không nói người hỏi là sinh viên hay giảng viên và hai tài liệu cạnh tranh dùng nhiều từ giống nhau.

**Bằng chứng A/B đầy đủ của FixedSizeChunker:**

| Lượt chạy | Hạng | `doc_id` | Score | Chunk chứa đáp án? |
| --- | ---: | --- | ---: | --- |
| Không filter | 1 | `giang-vien-kiem-tra-lich-spring-2026` | 0.846540 | Không — sai audience |
| Không filter | 2 | `lich-dang-ky-spring-2026` | 0.776053 | Không |
| Không filter | 3 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.772247 | Không |
| `audience: student` | 1 | `lich-dang-ky-spring-2026` | 0.776053 | Không |
| `audience: student` | 2 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.772247 | Không |
| `audience: student` | 3 | `huong-dan-dang-ky-hoc-phan` | 0.640615 | Không |

FixedSize loại được kết quả giảng viên nhưng gold chunk chứa đồng thời thông tin SIS/Canvas vẫn không lọt top-3.

**Bằng chứng A/B đầy đủ của HeadingChunker:**

| Lượt chạy | Hạng | `doc_id` | Score | Chunk chứa đáp án? |
| --- | ---: | --- | ---: | --- |
| Không filter | 1 | `giang-vien-kiem-tra-lich-spring-2026` | 0.5239 | Không |
| Không filter | 2 | `giang-vien-kiem-tra-lich-spring-2026` | 0.3115 | Không |
| Không filter | 3 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.3065 | Có |
| `audience: student` | 1 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.3065 | Có |
| `audience: student` | 2 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.2899 | Không |
| `audience: student` | 3 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.2417 | Không |

Hai chunk giảng viên bị loại trước khi tính top-k, đưa chính chunk sinh viên từ hạng 3 lên hạng 1. Filter không làm đổi similarity của chunk; nó cải thiện thứ hạng và precision theo đối tượng.

**Bằng chứng A/B đầy đủ của SentenceChunker:**

| Lượt chạy | Hạng | `doc_id` | Score | Chunk chứa đáp án? |
| --- | ---: | --- | ---: | --- |
| Không filter | 1 | `giang-vien-kiem-tra-lich-spring-2026` | 0.464 | Không — sai audience |
| Không filter | 2 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.393 | Có |
| Không filter | 3 | `huong-dan-dang-ky-hoc-phan` | 0.267 | Có một phần |
| `audience: student` | 1 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.393 | Có |
| `audience: student` | 2 | `huong-dan-dang-ky-hoc-phan` | 0.267 | Có một phần |
| `audience: student` | 3 | `huong-dan-dang-ky-hoc-phan` | 0.211 | Không |

Với SentenceChunker, filter loại tài liệu giảng viên ở hạng 1 và đưa gold chunk sinh viên từ hạng 2 lên hạng 1.

**Bằng chứng A/B đầy đủ của RecursiveChunker:**

| Lượt chạy | Hạng | `doc_id` | Score | Chunk chứa đáp án? |
| --- | ---: | --- | ---: | --- |
| Không filter | 1 | `giang-vien-kiem-tra-lich-spring-2026` | 0.7833 | Không |
| Không filter | 2 | `giang-vien-kiem-tra-lich-spring-2026` | 0.6876 | Không |
| Không filter | 3 | `lich-dang-ky-spring-2026` | 0.6837 | Không |
| `audience: student` | 1 | `lich-dang-ky-spring-2026` | 0.6837 | Không |
| `audience: student` | 2 | `sinh-vien-add-drop-withdraw-spring-2026` | 0.6739 | Có |
| `audience: student` | 3 | `lich-dang-ky-spring-2026` | 0.6720 | Không |

Với RecursiveChunker, gold chunk vắng khỏi top-3 khi không filter và lên hạng 2 sau pre-filter, nên Q5 đạt 1/2.

**Tóm tắt A/B từ bằng chứng hiện có:**

| Chiến lược | Không filter | Có `audience: student` | Kết luận |
| --- | --- | --- | --- |
| FixedSize | Top-1 là tài liệu giảng viên | Loại được tài liệu giảng viên nhưng gold chunk vẫn vắng top-3 | Filter đúng đối tượng nhưng không sửa được ranh giới chunk. |
| Sentence | Top-1 nhầm tài liệu giảng viên | Gold chunk sinh viên lên top-1 | Filter sửa được lỗi sai audience. |
| Heading | Hai hạng đầu là tài liệu giảng viên; gold ở hạng 3 | Gold chunk sinh viên lên hạng 1 | Có đủ top-3 A/B; filter đưa Q5 từ 1/2 lên 2/2. |
| Recursive | Gold chunk vắng top-3 | Gold chunk lên hạng 2 | Filter tăng recall cho nội dung sinh viên. |

**Đánh đổi precision/recall:** filter giúp khi biết chắc đối tượng là sinh viên, nhưng có thể loại nhầm tài liệu `all` hoặc tài liệu đối tượng khác chứa chính sách dùng chung. Vì vậy chỉ áp dụng filter cứng khi query hoặc ngữ cảnh người dùng xác định rõ audience; nếu không, nên tìm không filter hoặc hợp nhất nhiều audience hợp lệ.

> Cả bốn báo cáo cá nhân đều đã cung cấp top-3 A/B của Q5. Kết quả nhất quán rằng pre-filter loại tài liệu sai audience, nhưng mức cải thiện phụ thuộc ranh giới chunk: Sentence và Heading đưa gold lên hạng 1, Recursive đưa gold lên hạng 2, còn FixedSize vẫn không lấy được gold chunk trong top-3.

### Failure case thật và hướng sửa

> **Câu hỏng:** Q5 với FixedSize vẫn đạt 0/2 sau khi lọc `audience: student`. **Nguyên nhân:** filter loại đúng tài liệu giảng viên, nhưng top-3 chỉ lấy các chunk cùng chủ đề hoặc mốc thời gian; chunk chứa đồng thời `SIS` và `Canvas` nằm ở section khác nên không lọt vào ngữ cảnh. **Đề xuất:** dùng chunking theo heading có fallback cho section dài, hoặc thử lại kích thước/overlap và tăng `top_k`; sau mỗi thay đổi phải tiếp tục chấm ở cấp nội dung chunk, không chỉ theo `doc_id`.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày (6–8 phút):**

1. **Cấu trúc ngữ liệu quyết định chất lượng Chunking:** Tài liệu hành chính/học vụ có heading, danh sách và bảng. `FixedSize` dễ cắt ngang ý, còn Heading/Recursive giữ ranh giới ngữ nghĩa tốt hơn; section quá dài vẫn cần fallback để tránh làm loãng embedding.
2. **Sức mạnh và giới hạn của Metadata Pre-filtering:** Lọc `audience` loại tài liệu sai đối tượng trước khi search và tăng precision ở Q5, nhưng không tự sửa được ranh giới chunk kém như trường hợp FixedSize.
3. **Grounding và trích dẫn nguồn:** Prompt yêu cầu chỉ dùng context và trích dẫn chunk giúp tăng khả năng truy vết, giảm nguy cơ hallucination; nó không bảo đảm loại bỏ hoàn toàn câu trả lời sai nếu retrieval đưa vào context không phù hợp.

**Bài học rút ra khi so sánh trong nhóm:**

> Khi cùng nạp 8 văn bản quy chế nhưng sử dụng các chiến lược khác nhau, nhóm nhận thấy số lượng và chất lượng chunk có sự phân hóa rõ rệt: `FixedSize` (Đức) sinh ra 31 chunks với overlap giữ ngữ cảnh biên, nhưng Q5 thất bại vì gold chunk nằm sai vị trí cắt; `Sentence` (Long) sinh ra 43 chunks giữ trọn câu nhưng kích thước không đồng đều; `Heading` (Thành) sinh ra 49 chunks, giữ heading khi recursive fallback nhưng Q1 chỉ có chunk trả lời ở hạng 2; `Recursive` (Phúc) sinh ra 65 chunks gọn nhưng Q5 chỉ có gold ở hạng 2. Sentence, Heading và Recursive cùng đạt 9/10. Raw cosine chỉ dùng tham khảo vì các thành viên dùng embedding backend khác nhau; so sánh chính dựa trên điểm retrieval và hạng của chunk chứa đáp án.

**Tổng hợp đóng góp cá nhân:**

| Thành viên        | Vai trò                             | Chiến lược                  | Tests | Benchmark (5Q)   | Tự đánh giá |
| ----------------- | ----------------------------------- | --------------------------- | ----- | ---------------- | ----------- |
| Đinh Ngọc Đức     | R1 — Data Lead; FixedSize           | `FixedSizeChunker(500, 50)` | 42/42 | 4/5 (8/10 điểm)  | 58/60       |
| Đoàn Tuấn Long    | R2 — Benchmark Lead; Sentence       | `SentenceChunker(max=3)`    | 42/42 | 5/5 (9/10 điểm)  | 58/60       |
| Nguyễn Việt Thành | R3 — Strategy Lead; Heading         | `HeadingChunker(500)`       | 42/42 | 5/5 (9/10 điểm)  | 58/60       |
| Nguyễn Đình Phúc  | R4 — Demo/Report Lead; Recursive    | `RecursiveChunker(300)`     | 42/42 | 5/5 (9/10 điểm)  | 59/60       |

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**

> 1. Bổ sung thêm các trường metadata chuyên sâu như `semester` (`Spring-2026`), `degree_level` (`undergraduate`), và `urgency` để tăng độ linh hoạt khi truy vấn nghiệp vụ phức tạp.
> 2. Xây dựng bộ parser Markdown chuyên dụng cho bảng biểu (Markdown tables) để giữ nguyên tiêu đề cột cho từng dòng dữ liệu, tránh việc các dòng trong bảng bị tách rời khỏi ngữ cảnh tiêu đề.
> 3. Thống nhất embedding model giữa các thành viên để đảm bảo so sánh công bằng (Đức dùng `gemini-embedding-001`; Long dùng lexical embedder; Thành dùng offline lexical hash embedding; Phúc dùng `paraphrase-multilingual-MiniLM-L12-v2`).

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí                                 | Điểm tự đánh giá |
| ---------------------------------------- | ---------------- |
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10          |
| Thiết kế chiến lược (Strategy Design)    | 13 / 15          |
| Chất lượng truy xuất (Retrieval Quality) | 9 / 10           |
| Thuyết trình (Demo)                      | 5 / 5            |
| **Tổng phần nhóm**                       | **37 / 40**      |

> Điểm tự đánh giá giữ ở 37/40 vì các thành viên dùng embedding backend khác nhau, nên phép so sánh chỉ phản ánh kết quả quan sát được và chưa cô lập riêng tác động của chunker. Bằng chứng top-3 A/B của cả bốn chiến lược đã đầy đủ.
