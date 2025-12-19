def _require_lib(func):
    def wrapper(*args, **kwargs):
        if not pyautogui:
            raise RuntimeError("缺少库文件")
        return func(*args, **kwargs)
    return wrapper


@_require_lib
def get_screen_size():
    return pyautogui.size()


def ensure_ready():
    w, h = get_screen_size()


@_require_lib
def screencap(idx: int) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / f"raw_{idx:03d}.png"
    
    img = pyautogui.screenshot()
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, format='PNG', optimize=True)
    
    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError(f"保存失败: {dest}")
    
    return dest


@_require_lib
def flip_page():
    pyautogui.press(FLIP_KEY)
    time.sleep(WAIT_AFTER_FLIP)


def images_to_pdf(img_paths: List[Path], pdf_file: Path):
    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    with open(pdf_file, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in img_paths], dpi=300, x=0, y=0))


def capture_pages():
    ensure_ready()
    time.sleep(WAIT_BEFORE_FIRST)
    
    for i in range(1, TOTAL_PAGES + 1):
        screencap(i)
        if i < TOTAL_PAGES:
            flip_page()


def build_pdf():
    images = sorted(raw_dir.glob("raw_*.png"), key=lambda p: int(p.stem.split('_')[-1]))
    if not images:
        raise RuntimeError("raw目录下没有文件")
    images_to_pdf(images, pdf_path)


