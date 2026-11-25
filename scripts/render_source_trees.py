#!/usr/bin/env python3
"""Render high-resolution directory-tree PNG diagrams for Chapter 5.

Usage:
    python3 scripts/render_source_trees.py [--output-dir DIR]
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_MONO_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/JetBrainsMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
]
FONT_MONO_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/JetBrainsMono-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]
FONT_SANS_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_SANS_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

PRIMARY = (0, 72, 144)       # primaryBlue #004890
HEADER_TEXT = (255, 255, 255)
BORDER = (203, 213, 225)     # slate-300
ROW_EVEN = (255, 255, 255)
ROW_ODD = (248, 250, 252)    # slate-50
TREE_LINE = (148, 163, 184)  # slate-400
DIR_COLOR = (0, 72, 144)
FILE_COLOR = (15, 23, 42)    # slate-900
DESC_COLOR = (51, 65, 85)    # slate-700


def resolve_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    """Return the first available TrueType font from the candidate paths."""
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    raise FileNotFoundError(f"No font found in candidates: {candidates}")


def render_tree(
    out_path: str | Path,
    title: str,
    rows: list[tuple[str, str, bool, str]],
    split_x: int = 780,
    width: int = 1840,
) -> None:
    """Render a two-column directory tree diagram and save it as a PNG."""
    f_title = resolve_font(FONT_SANS_BOLD_CANDIDATES, 28)
    f_tree_bold = resolve_font(FONT_MONO_BOLD_CANDIDATES, 23)
    f_tree_reg = resolve_font(FONT_MONO_REG_CANDIDATES, 23)
    f_desc = resolve_font(FONT_SANS_REG_CANDIDATES, 23)
    f_header = resolve_font(FONT_SANS_BOLD_CANDIDATES, 22)

    pad_x = 34
    header_h = 64
    subhead_h = 46
    row_h = 42
    footer_pad = 16
    height = header_h + subhead_h + len(rows) * row_h + footer_pad

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Outer border & header bar
    draw.rectangle([0, 0, width - 1, header_h], fill=PRIMARY)
    draw.text((pad_x, 16), title, font=f_title, fill=HEADER_TEXT)

    # Column subheader
    draw.rectangle([0, header_h, width - 1, header_h + subhead_h], fill=(239, 246, 255))
    draw.line([(0, header_h + subhead_h), (width - 1, header_h + subhead_h)], fill=BORDER, width=2)
    draw.text((pad_x, header_h + 11), "Cấu trúc thư mục và tệp tiêu biểu", font=f_header, fill=PRIMARY)
    draw.text((split_x + 24, header_h + 11), "Vai trò / Tệp đại diện", font=f_header, fill=PRIMARY)

    # Vertical divider
    draw.line([(split_x, header_h), (split_x, height - 1)], fill=BORDER, width=2)

    y = header_h + subhead_h
    for idx, (prefix, name, is_dir, desc) in enumerate(rows):
        bg = ROW_ODD if idx % 2 == 1 else ROW_EVEN
        draw.rectangle([1, y, split_x - 1, y + row_h - 1], fill=bg)
        draw.rectangle([split_x + 2, y, width - 2, y + row_h - 1], fill=bg)
        draw.line([(1, y + row_h - 1), (width - 2, y + row_h - 1)], fill=(241, 245, 249), width=1)

        ty = y + 8
        # Draw tree prefix (box-drawing glyphs in JetBrainsMono-Regular)
        px_w = 0
        if prefix:
            draw.text((pad_x, ty), prefix, font=f_tree_reg, fill=TREE_LINE)
            bbox = draw.textbbox((0, 0), prefix, font=f_tree_reg)
            px_w = bbox[2] - bbox[0]

        font_name = f_tree_bold if is_dir else f_tree_reg
        color_name = DIR_COLOR if is_dir else FILE_COLOR
        draw.text((pad_x + px_w, ty), name, font=font_name, fill=color_name)

        # Draw description
        draw.text((split_x + 24, ty + 1), desc, font=f_desc, fill=DESC_COLOR)
        y += row_h

    # Outer border
    draw.rectangle([0, 0, width - 1, height - 1], outline=PRIMARY, width=3)
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_file, "PNG", optimize=True)


MONOREPO_ROWS = [
    ("", "RAG_TS/", True, "Thư mục gốc monorepo, chứa hai ứng dụng độc lập"),
    ("├── ", "backend_rag/", True, "Máy chủ NestJS 11 (API, RAG và pipeline nạp kho)"),
    ("│   ├── ", "src/", True, "Mã nguồn ứng dụng backend"),
    ("│   │   ├── ", "modules/", True, "Module tính năng có tầng API HTTP (auth/auth.service.ts)"),
    ("│   │   ├── ", "engines/", True, "Cổng cung cấp truy hồi và suy luận AI (judge/judge.service.ts)"),
    ("│   │   ├── ", "common/", True, "Tiện ích dùng chung giữa các module (pagination/pagination.ts)"),
    ("│   │   └── ", "config/", True, "Xác thực lược đồ biến môi trường (env.schema.ts)"),
    ("│   ├── ", "scripts/", True, "Script dòng lệnh (CLI) và tiến trình nạp dữ liệu"),
    ("│   │   └── ", "ingest/", True, "Pipeline nạp dữ liệu thượng nguồn 6 pha (ingest-source-objects.ts)"),
    ("│   ├── ", "benchmark/", True, "Bộ kiểm thử tải k6 bốn tầng (k6_rag_chat.ts)"),
    ("│   ├── ", "test/", True, "Kiểm thử đầu cuối E2E (flow.e2e-spec.ts)"),
    ("│   └── ", "docs/", True, "Tài liệu đặc tả kỹ thuật nội bộ máy chủ (MONGODB_SCHEMA_DESIGN.md)"),
    ("└── ", "frontend_rag/", True, "Ứng dụng giao diện React 19 + Vite 6"),
    ("    ├── ", "src/", True, "Mã nguồn giao diện và trạng thái ứng dụng"),
    ("    │   ├── ", "app/", True, "Khung vỏ ứng dụng, providers và định tuyến (AppShell.tsx)"),
    ("    │   ├── ", "features/", True, "Năm phân hệ tính năng độc lập (chat/store/ragStore.ts)"),
    ("    │   ├── ", "shared/", True, "Mã dùng chung: HTTP client, UI kit, theme (api/client.ts)"),
    ("    │   └── ", "test/", True, "Bộ kiểm thử đơn vị và tích hợp giao diện (featureModules.test.tsx)"),
    ("    ├── ", "e2e/", True, "Bộ kiểm thử đầu cuối Playwright (knowledge-tree.spec.ts)"),
    ("    ├── ", "docs/", True, "Báo cáo hiệu năng và Web Vitals (perf-report.md)"),
    ("    └── ", "scripts/", True, "Công cụ đo đạc hiệu năng kết xuất (perf-measure.cjs)"),
]

BACKEND_ROWS = [
    ("", "backend_rag/src/", True, "Mã nguồn lõi máy chủ NestJS"),
    ("├── ", "modules/", True, "Các phân hệ nghiệp vụ có tầng API HTTP"),
    ("│   ├── ", "auth/", True, "Xác thực, xoay vòng token và hồ sơ truy cập"),
    ("│   │   ├── ", "guards/", True, "Bảo vệ JWT và vai trò (jwt-auth.guard.ts)"),
    ("│   │   ├── ", "decorators/", True, "Trích xuất ngữ cảnh người dùng (current-user.decorator.ts)"),
    ("│   │   ├── ", "dto/", True, "Hợp đồng đầu vào/đầu ra (auth.dto.ts)"),
    ("│   │   └── ", "schemas/", True, "Schema Mongoose cho người dùng và token (user.schema.ts)"),
    ("│   ├── ", "admin/", True, "Quản trị tài khoản và nhật ký kiểm toán"),
    ("│   │   ├── ", "decorators/", True, "Gắn ngữ cảnh kiểm toán (audit-context.decorator.ts)"),
    ("│   │   ├── ", "dto/", True, "Hợp đồng quản trị (admin.dto.ts)"),
    ("│   │   └── ", "schemas/", True, "Schema kiểm toán append-only (admin-audit-log.schema.ts)"),
    ("│   ├── ", "chat-sessions/", True, "Quản lý phiên trò chuyện, tin nhắn và idempotency"),
    ("│   │   ├── ", "dto/", True, "Hợp đồng phân trang theo cursor và phiên (chat-session.dto.ts)"),
    ("│   │   └── ", "schemas/", True, "Schema phiên và tin nhắn UUIDv7 (chat-session.schema.ts)"),
    ("│   ├── ", "rag/", True, "Đường xử lý hỏi đáp RAG 7 pha"),
    ("│   │   ├── ", "pipeline/", True, "Dựng prompt, xếp hạng lại RRF và trích xuất nguồn (ranking.ts)"),
    ("│   │   ├── ", "transport/", True, "Luồng SSE, ping giữ kết nối và giới hạn slot (sse.ts)"),
    ("│   │   └── ", "dto/", True, "Hợp đồng yêu cầu hỏi đáp (chat-request.dto.ts)"),
    ("│   ├── ", "papers/", True, "Tra cứu chi tiết bài báo theo lô (papers.service.ts)"),
    ("│   ├── ", "health/", True, "Thăm dò tình trạng ba mức (health.service.ts)"),
    ("│   └── ", "api-root/", True, "Hợp đồng liên kết gốc HATEOAS (api-root.controller.ts)"),
    ("├── ", "engines/", True, "Bảy engine truy hồi và suy luận AI độc lập"),
    ("│   ├── ", "corpus/", True, "Đọc chỉ đọc kho khoa học MongoDB (paper-chunk.schema.ts)"),
    ("│   ├── ", "embedding/", True, "Sinh vector truy vấn 768 chiều (embedding.service.ts)"),
    ("│   ├── ", "vector-store/", True, "Truy vấn chỉ mục vector Qdrant chỉ đọc (vector-store.service.ts)"),
    ("│   ├── ", "judge/", True, "Bộ chấm điểm ONNX Laya và hai cổng kiểm soát (judge.service.ts)"),
    ("│   ├── ", "llm/", True, "Suy luận GGUF cục bộ và hàng đợi LLM (llm.service.ts)"),
    ("│   ├── ", "mining/", True, "Điểm uy tín PageRank và luật kết hợp (mining.service.ts)"),
    ("│   └── ", "tree-router/", True, "Định tuyến hai cấp trên cây tri thức (tree-router.service.ts)"),
    ("├── ", "common/", True, "Hạ tầng dùng chung toàn ứng dụng"),
    ("│   ├── ", "http/", True, "Content negotiation JSON/XML, bộ lọc lỗi và HATEOAS (xml.ts)"),
    ("│   ├── ", "logging/", True, "Ngữ cảnh nhật ký AsyncLocalStorage và UUIDv7 (request-context.ts)"),
    ("│   ├── ", "metrics/", True, "Bộ thu thập chỉ số Prometheus (prometheus-metrics.ts)"),
    ("│   ├── ", "pagination/", True, "Phân trang theo cursor kiểu limit + 1 (pagination.ts)"),
    ("│   ├── ", "security/", True, "Giới hạn tần suất và trust proxy (throttler.ts)"),
    ("│   └── ", "utils/", True, "Hàm tiện ích thuần dùng chung (uuid.ts)"),
    ("├── ", "config/", True, "Xác thực biến môi trường Zod (env.schema.ts)"),
    ("├── ", "testing/", True, "Khởi tạo ứng dụng thử nghiệm trong bộ nhớ (test-app.ts)"),
    ("└── ", "types/", True, "Khai báo kiểu TypeScript dùng chung (scientific-rag.ts)"),
]

FRONTEND_ROWS = [
    ("", "frontend_rag/src/", True, "Mã nguồn ứng dụng giao diện React 19"),
    ("├── ", "app/", True, "Khung ứng dụng (App shell)"),
    ("│   ├── ", "layout/", True, "Thanh điều hướng trên và khung bảng điều khiển (TopBar.tsx)"),
    ("│   ├── ", "providers/", True, "Cung cấp ngữ cảnh toàn cục React (AppProviders.tsx)"),
    ("│   └── ", "routers/", True, "Định tuyến trang cấp ứng dụng (AppRouter.tsx)"),
    ("├── ", "features/", True, "Năm phân hệ tính năng độc lập (vertical slice)"),
    ("│   ├── ", "auth/", True, "Đăng nhập, đăng ký và hồ sơ người dùng"),
    ("│   │   ├── ", "api/", True, "Client gọi API xác thực (authApi.ts)"),
    ("│   │   ├── ", "components/", True, "Nhãn trạng thái xác thực (AuthStatusBadge.tsx)"),
    ("│   │   ├── ", "hooks/", True, "Custom React hook quản lý phiên đăng nhập (useAuth.ts)"),
    ("│   │   └── ", "pages/", True, "Trang đăng nhập và tài khoản (AuthPage.tsx)"),
    ("│   ├── ", "chat/", True, "Hội thoại RAG, luồng SSE và hiển thị trích dẫn"),
    ("│   │   ├── ", "api/", True, "Client hỏi đáp và đồng bộ phiên (chatApi.ts)"),
    ("│   │   ├── ", "components/", True, "Hiển thị tin nhắn hội thoại và Markdown (MessageBubble.tsx)"),
    ("│   │   ├── ", "db/", True, "Kho cục bộ trình duyệt IndexedDB/Dexie (chatDb.ts)"),
    ("│   │   ├── ", "hooks/", True, "Custom React hook điều phối vùng làm việc (useChatWorkspace.ts)"),
    ("│   │   ├── ", "lib/", True, "Ánh xạ cấu trúc tin nhắn (messageMapping.ts)"),
    ("│   │   ├── ", "pages/", True, "Trang hội thoại chính (ChatPage.tsx)"),
    ("│   │   └── ", "store/", True, "Zustand store quản lý phiên và luồng SSE (sessionStore.ts)"),
    ("│   ├── ", "crawl/", True, "Theo dõi tiến độ thu thập và nạp dữ liệu"),
    ("│   │   ├── ", "api/", True, "Client kết nối luồng giám sát crawl (crawlApi.ts)"),
    ("│   │   ├── ", "components/", True, "Hiển thị dòng chỉ số tiến độ (CrawlMetricsRow.tsx)"),
    ("│   │   ├── ", "hooks/", True, "Custom React hook theo dõi telemetry (useCrawlTelemetry.ts)"),
    ("│   │   └── ", "pages/", True, "Trang bảng điều khiển thu thập (CrawlDashboardPage.tsx)"),
    ("│   ├── ", "result/", True, "Hiển thị và kiểm tra chi tiết bài báo khoa học"),
    ("│   │   ├── ", "api/", True, "Client tra cứu bài báo theo lô (resultApi.ts)"),
    ("│   │   ├── ", "components/", True, "Phần đầu tóm tắt kết quả tra cứu (ResultSummaryHeader.tsx)"),
    ("│   │   ├── ", "hooks/", True, "Custom React hook kiểm tra bài báo (usePaperInspector.ts)"),
    ("│   │   ├── ", "lib/", True, "Phân tích trường siêu dữ liệu arXiv (arxiv.ts)"),
    ("│   │   └── ", "pages/", True, "Trang xem chi tiết bài báo (ResultInspectorPage.tsx)"),
    ("│   └── ", "world/", True, "Không gian cây tri thức ba chiều WebGL/R3F"),
    ("│       ├── ", "api/", True, "Cầu nối dữ liệu cây tri thức 3D và bài báo thật (worldBridge.ts)"),
    ("│       ├── ", "components/", True, "Thanh điều khiển góc nhìn camera (CameraPresetBar.tsx)"),
    ("│       ├── ", "lib/", True, "Hình học nhánh cây và mặt phẳng nền 3D (treeGeometry.ts)"),
    ("│       ├── ", "pages/", True, "Trang khung cảnh 3D chính (WorldScenePage.tsx)"),
    ("│       ├── ", "scene/", True, "Các lớp đối tượng Three.js: vòm, hạt, mặt đất"),
    ("│       └── ", "store/", True, "Store trạng thái hiệu ứng thị giác (fxStore.ts)"),
    ("├── ", "shared/", True, "Mã dùng chung cho từ hai phân hệ trở lên"),
    ("│   ├── ", "api/", True, "HTTP client dùng chung và phân tích SSE (client.ts)"),
    ("│   │   └── ", "mock/", True, "Bộ dữ liệu giả lập tất định khi ngoại tuyến (mockChat.ts)"),
    ("│   ├── ", "hooks/", True, "Custom React hook dùng chung toàn app (useIsMobile.ts)"),
    ("│   ├── ", "lib/", True, "Hàm tiện ích thuần (rotation.ts)"),
    ("│   ├── ", "store/", True, "Store trạng thái giao diện chung (uiStore.ts)"),
    ("│   ├── ", "theme/", True, "Design token và cấu hình hiệu ứng glassmorphism (tokens.ts)"),
    ("│   ├── ", "types/", True, "Khai báo kiểu TypeScript dùng chung (rag.ts)"),
    ("│   └── ", "ui/", True, "Các thành phần giao diện nền tảng (Glass.tsx)"),
    ("└── ", "test/", True, "Bộ kiểm thử đơn vị và thành phần giao diện (featureModules.test.tsx)"),
]


def parse_args() -> argparse.Namespace:
    default_out = Path(__file__).resolve().parent.parent / "assets" / "diagrams"
    parser = argparse.ArgumentParser(
        description="Render directory-tree PNG diagrams for Chapter 5.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_out,
        help=f"Directory to write PNG files (default: {default_out})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir: Path = args.output_dir

    specs = [
        (
            "tree-monorepo.png",
            "Cấu trúc tổng thể monorepo RAG_TS",
            MONOREPO_ROWS,
            640,
            1820,
        ),
        (
            "tree-backend.png",
            "Cấu trúc mã nguồn tầng Backend (backend_rag/src)",
            BACKEND_ROWS,
            720,
            1920,
        ),
        (
            "tree-frontend.png",
            "Cấu trúc mã nguồn tầng Frontend (frontend_rag/src)",
            FRONTEND_ROWS,
            720,
            1920,
        ),
    ]

    for filename, title, rows, split_x, width in specs:
        render_tree(out_dir / filename, title, rows, split_x=split_x, width=width)


if __name__ == "__main__":
    main()
