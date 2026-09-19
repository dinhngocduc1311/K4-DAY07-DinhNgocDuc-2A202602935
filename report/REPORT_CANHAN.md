# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Đinh Ngọc Đức
**Nhóm:** G13
**Ngày:** 19/09/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Hai vector embedding có cosine similarity cao khi chúng cùng hướng, nghĩa là hai văn bản được mô hình biểu diễn là gần nhau về ngữ nghĩa. Điểm càng gần 1 thì mức tương đồng càng cao; gần 0 là ít liên quan và gần -1 là đối lập về hướng vector.

**Ví dụ có độ tương tự CAO:**
- Câu A: “Sinh viên cần nộp học phí trước hạn.”
- Câu B: “Người học phải hoàn tất khoản thu đúng thời hạn.”
- Tại sao tương đồng: Hai câu dùng từ khác nhau nhưng đều nói về nghĩa vụ thanh toán học phí đúng hạn.

**Ví dụ có độ tương tự THẤP:**
- Câu A: “Sinh viên đăng ký học phần trên cổng học vụ.”
- Câu B: “Hôm nay trời mưa lớn.”
- Tại sao khác: Hai câu thuộc hai chủ đề và mục đích hoàn toàn khác nhau.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine tập trung vào hướng của vector nên ít bị ảnh hưởng bởi độ lớn vector hoặc độ dài văn bản. Khoảng cách Euclid phụ thuộc cả độ lớn, vì vậy hai embedding cùng hướng nhưng khác chuẩn có thể bị xem là xa nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> Phép tính: `ceil((10.000 - 50) / (500 - 50)) = ceil(9.950 / 450) = ceil(22,111...) = 23`.
>
> Kiểm chứng bằng `FixedSizeChunker(chunk_size=500, overlap=50)` cũng trả về **23 chunks**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Số chunk tăng thành `ceil((10.000 - 100) / (500 - 100)) = ceil(9.900 / 400) = 25`, đúng với kết quả chạy `FixedSizeChunker`. Overlap lớn hơn giúp giữ ngữ cảnh nằm sát ranh giới chunk, đổi lại làm tăng dữ liệu trùng lặp, dung lượng lưu trữ và chi phí embedding/search.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**Chiến lược benchmark cá nhân — `FixedSizeChunker`:**
> Tôi dùng `chunk_size=300`, `overlap=30`. Mỗi bước tiến 270 ký tự; phần chồng lấp giúp thông tin nằm sát biên còn xuất hiện ở chunk kế tiếp. Tôi chỉ chunk phần thân Markdown, không chunk YAML frontmatter; mỗi chunk có ID dạng `doc_id#index` và kế thừa toàn bộ metadata của tài liệu gốc.

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Tôi dùng regex `(?<=[.!?])\s+`: positive lookbehind đặt điểm tách sau dấu câu nên vẫn giữ `.`, `!`, `?`. Các câu được gom theo `max_sentences_per_chunk`; chuỗi rỗng trả `[]` và tham số số câu được chặn tối thiểu là 1. Cách đơn giản này có thể cắt sai chữ viết tắt như “TS.”, “v.v.” hoặc số thập phân; nếu corpus có nhiều trường hợp đó thì cần bộ tách câu chuyên dụng hơn.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Thuật toán thử separator theo thứ tự `["\n\n", "\n", ". ", " ", ""]`. Mảnh dài hơn `chunk_size` được đệ quy với separator nhỏ hơn, còn các mảnh ngắn liền nhau được gom đến sát giới hạn để tránh chunk vụn. Ba trường hợp dừng là: text đã đủ ngắn, hết separator, hoặc gặp separator rỗng; hai trường hợp cuối cắt cứng theo `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Store dùng danh sách in-memory đúng yêu cầu lab; mỗi `Document` được copy metadata, thêm `doc_id` gốc và embedding đúng một lần. `search` embedding truy vấn, tính dot product với từng record và sắp xếp giảm dần; vì backend chuẩn hóa vector nên dot product tương đương cosine similarity. `add_documents` không tự chunk: mỗi `Document` đầu vào là một record.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter` lọc metadata trước rồi mới gọi chung `_search_records`, nhờ đó tài liệu sai bộ lọc không chiếm chỗ trong top-k. `delete_document` loại toàn bộ record có `metadata["doc_id"]` khớp và trả `True` khi kích thước store thực sự giảm.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Agent truy xuất top-k, đánh số từng chunk `[1]`, `[2]`, … và gắn nguồn trước khi đưa vào prompt. Prompt yêu cầu chỉ dùng context, trích dẫn số chunk và nói rõ khi không đủ dữ kiện để giảm hallucination. Nếu store rỗng, agent trả thông báo ngay và không gọi `llm_fn`.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
$ python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.12.9, pytest-9.1.1
collecting ... collected 42 items

tests/test_solution.py ..........................................       [100%]

============================= 42 passed in 0.13s ==============================
```

**Số lượng bài test vượt qua (pass):** **42 / 42**

Checkpoint riêng cho chunking/similarity/comparator cũng đạt **23 passed, 19 deselected**.

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên đăng ký học phần trên cổng học vụ. | Người học ghi danh môn học qua hệ thống học vụ. | Cao | 0.870785 | Có |
| 2 | Thư viện cho sinh viên mượn tài liệu. | Sinh viên có thể mượn sách tại thư viện. | Cao | 0.909629 | Có |
| 3 | Hạn đóng học phí là cuối tháng. | Hôm nay trời mưa lớn. | Thấp | 0.576129 | Có |
| 4 | Python là ngôn ngữ lập trình bậc cao. | Machine learning học từ dữ liệu. | Thấp | 0.604107 | Có |
| 5 | Lịch thi được công bố trên cổng sinh viên. | Công thức này cần hai quả trứng. | Thấp | 0.572448 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Gemini cho hai cặp đồng nghĩa điểm cao nhất (0.870785 và 0.909629), đúng với dự đoán. Ba cặp khác chủ đề vẫn có điểm dương khoảng 0.57–0.60, cho thấy không nên dùng ngưỡng 0 làm ranh giới cao/thấp; điều quan trọng là so sánh thứ hạng tương đối trên cùng model và corpus.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Tôi dùng `FixedSizeChunker(chunk_size=300, overlap=30)` trên phần thân của 8 tài liệu VinUni. Frontmatter được chuyển thành metadata cho từng chunk. Store nhận **50 chunks**, độ dài trung bình **277,7 ký tự**, và truy xuất với `top_k=3`.

| # | Câu hỏi (rút gọn) | Top-1 sau filter (doc_id — score) | Hạng chunk chứa đáp án | Điểm | Đáp án grounded |
|---|---|---|---:|---:|---|
| 1 | Cổng SIS Spring 2026 mở lúc nào? | `lich-dang-ky-spring-2026` — 0.894064 | 1 | 2/2 | Mở lúc 14:00 ngày 18/12/2025 [1] |
| 2 | Các bước đăng ký và trạng thái thành công? | `huong-dan-dang-ky-hoc-phan` — 0.806445 | 1 | 2/2 | Thực hiện trên SIS; phải ở trạng thái Registered, không phải Selected [1] |
| 3 | Trùng giờ/chưa đủ tiên quyết xử lý thế nào? | `huong-dan-dang-ky-hoc-phan` — 0.803733 | 1 | 2/2 | SIS chặn môn trùng giờ hoặc chưa đạt tiên quyết [1] |
| 4 | Giới hạn tín chỉ withdrawal? | `sinh-vien-add-drop-withdraw-spring-2026` — 0.831586 | 1 | 2/2 | Tối đa 18 tín chỉ; đạt giới hạn thì phải tiếp tục học và nhận điểm [1] |
| 5 | Trước ngày giảng dạy, sinh viên kiểm tra gì? | `lich-dang-ky-spring-2026` — 0.796817 | 2 | 1/2 | Kiểm tra thời gian, địa điểm và SIS đồng bộ đúng lên Canvas [2] |

**Tổng kết:** top-3 có chunk thực sự chứa đáp án **5/5**; điểm truy xuất **9/10**.

**A/B metadata filter ở câu 5:** khi không lọc, top-1 là tài liệu dành cho giảng viên (`giang-vien-kiem-tra-lich-spring-2026`, score 0.864947), còn chunk sinh viên đúng đứng hạng 3. Với `metadata_filter={audience: student}`, tài liệu giảng viên bị loại trước retrieval và chunk đúng lên hạng 2. Filter tăng precision theo audience nhưng chưa đưa chunk trả lời lên top-1.

**Failure case:** ở câu 5, metadata filter loại đúng tài liệu giảng viên nhưng top-1 vẫn là chunk lịch đăng ký; chunk thực sự trả lời về SIS/Canvas đứng hạng 2. Nếu chỉ chấm theo `doc_id` thì dễ đánh giá sai chất lượng. Có thể cải thiện bằng chunk theo heading hoặc diễn đạt query cụ thể hơn; khi so sánh giữa thành viên phải giữ nguyên query, top-k và embedding.

**Tính trung thực của phép đo:** lượt chạy chính thức dùng `gemini-embedding-001` (3072 chiều). Phần “đáp án grounded” trong `bench.py` chỉ trả gold answer khi top-3 có cùng một chunk chứa đủ chuỗi đặc trưng. Output đầy đủ nằm trong `ket_qua_benchmark.txt`.

**Điều hay nhất tôi học được:** phải chấm ở cấp chunk chứa câu trả lời, không chỉ kiểm tra `doc_id`; đồng thời mọi thành viên phải giữ nguyên corpus, query, top-k và embedding, chỉ thay dòng chọn chunker thì so sánh mới công bằng.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 9 / 10 |
| **Tổng phần cá nhân** | **59 / 60** |
