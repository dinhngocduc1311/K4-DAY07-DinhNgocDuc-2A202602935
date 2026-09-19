# 5 câu hỏi đánh giá (Benchmark) — R2 gửi nhóm

**Chủ đề:** Đăng ký & điều chỉnh học phần (VinUni)  
**Corpus dùng chung:** `data/vinuni-course-registration/`  
**Ngày chốt:** 2026-09-19  

> Cả nhóm chạy **đúng 5 câu** dưới đây. Mỗi người chỉ khác chiến lược chunking.  
> Câu 5 **bắt buộc** dùng `metadata_filter={"audience": "student"}`.

---

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | File chứa thông tin | Filter |
|---|-----------------|----------------------------------|---------------------|--------|
| 1 | Cổng đăng ký SIS kỳ Spring 2026 mở lúc nào? | Cổng đăng ký SIS mở lúc **14:00 ngày 18/12/2025**. | `lich-dang-ky-spring-2026.md` | Không |
| 2 | Đăng ký học phần trên SIS gồm những bước nào? Trạng thái nào mới là đăng ký thành công? | Đăng nhập SIS → Academics → Course Registration → chọn học kỳ → Register khi Open → Add rồi Register. Trạng thái phải là **Registered** (`Selected` = chưa thành công). | `huong-dan-dang-ky-hoc-phan.md` | Không |
| 3 | Nếu môn trùng giờ hoặc chưa đủ điều kiện tiên quyết thì SIS xử lý thế nào? | SIS **không cho đăng ký môn trùng giờ** và **tự động chặn** khi chưa đạt tiên quyết. Nếu bị chặn dù nghĩ đủ điều kiện → liên hệ Phòng Quản lý Đào tạo. | `huong-dan-dang-ky-hoc-phan.md` | Không |
| 4 | Sinh viên được rút (withdraw) tối đa bao nhiêu tín chỉ trong cả chương trình? Sau khi đạt giới hạn thì sao? | Rút tối đa **18 tín chỉ** trong toàn chương trình. Khi đạt giới hạn phải tiếp tục học và nhận điểm cho môn đã đăng ký. | `sinh-vien-add-drop-withdraw-spring-2026.md` | Không |
| 5 | Trước ngày bắt đầu giảng dạy Spring 2026, tôi cần kiểm tra những gì? | Sinh viên phải xác nhận thời gian, địa điểm học và kiểm tra các môn đã đăng ký trên SIS được đồng bộ, hiển thị đúng trên Canvas. Nếu môn có trên SIS nhưng không xuất hiện trên Canvas thì báo Phòng Quản lý Đào tạo. | `sinh-vien-add-drop-withdraw-spring-2026.md` | **`{"audience": "student"}`** |

---

## Cách chạy (mỗi thành viên)

1. Nạp toàn bộ file `.md` trong `data/vinuni-course-registration/` (YAML → metadata, phần thân → content).
2. Chunk bằng **một** chiến lược riêng (không trùng nhau): FixedSize / Recursive / **Heading** (bắt buộc ≥1 người).
3. Với câu 1–4: `store.search(query, top_k=3)`.
4. Với câu 5, chạy A/B hai lần: một lần `store.search(query, top_k=3)`, một lần `store.search_with_filter(query, top_k=3, metadata_filter={"audience": "student"})`.
5. Đối chiếu với tài liệu cạnh tranh `giang-vien-kiem-tra-lich-spring-2026.md`: giảng viên cần kiểm tra lịch dạy, thời gian và phòng học; đây không phải gold answer dành cho sinh viên.
6. Ghi lại top-3 (score + doc_id + preview) của cả hai lượt để so sánh trong nhóm.
