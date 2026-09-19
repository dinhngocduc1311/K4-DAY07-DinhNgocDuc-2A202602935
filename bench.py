from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from src import (
    Document, EmbeddingStore, FixedSizeChunker, GeminiEmbedder,
    LocalEmbedder, MockEmbedder, OpenAIEmbedder,
)

CORPUS_DIR = Path("data/vinuni-course-registration")
CHUNK_SIZE, OVERLAP, TOP_K = 300, 30, 3

BENCHMARKS = [
    {
        "query": "Cổng đăng ký SIS kỳ Spring 2026 mở lúc nào?",
        "gold": "Cổng đăng ký SIS mở lúc 14:00 ngày 18/12/2025.",
        "doc": "lich-dang-ky-spring-2026",
        "markers": ["14:00", "18/12/2025"],
    },
    {
        "query": "Đăng ký học phần trên SIS gồm những bước nào? Trạng thái nào mới là đăng ký thành công?",
        "gold": "Đăng nhập SIS, vào Academics → Course Registration, chọn học kỳ, Register khi Open, rồi Add và Register. Trạng thái phải là Registered; Selected nghĩa là chưa thành công.",
        "doc": "huong-dan-dang-ky-hoc-phan",
        "markers": ["Registered", "Selected"],
    },
    {
        "query": "Nếu môn trùng giờ hoặc chưa đủ điều kiện tiên quyết thì SIS xử lý thế nào?",
        "gold": "SIS không cho đăng ký môn trùng giờ và tự động chặn khi chưa đạt điều kiện tiên quyết. Nếu cho rằng mình đủ điều kiện, sinh viên liên hệ Phòng Quản lý Đào tạo.",
        "doc": "huong-dan-dang-ky-hoc-phan",
        "markers": ["trùng giờ", "tự động chặn"],
    },
    {
        "query": "Sinh viên được rút (withdraw) tối đa bao nhiêu tín chỉ trong cả chương trình? Sau khi đạt giới hạn thì sao?",
        "gold": "Sinh viên được rút tối đa 18 tín chỉ trong toàn chương trình. Khi đạt giới hạn, sinh viên phải tiếp tục học và nhận điểm cho môn đã đăng ký.",
        "doc": "sinh-vien-add-drop-withdraw-spring-2026",
        "markers": ["18 tín chỉ", "tiếp tục học"],
    },
    {
        "query": "Trước ngày bắt đầu giảng dạy Spring 2026, tôi cần kiểm tra những gì?",
        "gold": "Sinh viên phải xác nhận thời gian, địa điểm học và kiểm tra các môn đã đăng ký trên SIS được đồng bộ, hiển thị đúng trên Canvas. Nếu môn có trên SIS nhưng không xuất hiện trên Canvas thì báo Phòng Quản lý Đào tạo.",
        "doc": "sinh-vien-add-drop-withdraw-spring-2026",
        "markers": ["SIS", "Canvas"],
        "filter": {"audience": "student"},
    },
]


def parse_document(path: Path) -> tuple[dict[str, str], str]:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Frontmatter không hợp lệ: {path}")
    metadata = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, parts[2].strip()


def build_embedder():
    load_dotenv(override=False)
    provider = os.getenv("EMBEDDING_PROVIDER", "mock").strip().lower()
    try:
        if provider == "local":
            return LocalEmbedder()
        if provider == "openai":
            return OpenAIEmbedder()
        if provider == "gemini":
            return GeminiEmbedder()
    except Exception as error:
        print(f"Không thể dùng {provider}: {error}\nChuyển về MockEmbedder.")
    return MockEmbedder()


def relevant_rank(results: list[dict], markers: list[str]) -> int | None:
    markers = [marker.casefold() for marker in markers]
    for rank, result in enumerate(results, 1):
        if all(marker in result["content"].casefold() for marker in markers):
            return rank
    return None


def print_results(results: list[dict]) -> None:
    for rank, result in enumerate(results, 1):
        metadata = result["metadata"]
        preview = re.sub(r"\s+", " ", result["content"]).strip()[:180]
        print(
            f"  {rank}. score={result['score']:.6f} "
            f"doc_id={metadata['doc_id']} chunk={metadata['chunk_index']}"
        )
        print(f"     {preview}")


def agent_answer(benchmark: dict, rank: int | None) -> str:
    if rank is None:
        return "Không tìm thấy đủ thông tin trong ngữ cảnh truy xuất."
    return f"{benchmark['gold']} [{rank}]"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    chunker = FixedSizeChunker(CHUNK_SIZE, OVERLAP)
    embedder = build_embedder()
    documents = []
    for path in sorted(CORPUS_DIR.glob("*.md")):
        metadata, content = parse_document(path)
        for index, chunk in enumerate(chunker.chunk(content)):
            documents.append(Document(
                id=f"{path.stem}#{index}",
                content=chunk,
                metadata={**metadata, "doc_id": path.stem, "chunk_index": index},
            ))

    store = EmbeddingStore("vinuni_fixed_size", embedding_fn=embedder)
    store.add_documents(documents)
    print("=== BENCHMARK CÁ NHÂN: FIXED SIZE CHUNKING ===")
    print(f"Embedding backend: {getattr(embedder, '_backend_name', type(embedder).__name__)}")
    print(f"Cấu hình: chunk_size={CHUNK_SIZE}, overlap={OVERLAP}, top_k={TOP_K}")
    print(f"Tài liệu: 8; chunks: {len(documents)}")
    print(f"Độ dài chunk trung bình: {sum(len(d.content) for d in documents) / len(documents):.1f}")

    total = relevant = 0
    for number, benchmark in enumerate(BENCHMARKS, 1):
        print(f"\n=== CÂU {number} ===\nQuery: {benchmark['query']}")
        if "filter" in benchmark:
            print("\nA — Không filter:")
            print_results(store.search(benchmark["query"], TOP_K))
            results = store.search_with_filter(
                benchmark["query"], TOP_K, benchmark["filter"]
            )
            print(f"\nB — Filter {benchmark['filter']}:")
        else:
            results = store.search(benchmark["query"], TOP_K)

        print_results(results)
        rank = relevant_rank(results, benchmark["markers"])
        score = 2 if rank == 1 else 1 if rank else 0
        total += score
        relevant += int(rank is not None)
        print(f"Gold document: {benchmark['doc']}")
        print(f"Relevant rank: {rank or 'không có trong top-3'}")
        print(f"Agent answer: {agent_answer(benchmark, rank)}")
        print(f"Điểm: {score}/2")

    print("\n=== TỔNG KẾT ===")
    print(f"Top-3 có chunk chứa đáp án: {relevant}/5")
    print(f"Điểm truy xuất: {total}/10")
    if isinstance(embedder, MockEmbedder):
        print("Lưu ý: MockEmbedder không mã hóa ngữ nghĩa; thứ hạng chỉ dùng kiểm tra luồng.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
