# LaTeX Technical Documentation for JS/TS Course

## 1. Yêu cầu hệ thống tối thiểu (Prerequisites)

| Công cụ / Gói | Phiên bản tối thiểu | Ghi chú |
| :--- | :--- | :--- |
| **TeX Distribution** | TeX Live 2024+ / MacTeX 2024+ | Hỗ trợ cơ chế `latexminted` và restricted shell escape |
| **Trình biên dịch** | XeLaTeX (`xelatex`) | Hỗ trợ Unicode native và nạp font `.ttf` qua `fontspec` |
| **Công cụ tự động hóa**| `latexmk` (v4.80+) | Quản lý quy trình biên dịch nhiều lượt và xuất file vào `build/` |
| **Tô màu cú pháp** | `minted` 3.x (`latexminted`) | Highlight mã nguồn JS / TS |
| **Python** | Python 3.10 – 3.13 | Chạy backend `latexminted` (khuyến nghị 3.12) |
| **Trình soạn thảo** | Visual Studio Code | Khuyên dùng kèm extension LaTeX Workshop |

---

## 2. Cài đặt môi trường theo từng hệ điều hành

### 2.1. Ubuntu / Debian (Linux)

1. **Cài đặt TeX Live và các gói phụ thuộc:**
   ```bash
   sudo apt update
   sudo apt install -y texlive-xetex texlive-latex-extra texlive-fonts-recommended latexmk python3-pygments
   ```

2. **Cài đặt hoặc cập nhật gói minted 3.x & latexminted:**
   Nếu bản phân phối TeX Live của bạn chưa có `latexminted`:
   ```bash
   pip install --user latexminted pygments
   ```

3. **Cài đặt VS Code và tiện ích mở rộng:**
   - Cài đặt extension: **LaTeX Workshop** (`James-Yu.latex-workshop`).

---

### 2.2. Windows

1. **Cài đặt TeX Live (Khuyến nghị):**
   - Tải bộ cài `install-tl-windows.exe` từ trang chủ [TeX Live](https://www.tug.org/texlive/).
   - Trong quá trình cài đặt, chọn *Full scheme* hoặc tối thiểu các gói: `collection-xetex`, `collection-latexextra`, `latexmk`, `minted`.
   - Đảm bảo tùy chọn **"Add to PATH"** được tích chọn.

2. **Cài đặt Python & Pygments:**
   - Cài đặt Python 3.11 hoặc 3.12 từ [python.org](https://www.python.org/) hoặc Microsoft Store (tích chọn *Add Python to PATH*).
   - Mở PowerShell và cài đặt:
     ```powershell
     pip install pygments latexminted
     ```

3. **Tích hợp VS Code:**
   - Cài đặt VS Code và extension **LaTeX Workshop**.

---

### 2.3. macOS

1. **Cài đặt MacTeX:**
   Sử dụng Homebrew:
   ```bash
   brew install --cask mactex
   ```
   *(Hoặc tải gói MacTeX.pkg từ [tug.org/mactex](https://www.tug.org/mactex/))*.

2. **Cập nhật gói và kiểm tra python:**
   ```bash
   sudo tlmgr update --self
   sudo tlmgr install minted latexmk
   pip3 install --user latexminted pygments
   ```

---

## 3. Kiểm tra môi trường (Environment Verification)

Trước khi bắt đầu, chạy script kiểm tra tự động để xác nhận đầy đủ dependencies và font chữ:

- **Trên Linux / macOS:**
  ```bash
  ./scripts/verify_env.sh
  ```
- **Trên Windows (PowerShell):**
  ```powershell
  .\scripts\verify_env.ps1
  ```

Script sẽ kiểm tra sự hiện diện của `xelatex`, `latexmk`, `minted.sty`, `latexminted`, các file font trong `fonts/`, và thực hiện một lượt biên dịch thử nghiệm với mã nguồn JavaScript / TypeScript mẫu.

---

## 4. Quản lý thông tin bảo mật & Metadata nhóm

Theo yêu cầu chuẩn hóa, các thông tin định danh cá nhân và thông tin trường lớp **không được commit lên Git**.

1. Khởi tạo file cấu hình thông tin cá nhân:
   ```bash
   cp metadata.example.tex metadata.tex
   ```
2. Mở file `metadata.tex` và cập nhật thông tin:
   - Tên cơ quan, trường, viện (`\universityName`, `\facultyName`, ...).
   - Tên đề tài, học phần, mã lớp, giảng viên hướng dẫn.
   - Bảng thông tin 5 thành viên nhóm:
     - Họ và tên (`\memberOneName`, `\memberTwoName`, ...)
     - MSSV (`\memberOneId`, `\memberTwoId`, ...)
     - % Hoàn thành nhiệm vụ (`\memberOneProgress`, ...)
3. File `metadata.tex` đã được cấu hình trong `.gitignore` để luôn được giữ bảo mật trên máy cá nhân.

---

## 5. Hướng dẫn biên dịch (Build Workflow)

### 5.1. Sử dụng Script dòng lệnh

- **Biên dịch tài liệu ra thư mục `build/`:**
  - Linux/macOS:
    ```bash
    ./compile.sh
    ```
  - Windows:
    ```cmd
    compile.bat
    ```
- **Dọn dẹp thư mục tạm:**
  ```bash
  ./compile.sh clean
  # hoặc trên Windows:
  compile.bat clean
  ```
- **Chế độ tự động biên dịch khi lưu (Watch mode):**
  ```bash
  ./compile.sh watch
  # hoặc trên Windows:
  compile.bat watch
  ```

---

## 6. Hướng dẫn chèn mã nguồn (JavaScript & TypeScript)

Trong tài liệu, sử dụng các môi trường đã định nghĩa sẵn trong `preamble.tex`:

### JavaScript Box
```latex
\begin{jsbox}{Thuật toán sinh khóa RSA (Node.js)}
import crypto from 'crypto';

export function generateKeys() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
  });
  return { publicKey, privateKey };
}
\end{jsbox}
```

### TypeScript Box
```latex
\begin{tsbox}{Định nghĩa kiểu và interface}
interface CipherResult {
  readonly ciphertext: string;
  readonly iv: string;
  readonly tag?: string;
}

const encryptData = (data: string): CipherResult => {
  // Implementation in TypeScript
  return { ciphertext: "...", iv: "..." };
};
\end{tsbox}
```

### Inline code
- JavaScript: `\jscode{const x = 10;}`
- TypeScript: `\tscode{type ID = string | number;}`

