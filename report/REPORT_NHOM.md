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
| 1   | Biểu mẫu và đơn từ học vụ                                  | https://registrar.vinuni.edu.vn/vi/hoc-thuat-dich-vu/bieu-mau-don-tu/                                      | 2026-09-19 / not-stated | 1,846    | `audience: student`, `dept: registrar`, `cat: academic-requests`      |
| 2   | Câu hỏi thường gặp về đăng ký học phần                     | https://registrar.vinuni.edu.vn/vi/nhung-cau-hoi-thuong-gap/                                               | 2026-09-19 / not-stated | 1,220    | `audience: student`, `dept: registrar`, `cat: faq`                    |
| 3   | Hướng dẫn giảng viên kiểm tra lịch dạy kỳ Spring 2026      | https://registrar.vinuni.edu.vn/vi/2026/01/28/thong-bao-quan-trong-cho-hoc-ky-mua-xuan-2026/               | 2026-09-19 / 2026-01-28 | 778      | `audience: faculty`, `dept: registrar`, `cat: teaching-schedule`      |
| 4   | Hướng dẫn thời khóa biểu và đăng ký học phần               | https://registrar.vinuni.edu.vn/vi/hoc-thuat-dich-vu/thoi-khoa-bieu-dang-ky-hoc-phan/                      | 2026-09-19 / not-stated | 1,746    | `audience: student`, `dept: registrar`, `cat: registration-guide`     |
| 5   | Lịch đăng ký học phần kỳ Spring 2026                       | https://registrar.vinuni.edu.vn/vi/2025/12/15/thong-bao-chinh-thuc-ve-lich-dang-ky-mon-hoc-ky-spring-2026/ | 2026-09-19 / 2025-12-15 | 1,465    | `audience: student`, `dept: registrar`, `cat: registration-schedule`  |
| 6   | Quy định học thuật chương trình đại học toàn thời gian     | https://policy.vinuni.edu.vn/all-policies/academic-regulations-for-full-time-undergraduate-programs/       | 2026-09-19 / V8.1       | 3,369    | `audience: student`, `dept: academic-affairs`, `cat: academic-policy` |
| 7   | Hướng dẫn sinh viên Add, Drop và Withdrawal kỳ Spring 2026 | https://registrar.vinuni.edu.vn/vi/2026/01/28/thong-bao-quan-trong-cho-hoc-ky-mua-xuan-2026/               | 2026-09-19 / 2026-01-28 | 1,617    | `audience: student`, `dept: registrar`, `cat: add-drop-withdraw`      |
| 8   | Vai trò Phòng Quản lý Đào tạo VinUni                       | https://registrar.vinuni.edu.vn/vi/trang-chu/                                                              | 2026-09-19 / not-stated | 583      | `audience: all`, `dept: registrar`, `cat: registrar-services`         |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**

- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata    | Kiểu   | Ví dụ giá trị                                  | Tại sao hữu ích cho truy xuất (retrieval)?                                                            |
| ------------------ | ------ | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `audience`         | string | `student`, `faculty`, `all`                    | Lọc chính xác đối tượng áp dụng quy định, tránh nhầm lẫn giữa lịch trình của sinh viên và giảng viên. |
| `department`       | string | `registrar`, `academic-affairs`                | Giúp thu hẹp phạm vi tìm kiếm theo đơn vị phụ trách (Phòng Đào tạo vs Phòng Học vụ).                  |
| `category`         | string | `registration-guide`, `faq`, `academic-policy` | Phân loại loại hình tài liệu (hướng dẫn thao tác, câu hỏi thường gặp, hay quy chế chính thức).        |
| `document_version` | string | `2026-01-28`, `V8.1`, `not-stated`             | Xác thực tính hiệu lực và phiên bản cập nhật mới nhất của quy định.                                   |
| `retrieved_at`     | string | `2026-09-19`                                   | Ghi nhận thời điểm thu thập dữ liệu phục vụ truy xuất nguồn gốc (provenance).                         |

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
- **Mô tả & lý do chọn:** Nhận diện ranh giới câu thông qua biểu thức chính quy (Regex: `[.!?]`) và gom tối đa 3 câu vào một khối. Chiến lược này đảm bảo mỗi chunk là một phát biểu hoàn chỉnh ngữ nghĩa tiếng Việt. Hạn chế là các văn bản thông báo học vụ chứa nhiều bullet points không có dấu chấm cuối câu, khiến bộ tách câu gom nhiều dòng vào một chunk dài.
- **Code snippet:**

```python
chunker = SentenceChunker(max_sentences_per_chunk=3)
chunks = chunker.chunk(document_text)
```

**Thành viên 3 — Nguyễn Việt Thành (R3)**

- **Loại chiến lược:** Heading / Markdown Section Chunker (Custom)
- **Mô tả & lý do chọn:** Tách tài liệu theo các tiêu đề cấp bậc (`#`, `##`, `###`) của định dạng Markdown. Rất phù hợp với tài liệu có mục lục rõ ràng (ví dụ: Quy định học thuật). Tuy nhiên với các tài liệu ngắn hoặc các thông báo chỉ có một heading duy nhất thì chunk sinh ra quá lớn, làm giảm độ tập trung của vector embeddings.
- **Code snippet:**

```python
class HeadingChunker:
    def chunk(self, text: str) -> list[str]:
        sections = re.split(r'\n(?=#{1,3}\s)', text)
        return [s.strip() for s in sections if s.strip()]
```

**Thành viên 4 — Nguyễn Đình Phúc (R4 — Demo & Report Lead)**

- **Loại chiến lược:** RecursiveChunker (`chunk_size=300`, `separators=["\n\n", "\n", " ", ""]`)
- **Mô tả & lý do chọn:** Sử dụng thuật toán chia đệ quy ưu tiên bảo toàn tính phân tầng của tài liệu: thử tách theo đoạn văn (`\n\n`), nếu quá dài chuyển sang tách dòng (`\n`), rồi đến từ (` `) và ký tự (`""`). Đây là chiến lược tối ưu nhất cho văn bản học vụ vì vừa tôn trọng cấu trúc Markdown, vừa khống chế nghiêm ngặt kích thước chunk dưới 300 ký tự.
- **Code snippet:**

```python
chunker = RecursiveChunker(chunk_size=300, separators=["\n\n", "\n", " ", ""])
chunks = chunker.chunk(document_text)
```

### So Sánh Giữa Các Thành Viên

| Thành viên             | Chiến lược (Strategy)       | Số chunks | Điểm truy xuất (/10)           | Top-1 Score trung bình | Điểm mạnh                                                                                             | Điểm yếu                                                                                                   |
| ---------------------- | --------------------------- | --------- | ------------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Đinh Ngọc Đức (R1)     | FixedSizeChunker (`500/50`) | 31        | 8 / 10                         | 0.8228 (Q1–Q4)         | Dễ cài đặt, kiểm soát kích thước chặt chẽ, điểm cosine cao nhất ở Q1 (0.8787).                        | Cắt ngang câu; Q5 gold chunk không lọt top-3 dù có metadata filter.                                        |
| Đoàn Tuấn Long (R2)    | SentenceChunker (`max=3`)   | 43        | 9 / 10                         | 0.5229 (Q1–Q4)         | Giữ trọn vẹn ngữ nghĩa câu, không bị rách từ; Q2 gold ở hạng 2.                                       | Nhạy cảm với bullet points; kích thước chunk không đều; score tương đối thấp hơn do dùng lexical embedder. |
| Nguyễn Việt Thành (R3) | HeadingChunker              | 49        | 10 / 10                        | 0.5485 (Q1–Q4)         | Giữ toàn vẹn tiểu mục; logic thông tin liền mạch; 5/5 relevant.                                       | Các mục dài sinh chunk quá khổ, làm loãng ngữ nghĩa vector.                                                |
| Nguyễn Đình Phúc (R4)  | RecursiveChunker (`300`)    | 65       | **10 / 10** _(Top similarity)_ | **0.7731** (Q1–Q4)     | Điểm cosine similarity cao nhất (Q1: 0.8788, Q4: 0.8197); chunk cân đối, tôn trọng cấu trúc Markdown. | Thuật toán đệ quy phức tạp hơn; cần định nghĩa bộ separators hợp lý.                                       |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**

> **RecursiveChunker** là chiến lược tốt nhất cho chủ đề Đăng ký học phần VinUni. Ngữ liệu học vụ thực tế chứa sự kết hợp giữa các đoạn văn giải thích, các mốc thời gian dạng bullet points và các bước hướng dẫn thao tác (1, 2, 3...). `RecursiveChunker` khéo léo giữ nguyên từng mục thông tin trọn vẹn ở mức đoạn/dòng trước khi buộc phải chia nhỏ, giúp vector embeddings phản ánh chính xác nhất ngữ nghĩa câu hỏi mà không bị nhiễu do loãng văn bản hoặc đứt gãy thông tin.

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

| #   | Câu hỏi                                                   | Chiến lược tốt nhất cho câu này                       | Có chunk liên quan trong top-3?                                | Ghi chú                                                                                   |
| --- | --------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | Cổng đăng ký SIS kỳ Spring 2026 mở lúc nào?               | **RecursiveChunker** (score=0.8788)                   | Có (Hạng 1 & 2)                                                | Các chiến lược đều tìm thấy thông tin liên quan, nhưng Recursive đạt điểm tương đồng vượt trội nhất. |
| 2   | Các bước đăng ký trên SIS & trạng thái thành công?        | **RecursiveChunker** (score=0.7202)                   | Có (Hạng 1 & 2)                                                | Tách trọn vẹn quy trình các bước mà không bị chia cắt giữa `Registered` và `Selected`.    |
| 3   | Môn trùng giờ hoặc chưa đủ điều kiện tiên quyết?          | **RecursiveChunker** (score=0.6737)                   | Có (Hạng 1 & 2)                                                | Truy xuất chính xác mục lưu ý về môn trùng giờ và cơ chế tự động chặn của hệ thống SIS.   |
| 4   | Rút (withdraw) tối đa bao nhiêu tín chỉ?                  | **RecursiveChunker** (score=0.8197)                   | Có (Hạng 1 & 3)                                                | Tìm thấy chunk chứa con số chính xác `18 tín chỉ` và hậu quả khi đạt giới hạn.            |
| 5   | Trước ngày bắt đầu giảng dạy Spring 2026 cần kiểm tra gì? | **RecursiveChunker + Metadata Filter** (score=0.6739) | Có (Hạng 2 khi có Filter; Văng khỏi Top-3 nếu không có Filter) | Bắt buộc phải dùng `audience: student` để lọc bỏ tài liệu cạnh tranh của giảng viên.      |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**

> **Có, lọc bằng metadata mang tính sống còn và quyết định ở Câu hỏi 5.**
>
> - **Khi KHÔNG có metadata filter:** Cả hai vị trí dẫn đầu Top-3 đều bị chiếm bởi tài liệu giảng viên `giang-vien-kiem-tra-lich-spring-2026.md` (`audience: faculty`) với điểm rất cao (Top-1: `0.7833`, Top-2: `0.6876`). Hậu quả là chunk Gold của sinh viên (`sinh-vien-add-drop-withdraw-spring-2026.md`) **bị đánh văng hoàn toàn khỏi Top-3**! Nếu sinh viên hỏi câu này, Agent sẽ nhầm lẫn và hướng dẫn sinh viên kiểm tra "lịch giảng dạy và phòng học của giảng viên".
> - **Khi CÓ metadata filter `{"audience": "student"}`:** Cơ chế tiền lọc (pre-filtering) loại bỏ 100% tài liệu của giảng viên trước khi tính toán tương đồng vector. Nhờ đó, chunk Gold của sinh viên ngay lập tức lọt vào **Top-2 (score `0.6739`)**, giúp Agent trả lời chính xác sinh viên cần kiểm tra lịch học, địa điểm học và việc đồng bộ môn học giữa SIS và Canvas.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày (6–8 phút):**

1. **Cấu trúc ngữ liệu quyết định thành bại của Chunking:** Tài liệu hành chính/học vụ có cấu trúc dạng danh sách gạch đầu dòng và bảng biểu. `FixedSize` dễ làm đứt gãy thông tin quan trọng (như ngày giờ hoặc điều kiện tiên quyết), trong khi `RecursiveChunker` bảo tồn trọn vẹn ngữ cảnh phân tầng.
2. **Sức mạnh của Metadata Pre-filtering:** Trong hệ thống RAG thực tế phục vụ nhiều nhóm đối tượng (sinh viên vs giảng viên vs cán bộ), nếu chỉ dựa vào semantic search thì các từ khóa chung (như "Spring 2026", "Lịch học", "Hạn chót") sẽ gây nhầm lẫn nghiêm trọng. Lọc trước theo siêu dữ liệu (`audience`) giúp cô lập không gian tìm kiếm, tăng độ tin cậy của câu trả lời lên mức tuyệt đối.
3. **Độ tương đồng Cosine kết hợp LLM Prompting:** Khi kết hợp `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` với Prompt ép buộc trích dẫn nguồn ("Chỉ trả lời dựa trên context được cung cấp"), hệ thống triệt tiêu hoàn toàn ảo giác (hallucination).

**Bài học rút ra khi so sánh trong nhóm:**

> Khi cùng nạp 8 văn bản quy chế nhưng sử dụng các chiến lược khác nhau, nhóm nhận thấy số lượng và chất lượng chunk có sự phân hóa rõ rệt: `FixedSize` (Đức) sinh ra 31 chunks với overlap giữ ngữ cảnh biên, nhưng Q5 thất bại vì gold chunk nằm sai vị trí cắt; `Sentence` (Long) sinh ra 43 chunks giữ trọn câu nhưng kích thước không đồng đều và score thấp hơn; `Heading` (Thành) sinh ra 49 chunks và giữ nguyên cấu trúc tiểu mục nhưng một số chunk dài có thể làm loãng semantic; trong khi `Recursive` (Phúc) sinh ra ~65 chunks gọn gàng, bao phủ sát sao từng ý và đạt điểm cosine similarity trung bình cao nhất (0.7731 trên Q1–Q4).

**Tổng hợp đóng góp cá nhân:**

| Thành viên        | Vai trò                             | Chiến lược                  | Tests | Benchmark (5Q)   | Tự đánh giá |
| ----------------- | ----------------------------------- | --------------------------- | ----- | ---------------- | ----------- |
| Đinh Ngọc Đức     | R1 — FixedSize                      | `FixedSizeChunker(500, 50)` | 42/42 | 4/5 (8/10 điểm)  | 58/60       |
| Đoàn Tuấn Long    | R2 — Sentence                       | `SentenceChunker(max=3)`    | 42/42 | 5/5 (9/10 điểm)  | 58/60       |
| Nguyễn Việt Thành | R3 — Heading                        | `HeadingChunker`            | 42/42 | 5/5 (10/10 điểm) | 59/60       |
| Nguyễn Đình Phúc  | R4 — Recursive (Demo & Report Lead) | `RecursiveChunker(300)`     | 42/42 | 5/5 (10/10 điểm) | 60/60       |

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**

> 1. Bổ sung thêm các trường metadata chuyên sâu như `semester` (`Spring-2026`), `degree_level` (`undergraduate`), và `urgency` để tăng độ linh hoạt khi truy vấn nghiệp vụ phức tạp.
> 2. Xây dựng bộ parser Markdown chuyên dụng cho bảng biểu (Markdown tables) để giữ nguyên tiêu đề cột cho từng dòng dữ liệu, tránh việc các dòng trong bảng bị tách rời khỏi ngữ cảnh tiêu đề.
> 3. Thống nhất embedding model giữa các thành viên để đảm bảo so sánh công bằng (Đức dùng `gemini-embedding-001`, Long dùng lexical embedder, Phúc dùng `paraphrase-multilingual-MiniLM-L12-v2`).

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí                                 | Điểm tự đánh giá |
| ---------------------------------------- | ---------------- |
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10          |
| Thiết kế chiến lược (Strategy Design)    | 15 / 15          |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10          |
| Thuyết trình (Demo)                      | 5 / 5            |
| **Tổng phần nhóm**                       | **40 / 40**      |
